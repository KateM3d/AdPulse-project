import { Link } from "react-router-dom";

import type { AdSummary } from "../../types/api";
import { formatNumber, formatPercentage } from "../../utils/formatters";
import {
  CTR_TOOLTIP,
  ENGAGEMENT_RATE_TOOLTIP,
} from "../../utils/metricTooltips";
import { MetricTooltip } from "../MetricTooltip/MetricTooltip";

import "./CampaignAds.scss";

interface CampaignAdsProps {
  ads: AdSummary[];
}

export const CampaignAds = ({ ads }: CampaignAdsProps) => (
  <section className="campaign-ads">
    <header className="campaign-ads__header">
      <h2>Campaign ads</h2>
      <p>Compare individual creatives and open a full performance analysis.</p>
    </header>

    {ads.length === 0 ? (
      <div className="campaign-ads__empty">
        <p>No campaign ads available.</p>
      </div>
    ) : (
      <div className="campaign-ads__grid">
        {ads.map((ad) => (
          <article key={ad.ad_id} className="campaign-ads__card">
            <div className="campaign-ads__content">
              <h3 className="campaign-ads__title">{ad.title}</h3>

              <dl className="campaign-ads__metrics">
                <div className="campaign-ads__metric">
                  <dt>Impressions</dt>
                  <dd>{formatNumber(ad.total_impressions)}</dd>
                </div>

                <div className="campaign-ads__metric">
                  <dt>Clicks</dt>
                  <dd>{formatNumber(ad.total_clicks)}</dd>
                </div>

                <div className="campaign-ads__metric">
                  <dt className="metric-label">
                    CTR
                    <MetricTooltip label="CTR" text={CTR_TOOLTIP} />
                  </dt>
                  <dd>{formatPercentage(ad.ctr)}</dd>
                </div>

                <div className="campaign-ads__metric">
                  <dt className="metric-label">
                    Engagement rate
                    <MetricTooltip
                      label="Engagement rate"
                      text={ENGAGEMENT_RATE_TOOLTIP}
                    />
                  </dt>
                  <dd>{formatPercentage(ad.engagement_rate)}</dd>
                </div>
              </dl>

              <Link className="campaign-ads__button" to={`/ads/${ad.ad_id}`}>
                View full analysis
                <span aria-hidden="true">→</span>
              </Link>
            </div>
          </article>
        ))}
      </div>
    )}
  </section>
);
