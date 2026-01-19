import React from "react";
import { ThinksoftAction } from "#/types/core/actions";
import { ThinksoftObservation } from "#/types/core/observations";
import { isErrorObservation } from "#/types/core/guards";
import { LikertScale } from "../../feedback/likert-scale";

interface LikertScaleWrapperProps {
  event: ThinksoftAction | ThinksoftObservation;
  isLastMessage: boolean;
  isInLast10Actions: boolean;
  config?: { APP_MODE?: string } | null;
  isCheckingFeedback: boolean;
  feedbackData: {
    exists: boolean;
    rating?: number;
    reason?: string;
  };
}

export function LikertScaleWrapper({
  event,
  isLastMessage,
  isInLast10Actions,
  config,
  isCheckingFeedback,
  feedbackData,
}: LikertScaleWrapperProps) {
  if (config?.APP_MODE !== "saas" || isCheckingFeedback) {
    return null;
  }

  // For error observations, show if in last 10 actions
  // For other events, show only if it's the last message
  const shouldShow = isErrorObservation(event)
    ? isInLast10Actions
    : isLastMessage;

  if (!shouldShow) {
    return null;
  }

  return (
    <LikertScale
      eventId={event.id}
      initiallySubmitted={feedbackData.exists}
      initialRating={feedbackData.rating}
      initialReason={feedbackData.reason}
    />
  );
}
