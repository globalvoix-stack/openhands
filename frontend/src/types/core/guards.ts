import { ThinksoftParsedEvent } from ".";
import {
  UserMessageAction,
  AssistantMessageAction,
  ThinksoftAction,
  SystemMessageAction,
  CommandAction,
  FinishAction,
  TaskTrackingAction,
} from "./actions";
import {
  AgentStateChangeObservation,
  CommandObservation,
  ErrorObservation,
  MCPObservation,
  ThinksoftObservation,
  TaskTrackingObservation,
} from "./observations";
import { StatusUpdate } from "./variances";

export const isThinksoftEvent = (
  event: unknown,
): event is ThinksoftParsedEvent =>
  typeof event === "object" &&
  event !== null &&
  "id" in event &&
  "source" in event &&
  "message" in event &&
  "timestamp" in event;

export const isThinksoftAction = (
  event: ThinksoftParsedEvent,
): event is ThinksoftAction => "action" in event;

export const isThinksoftObservation = (
  event: ThinksoftParsedEvent,
): event is ThinksoftObservation => "observation" in event;

export const isUserMessage = (
  event: ThinksoftParsedEvent,
): event is UserMessageAction =>
  isThinksoftAction(event) &&
  event.source === "user" &&
  event.action === "message";

export const isAssistantMessage = (
  event: ThinksoftParsedEvent,
): event is AssistantMessageAction =>
  isThinksoftAction(event) &&
  event.source === "agent" &&
  (event.action === "message" || event.action === "finish");

export const isErrorObservation = (
  event: ThinksoftParsedEvent,
): event is ErrorObservation =>
  isThinksoftObservation(event) && event.observation === "error";

export const isCommandAction = (
  event: ThinksoftParsedEvent,
): event is CommandAction => isThinksoftAction(event) && event.action === "run";

export const isAgentStateChangeObservation = (
  event: ThinksoftParsedEvent,
): event is AgentStateChangeObservation =>
  isThinksoftObservation(event) && event.observation === "agent_state_changed";

export const isCommandObservation = (
  event: ThinksoftParsedEvent,
): event is CommandObservation =>
  isThinksoftObservation(event) && event.observation === "run";

export const isFinishAction = (
  event: ThinksoftParsedEvent,
): event is FinishAction =>
  isThinksoftAction(event) && event.action === "finish";

export const isSystemMessage = (
  event: ThinksoftParsedEvent,
): event is SystemMessageAction =>
  isThinksoftAction(event) && event.action === "system";

export const isRejectObservation = (
  event: ThinksoftParsedEvent,
): event is ThinksoftObservation =>
  isThinksoftObservation(event) && event.observation === "user_rejected";

export const isMcpObservation = (
  event: ThinksoftParsedEvent,
): event is MCPObservation =>
  isThinksoftObservation(event) && event.observation === "mcp";

export const isTaskTrackingAction = (
  event: ThinksoftParsedEvent,
): event is TaskTrackingAction =>
  isThinksoftAction(event) && event.action === "task_tracking";

export const isTaskTrackingObservation = (
  event: ThinksoftParsedEvent,
): event is TaskTrackingObservation =>
  isThinksoftObservation(event) && event.observation === "task_tracking";

export const isStatusUpdate = (event: unknown): event is StatusUpdate =>
  typeof event === "object" &&
  event !== null &&
  "status_update" in event &&
  "type" in event &&
  "id" in event;

export const isActionOrObservation = (
  event: ThinksoftParsedEvent,
): event is ThinksoftAction | ThinksoftObservation =>
  isThinksoftAction(event) || isThinksoftObservation(event);
