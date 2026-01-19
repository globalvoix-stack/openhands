from datetime import datetime
from enum import Enum
from uuid import uuid4

from pydantic import BaseModel, Field

from thinksoft.agent_server.utils import ThinksoftUUID, utc_now
from thinksoft.sdk.event.types import EventID


class EventCallbackResultStatus(Enum):
    SUCCESS = 'SUCCESS'
    ERROR = 'ERROR'


class EventCallbackResultSortOrder(Enum):
    CREATED_AT = 'CREATED_AT'
    CREATED_AT_DESC = 'CREATED_AT_DESC'


class EventCallbackResult(BaseModel):
    """Object representing the result of an event callback."""

    id: ThinksoftUUID = Field(default_factory=uuid4)
    status: EventCallbackResultStatus
    event_callback_id: ThinksoftUUID
    event_id: EventID
    conversation_id: ThinksoftUUID
    detail: str | None = None
    created_at: datetime = Field(default_factory=utc_now)


class EventCallbackResultPage(BaseModel):
    items: list[EventCallbackResult]
    next_page_id: str | None = None
