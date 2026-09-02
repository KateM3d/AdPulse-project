import { Link, useParams } from "react-router-dom";

import { AdComments } from "../components/AdComments/AdComments";
import { AdNavigation } from "../components/AdNavigation/AdNavigation";
import { CampaignTimeline } from "../components/CampaignTimeline/CampaignTimeline";
import { MetricCard } from "../components/MetricCard/MetricCard";
import { PlatformBreakdown } from "../components/PlatformBreakdown/PlatformBreakdown";
import { useAd } from "../hooks/useAd";
import { formatNumber, formatPercentage } from "../utils/formatters";
import { CTR_TOOLTIP, ENGAGEMENT_RATE_TOOLTIP } from "../utils/metricTooltips";

import "./AdDetailPage.scss";

export const AdDetailPage = () => {
  const { adId = "" } = useParams();
  const adQuery = useAd(adId);

  if (adQuery.isPending) {
    return (
      <main className="ad-detail-page">
        <p>Loading ad details...</p>
      </main>
    );
  }

  if (adQuery.isError) {
    return (
      <main className="ad-detail-page">
        <div className="ad-detail-page__navigation">
          <Link to="/" className="ad-detail-page__back">
            <span aria-hidden="true">←</span>
            Back to campaign
          </Link>
        </div>

        <h1>Unable to load ad</h1>

        <p role="alert">
          {adQuery.error instanceof Error
            ? adQuery.error.message
            : "Unable to load ad details"}
        </p>
      </main>
    );
  }

  const ad = adQuery.data;

  return (
    <main className="ad-detail-page">
      <header className="ad-detail-page__header">
        <div className="ad-detail-page__navigation">
          <Link className="ad-detail-page__back" to="/">
            <span aria-hidden="true">←</span>
            Back to campaign
          </Link>

          <AdNavigation currentAdId={ad.ad_id} />
        </div>

        <div className="ad-detail-page__heading">
          <h1>{ad.title}</h1>
          <p>{ad.body}</p>
        </div>
      </header>

      <section className="ad-detail-page__overview">
        <div className="ad-detail-page__creative">
          <img src={`/ads/${ad.image}`} alt={`${ad.title} creative`} />
        </div>

        <section className="ad-detail-page__performance">
          <h2>Performance</h2>

          <div className="ad-detail-page__metrics">
            <MetricCard
              label="Impressions"
              value={formatNumber(ad.total_impressions)}
            />

            <MetricCard label="Clicks" value={formatNumber(ad.total_clicks)} />

            <MetricCard
              label="Engagements"
              value={formatNumber(ad.total_engagements)}
            />

            <MetricCard
              label="CTR"
              value={formatPercentage(ad.ctr)}
              tooltip={CTR_TOOLTIP}
            />

            <MetricCard
              label="Engagement rate"
              value={formatPercentage(ad.engagement_rate)}
              tooltip={ENGAGEMENT_RATE_TOOLTIP}
            />
          </div>
        </section>
      </section>

      <section className="ad-detail-page__analytics">
        <CampaignTimeline timeline={ad.timeline} />

        <PlatformBreakdown platforms={ad.platforms} />
      </section>

      <AdComments comments={ad.comments} />
    </main>
  );
};
