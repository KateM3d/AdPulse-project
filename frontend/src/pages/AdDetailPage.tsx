import { Link, useParams } from "react-router-dom";

import { AdComments } from "../components/AdComments/AdComments";
import { CampaignTimeline } from "../components/CampaignTimeline/CampaignTimeline";
import { MetricCard } from "../components/MetricCard/MetricCard";
import { PlatformBreakdown } from "../components/PlatformBreakdown/PlatformBreakdown";
import { useAd } from "../hooks/useAd";
import { formatNumber, formatPercentage } from "../utils/formatters";

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
        <Link to="/" className="ad-detail-page__back">
          ← Back to campaign
        </Link>

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
      <Link to="/" className="ad-detail-page__back">
        ← Back to campaign
      </Link>

      <header className="ad-detail-page__header">
        <span className="ad-detail-page__eyebrow">Ad performance</span>

        <h1>{ad.title}</h1>

        <p>Review creative performance, platform results, and audience feedback.</p>
      </header>

      <section className="ad-detail-page__overview">
        <div className="ad-detail-page__creative">
          <img src={`/ads/${ad.image}`} alt={`${ad.title} creative`} />
        </div>

        <div className="ad-detail-page__overview-content">
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

            <MetricCard label="CTR" value={formatPercentage(ad.ctr)} />

            <MetricCard
              label="Engagement rate"
              value={formatPercentage(ad.engagement_rate)}
            />
          </div>

          <article className="ad-detail-page__copy">
            <span className="ad-detail-page__section-label">Ad copy</span>

            <h2>{ad.title}</h2>

            <p>{ad.body}</p>
          </article>
        </div>
      </section>

      <section className="ad-detail-page__analytics">
        <CampaignTimeline
          timeline={ad.timeline}
          title="Ad performance over time"
        />

        <PlatformBreakdown
          platforms={ad.platforms}
          title="Performance by platform"
        />
      </section>

      <AdComments comments={ad.comments} />
    </main>
  );
};
