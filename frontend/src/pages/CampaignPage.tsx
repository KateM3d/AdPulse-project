import { CampaignAds } from "../components/CampaignAds/CampaignAds";
import { CampaignTimeline } from "../components/CampaignTimeline/CampaignTimeline";
import { MetricCard } from "../components/MetricCard/MetricCard";
import { PageError, PageLoading } from "../components/PageState/PageState";
import { PlatformBreakdown } from "../components/PlatformBreakdown/PlatformBreakdown";
import { useAds } from "../hooks/useAds";
import { useCampaign } from "../hooks/useCampaign";
import { formatDate, formatNumber, formatPercentage } from "../utils/formatters";
import { CTR_TOOLTIP, ENGAGEMENT_RATE_TOOLTIP } from "../utils/metricTooltips";

import "./CampaignPage.scss";

export const CampaignPage = () => {
  const campaignQuery = useCampaign();
  const adsQuery = useAds();

  if (campaignQuery.isPending || adsQuery.isPending) {
    return (
      <main className="campaign-page">
        <PageLoading label="Loading campaign data..." />
      </main>
    );
  }

  if (campaignQuery.isError || adsQuery.isError) {
    const error = campaignQuery.error ?? adsQuery.error;

    return (
      <main className="campaign-page">
        <PageError
          title="Unable to load campaign"
          message={
            error instanceof Error ? error.message : "Unable to load campaign data"
          }
          onRetry={() => {
            void campaignQuery.refetch();
            void adsQuery.refetch();
          }}
        />
      </main>
    );
  }

  const { summary, timeline, platforms } = campaignQuery.data;
  const ads = adsQuery.data;

  return (
    <main className="campaign-page">
      <header className="campaign-page__header">
        <div>
          <p className="campaign-page__eyebrow">Campaign overview</p>

          <h1>Campaign Performance</h1>

          <p className="campaign-page__subtitle">
            Track reach, engagement, and efficiency across channels, then dig
            into individual ads for recommended next experiments.
          </p>
        </div>

        {summary.start_date && summary.end_date && (
          <div className="campaign-page__date-range">
            {formatDate(summary.start_date)} — {formatDate(summary.end_date)}
          </div>
        )}
      </header>

      <section className="campaign-page__metrics" aria-label="Campaign metrics">
        <MetricCard
          label="Impressions"
          value={formatNumber(summary.total_impressions)}
        />

        <MetricCard label="Clicks" value={formatNumber(summary.total_clicks)} />

        <MetricCard
          label="Engagements"
          value={formatNumber(summary.total_engagements)}
        />

        <MetricCard
          label="CTR"
          value={formatPercentage(summary.ctr)}
          tooltip={CTR_TOOLTIP}
        />

        <MetricCard
          label="Engagement rate"
          value={formatPercentage(summary.engagement_rate)}
          tooltip={ENGAGEMENT_RATE_TOOLTIP}
        />
      </section>

      <CampaignTimeline timeline={timeline} />

      <PlatformBreakdown platforms={platforms} />

      <CampaignAds ads={ads} />
    </main>
  );
};
