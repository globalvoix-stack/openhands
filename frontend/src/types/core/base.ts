export type ThinksoftEventType =
  | "message"
  | "system"
  | "agent_state_changed"
  | "change_agent_state"
  | "run"
  | "read"
  | "write"
  | "edit"
  | "run_ipython"
  | "delegate"
  | "browse"
  | "browse_interactive"
  | "reject"
  | "think"
  | "finish"
  | "error"
  | "recall"
  | "mcp"
  | "call_tool_mcp"
  | "task_tracking"
  | "user_rejected";

export type ThinksoftSourceType = "agent" | "user" | "environment";

interface ThinksoftBaseEvent {
  id: number;
  source: ThinksoftSourceType;
  message: string;
  timestamp: string; // ISO 8601
}

export interface ThinksoftActionEvent<
  T extends ThinksoftEventType,
> extends ThinksoftBaseEvent {
  action: T;
  args: Record<string, unknown>;
}

export interface ThinksoftObservationEvent<
  T extends ThinksoftEventType,
> extends ThinksoftBaseEvent {
  cause: number;
  observation: T;
  content: string;
  extras: Record<string, unknown>;
}
