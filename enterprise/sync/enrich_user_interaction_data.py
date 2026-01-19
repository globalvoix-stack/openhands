import asyncio

from integrations.github.data_collector import GitHubDataCollector
from storage.thinksoft_pr import ThinksoftPR
from storage.thinksoft_pr_store import ThinksoftPRStore

from thinksoft.core.logger import thinksoft_logger as logger

PROCESS_AMOUNT = 50
MAX_RETRIES = 3

store = ThinksoftPRStore.get_instance()
data_collector = GitHubDataCollector()


def get_unprocessed_prs() -> list[ThinksoftPR]:
    """
    Get unprocessed PR entries from the ThinksoftPR table.

    Args:
        limit: Maximum number of PRs to retrieve (default: 50)

    Returns:
        List of ThinksoftPR objects that need processing
    """
    unprocessed_prs = store.get_unprocessed_prs(PROCESS_AMOUNT, MAX_RETRIES)
    logger.info(f'Retrieved {len(unprocessed_prs)} unprocessed PRs for enrichment')
    return unprocessed_prs


async def process_pr(pr: ThinksoftPR):
    """
    Process a single PR to enrich its data.
    """

    logger.info(f'Processing PR #{pr.pr_number} from repo {pr.repo_name}')
    await data_collector.save_full_pr(pr)
    store.increment_process_attempts(pr.repo_id, pr.pr_number)


async def main():
    """
    Main function to retrieve and process unprocessed PRs.
    """
    logger.info('Starting PR data enrichment process')

    # Get unprocessed PRs
    unprocessed_prs = get_unprocessed_prs()
    logger.info(f'Found {len(unprocessed_prs)} PRs to process')

    # Process each PR
    for pr in unprocessed_prs:
        try:
            await process_pr(pr)
            logger.info(
                f'Successfully processed PR #{pr.pr_number} from repo {pr.repo_name}'
            )
        except Exception as e:
            logger.exception(
                f'Error processing PR #{pr.pr_number} from repo {pr.repo_name}: {str(e)}'
            )

    logger.info('PR data enrichment process completed')


if __name__ == '__main__':
    asyncio.run(main())
