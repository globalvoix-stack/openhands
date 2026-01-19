import { ThinksoftAction } from "#/types/core/actions";
import { ThinksoftEventType } from "#/types/core/base";
import {
  isCommandAction,
  isCommandObservation,
  isThinksoftAction,
  isThinksoftObservation,
} from "#/types/core/guards";
import { ThinksoftObservation } from "#/types/core/observations";

const COMMON_NO_RENDER_LIST: ThinksoftEventType[] = [
  "system",
  "agent_state_changed",
  "change_agent_state",
];

const ACTION_NO_RENDER_LIST: ThinksoftEventType[] = ["recall"];

const OBSERVATION_NO_RENDER_LIST: ThinksoftEventType[] = ["think"];

export const shouldRenderEvent = (
  event: ThinksoftAction | ThinksoftObservation,
) => {
  if (isThinksoftAction(event)) {
    if (isCommandAction(event) && event.source === "user") {
      // For user commands, we always hide them from the chat interface
      return false;
    }

    const noRenderList = COMMON_NO_RENDER_LIST.concat(ACTION_NO_RENDER_LIST);
    return !noRenderList.includes(event.action);
  }

  if (isThinksoftObservation(event)) {
    if (isCommandObservation(event) && event.source === "user") {
      // For user commands, we always hide them from the chat interface
      return false;
    }

    const noRenderList = COMMON_NO_RENDER_LIST.concat(
      OBSERVATION_NO_RENDER_LIST,
    );
    return !noRenderList.includes(event.observation);
  }

  return true;
};

export const hasUserEvent = (
  events: (ThinksoftAction | ThinksoftObservation)[],
) =>
  events.some((event) => isThinksoftAction(event) && event.source === "user");
