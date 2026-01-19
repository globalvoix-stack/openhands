import { NavLink } from "react-router";
import { useTranslation } from "react-i18next";
import ThinksoftLogo from "#/assets/branding/thinksoft-logo.svg?react";
import { I18nKey } from "#/i18n/declaration";
import { StyledTooltip } from "#/components/shared/buttons/styled-tooltip";

export function ThinksoftLogoButton() {
  const { t } = useTranslation();

  const tooltipText = t(I18nKey.BRANDING$THINKSOFT);
  const ariaLabel = t(I18nKey.BRANDING$THINKSOFT_LOGO);

  return (
    <StyledTooltip content={tooltipText}>
      <NavLink to="/" aria-label={ariaLabel}>
        <ThinksoftLogo width={46} height={30} />
      </NavLink>
    </StyledTooltip>
  );
}
