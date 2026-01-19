from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import and_, desc
from sqlalchemy.orm import sessionmaker
from storage.database import session_maker
from storage.thinksoft_pr import ThinksoftPR

from thinksoft.core.logger import thinksoft_logger as logger
from thinksoft.integrations.service_types import ProviderType


@dataclass
class ThinksoftPRStore:
    session_maker: sessionmaker

    def insert_pr(self, pr: ThinksoftPR) -> None:
        """
        Insert a new PR or delete and recreate if repo_id and pr_number already exist.
        """
        with self.session_maker() as session:
            # Check if PR already exists
            existing_pr = (
                session.query(ThinksoftPR)
                .filter(
                    ThinksoftPR.repo_id == pr.repo_id,
                    ThinksoftPR.pr_number == pr.pr_number,
                    ThinksoftPR.provider == pr.provider,
                )
                .first()
            )

            if existing_pr:
                # Delete existing PR
                session.delete(existing_pr)
                session.flush()

            session.add(pr)
            session.commit()

    def increment_process_attempts(self, repo_id: str, pr_number: int) -> bool:
        """
        Increment the process attempts counter for a PR.

        Args:
            repo_id: Repository identifier
            pr_number: Pull request number

        Returns:
            True if PR was found and updated, False otherwise
        """
        with self.session_maker() as session:
            pr = (
                session.query(ThinksoftPR)
                .filter(
                    ThinksoftPR.repo_id == repo_id, ThinksoftPR.pr_number == pr_number
                )
                .first()
            )

            if pr:
                pr.process_attempts += 1
                session.merge(pr)
                session.commit()
                return True
            return False

    def update_pr_thinksoft_stats(
        self,
        repo_id: str,
        pr_number: int,
        original_updated_at: datetime,
        thinksoft_helped_author: bool,
        num_thinksoft_commits: int,
        num_thinksoft_review_comments: int,
        num_thinksoft_general_comments: int,
    ) -> bool:
        """
        Update Thinksoft statistics for a PR with row-level locking and timestamp validation.

        Args:
            repo_id: Repository identifier
            pr_number: Pull request number
            original_updated_at: Original updated_at timestamp to check for concurrent modifications
            thinksoft_helped_author: Whether Thinksoft helped the author (1+ commits)
            num_thinksoft_commits: Number of commits by Thinksoft
            num_thinksoft_review_comments: Number of review comments by Thinksoft
            num_thinksoft_general_comments: Number of PR comments (not review comments) by Thinksoft

        Returns:
            True if PR was found and updated, False if not found or timestamp changed
        """
        with self.session_maker() as session:
            # Use row-level locking to prevent concurrent modifications
            pr: ThinksoftPR | None = (
                session.query(ThinksoftPR)
                .filter(
                    ThinksoftPR.repo_id == repo_id, ThinksoftPR.pr_number == pr_number
                )
                .with_for_update()
                .first()
            )

            if not pr:
                # Current PR snapshot is stale
                logger.warning('Did not find PR {pr_number} for repo {repo_id}')
                return False

            # Check if the updated_at timestamp has changed (indicating concurrent modification)
            if pr.updated_at != original_updated_at:
                # Abort transaction - the PR was modified by another process
                session.rollback()
                return False

            # Update the Thinksoft statistics
            pr.thinksoft_helped_author = thinksoft_helped_author
            pr.num_thinksoft_commits = num_thinksoft_commits
            pr.num_thinksoft_review_comments = num_thinksoft_review_comments
            pr.num_thinksoft_general_comments = num_thinksoft_general_comments
            pr.processed = True

            session.merge(pr)
            session.commit()
            return True

    def get_unprocessed_prs(
        self, limit: int = 50, max_retries: int = 3
    ) -> list[ThinksoftPR]:
        """
        Get unprocessed PR entries from the ThinksoftPR table.

        Args:
            limit: Maximum number of PRs to retrieve (default: 50)

        Returns:
            List of ThinksoftPR objects that need processing
        """
        with self.session_maker() as session:
            unprocessed_prs = (
                session.query(ThinksoftPR)
                .filter(
                    and_(
                        ~ThinksoftPR.processed,
                        ThinksoftPR.process_attempts < max_retries,
                        ThinksoftPR.provider == ProviderType.GITHUB.value,
                    )
                )
                .order_by(desc(ThinksoftPR.updated_at))
                .limit(limit)
                .all()
            )

            return unprocessed_prs

    @classmethod
    def get_instance(cls):
        """Get an instance of the ThinksoftPRStore."""
        return ThinksoftPRStore(session_maker)
