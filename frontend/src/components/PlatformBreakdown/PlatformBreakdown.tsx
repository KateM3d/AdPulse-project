import type { PlatformSummary } from "../../types/api";
import { formatNumber, formatPercentage } from "../../utils/formatters";

import "./PlatformBreakdown.scss";

interface PlatformBreakdownProps {
  platforms: PlatformSummary[];
  title?: string;
}

export const PlatformBreakdown = ({
  platforms,
  title = "Platform breakdown",
}: PlatformBreakdownProps) => (
  <section className="platform-breakdown">
    <div className="platform-breakdown__header">
      <div>
        <span className="platform-breakdown__eyebrow">Channel performance</span>
        <h2>{title}</h2>
      </div>
    </div>

    <div className="platform-breakdown__grid">
      {platforms.map((platform) => (
        <article key={platform.platform} className="platform-breakdown__card">
          <h3>{platform.platform}</h3>

          <dl>
            <div>
              <dt>Impressions</dt>
              <dd>{formatNumber(platform.impressions)}</dd>
            </div>

            <div>
              <dt>Clicks</dt>
              <dd>{formatNumber(platform.clicks)}</dd>
            </div>

            <div>
              <dt>Engagements</dt>
              <dd>{formatNumber(platform.engagements)}</dd>
            </div>

            <div>
              <dt>CTR</dt>
              <dd>{formatPercentage(platform.ctr)}</dd>
            </div>

            <div>
              <dt>Engagement rate</dt>
              <dd>{formatPercentage(platform.engagement_rate)}</dd>
            </div>
          </dl>
        </article>
      ))}
    </div>
  </section>
);
