import { Link, useParams } from "react-router-dom";

import { AdComments } from "../components/AdComments/AdComments";
import { AdNavigation } from "../components/AdNavigation/AdNavigation";
import { AiCampaignAnalyst } from "../components/AiCampaignAnalyst/AiCampaignAnalyst";
import { AiCampaignInsight } from "../components/AiCampaignInsight/AiCampaignInsight";
import { CampaignTimeline } from "../components/CampaignTimeline/CampaignTimeline";
import { MetricCard } from "../components/MetricCard/MetricCard";
import { PageError, PageLoading } from "../components/PageState/PageState";
import { PlatformBreakdown } from "../components/PlatformBreakdown/PlatformBreakdown";
import { useAd } from "../hooks/useAd";
import { useAdInsights } from "../hooks/useAdInsights";
import { useInsightsProvider } from "../hooks/useInsightsProvider";
import { formatNumber, formatPercentage } from "../utils/formatters";
import { CTR_TOOLTIP, ENGAGEMENT_RATE_TOOLTIP } from "../utils/metricTooltips";

import "./AdDetailPage.scss";

export const AdDetailPage = () => {
  const { adId = "" } = useParams();
  const adQuery = useAd(adId);
  const providerQuery = useInsightsProvider();
  const {
    data: aiInsight,
    error: aiError,
    isFetching: isAiPending,
    isError: isAiError,
    refetch: generateInsights,
  } = useAdInsights(adId);

  const visibleAiInsight = isAiPending ? undefined : aiInsight;

  if (adQuery.isPending) {
    return (
      <main className="ad-detail-page">
        <PageLoading label="Loading ad details..." />
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

        <PageError
          title="Unable to load ad"
          message={
            adQuery.error instanceof Error
              ? adQuery.error.message
              : "Unable to load ad details"
          }
          onRetry={() => {
            void adQuery.refetch();
          }}
        />
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

          <AiCampaignAnalyst
            insight={visibleAiInsight}
            providerStatus={providerQuery.data}
            isPending={isAiPending}
            isError={isAiError}
            errorMessage={aiError instanceof Error ? aiError.message : undefined}
            onGenerate={() => {
              void generateInsights();
            }}
          />
        </section>
      </section>

      {visibleAiInsight && <AiCampaignInsight insight={visibleAiInsight} />}

      <section className="ad-detail-page__analytics">
        <CampaignTimeline timeline={ad.timeline} />

        <PlatformBreakdown platforms={ad.platforms} />
      </section>

      <AdComments comments={ad.comments} />
    </main>
  );
};
