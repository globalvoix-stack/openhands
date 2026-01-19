import { ThinksoftAction } from "./actions";
import { ThinksoftObservation } from "./observations";
import { ThinksoftVariance } from "./variances";

/**
 * @deprecated Will be removed once we fully transition to v1 events
 */
export type ThinksoftParsedEvent =
  | ThinksoftAction
  | ThinksoftObservation
  | ThinksoftVariance;
