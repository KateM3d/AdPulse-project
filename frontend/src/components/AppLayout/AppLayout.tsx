import type { PropsWithChildren } from "react";
import { Link, useLocation } from "react-router-dom";

import { LogoMark } from "../Logo/Logo";

import "./AppLayout.scss";

export const AppLayout = ({ children }: PropsWithChildren) => {
  const { pathname } = useLocation();
  const isCampaignSection = pathname === "/" || pathname.startsWith("/ads/");

  return (
    <div className="app-layout">
      <a className="app-layout__skip-link" href="#main-content">
        Skip to content
      </a>

      <header className="app-layout__header">
        <div className="app-layout__header-inner">
          <Link className="app-layout__brand" to="/" aria-label="AdPulse home">
            <LogoMark />
            <span className="app-layout__brand-name">AdPulse</span>
          </Link>

          <nav className="app-layout__nav" aria-label="Primary">
            <Link
              className={`app-layout__nav-link${isCampaignSection ? " app-layout__nav-link--active" : ""}`}
              to="/"
              aria-current={isCampaignSection ? "page" : undefined}
            >
              Campaign
            </Link>
          </nav>

          <span
            className="app-layout__workspace"
            title="All campaigns, metrics, and comments in this workspace are fictional."
          >
            <span className="app-layout__workspace-dot" aria-hidden="true" />
            <span className="app-layout__workspace-full">
              Demo workspace · Tidewell (fictional)
            </span>
            <span className="app-layout__workspace-short" aria-hidden="true">
              Fictional data
            </span>
          </span>
        </div>
      </header>

      <div id="main-content" className="app-layout__content">
        {children}
      </div>

      <footer className="app-layout__footer">
        <p>
          AdPulse is an independent portfolio project. Tidewell and all campaign
          data shown here are fictional.
        </p>
      </footer>
    </div>
  );
};
