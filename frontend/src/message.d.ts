import { ThinksoftObservation } from "./types/core/observations";
import { ThinksoftAction } from "./types/core/actions";

export type Message = {
  sender: "user" | "assistant";
  content: string;
  timestamp: string;
  imageUrls?: string[];
  type?: "thought" | "error" | "action";
  success?: boolean;
  pending?: boolean;
  translationID?: string;
  eventID?: number;
  observation?: { payload: ThinksoftObservation };
  action?: { payload: ThinksoftAction };
};
