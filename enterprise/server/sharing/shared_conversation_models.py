from datetime import datetime
from enum import Enum

# Simplified imports to avoid dependency chain issues
# from thinksoft.integrations.service_types import ProviderType
# from thinksoft.sdk.llm import MetricsSnapshot
# from thinksoft.storage.data_models.conversation_metadata import ConversationTrigger
# For now, use Any to avoid import issues
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field

from thinksoft.agent_server.utils import ThinksoftUUID, utc_now

ProviderType = Any
MetricsSnapshot = Any
ConversationTrigger = Any


class SharedConversation(BaseModel):
    """Shared conversation info model with all fields from AppConversationInfo."""

    id: ThinksoftUUID = Field(default_factory=uuid4)

    created_by_user_id: str | None
    sandbox_id: str

    selected_repository: str | None = None
    selected_branch: str | None = None
    git_provider: ProviderType | None = None
    title: str | None = None
    pr_number: list[int] = Field(default_factory=list)
    llm_model: str | None = None

    metrics: MetricsSnapshot | None = None

    parent_conversation_id: ThinksoftUUID | None = None
    sub_conversation_ids: list[ThinksoftUUID] = Field(default_factory=list)

    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)


class SharedConversationSortOrder(Enum):
    CREATED_AT = 'CREATED_AT'
    CREATED_AT_DESC = 'CREATED_AT_DESC'
    UPDATED_AT = 'UPDATED_AT'
    UPDATED_AT_DESC = 'UPDATED_AT_DESC'
    TITLE = 'TITLE'
    TITLE_DESC = 'TITLE_DESC'


class SharedConversationPage(BaseModel):
    items: list[SharedConversation]
    next_page_id: str | None = None
