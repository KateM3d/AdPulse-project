import type { AdInsights, InsightsProviderStatus } from "../../types/api";
import { ProviderBadge } from "../ProviderBadge/ProviderBadge";

import "./AiCampaignAnalyst.scss";

type AiCampaignAnalystProps = {
  insight?: AdInsights;
  providerStatus?: InsightsProviderStatus;
  isPending: boolean;
  isError: boolean;
  errorMessage?: string;
  onGenerate: () => void;
};

const introText = (status?: InsightsProviderStatus) => {
  if (status?.provider === "demo") {
    return "Generate sample insights from this ad's performance, campaign benchmarks, and audience feedback. Demo mode uses deterministic rules, so no AI model or API key is involved.";
  }

  if (status?.provider === "openai") {
    return `Generate an evidence-based analysis with ${status.model ?? "a live language model"}, using this ad's performance, campaign benchmarks, and audience feedback.`;
  }

  return "Generate an evidence-based analysis using this ad's performance, campaign benchmarks, and audience feedback.";
};

export const AiCampaignAnalyst = ({
  insight,
  providerStatus,
  isPending,
  isError,
  errorMessage,
  onGenerate,
}: AiCampaignAnalystProps) => {
  const provider = insight?.provider ?? providerStatus?.provider;
  const model = insight?.model ?? providerStatus?.model;

  return (
    <section className="ai-campaign-analyst" aria-labelledby="ai-analyst-heading">
      <div className="ai-campaign-analyst__header">
        <div>
          <div className="ai-campaign-analyst__eyebrow-row">
            <p className="ai-campaign-analyst__eyebrow">AI Campaign Analyst</p>
            {provider && <ProviderBadge provider={provider} model={model} />}
          </div>

          <h2 id="ai-analyst-heading">Turn performance into the next experiment</h2>
        </div>

        <button
          className="ai-campaign-analyst__button"
          type="button"
          onClick={onGenerate}
          disabled={isPending}
        >
          {isPending
            ? "Generating insights…"
            : insight
              ? "Regenerate insights"
              : "Generate insights"}
        </button>
      </div>

      {!insight && !isPending && !isError && (
        <div className="ai-campaign-analyst__intro-card">
          <p>{introText(providerStatus)}</p>
        </div>
      )}

      {isPending && (
        <div
          className="ai-campaign-analyst__intro-card ai-campaign-analyst__intro-card--pending"
          role="status"
        >
          <span className="ai-campaign-analyst__spinner" aria-hidden="true" />
          <p>Analyzing campaign performance and audience signals…</p>
        </div>
      )}

      {isError && !isPending && (
        <div className="ai-campaign-analyst__intro-card ai-campaign-analyst__intro-card--error">
          <p className="ai-campaign-analyst__error" role="alert">
            {insight
              ? "Unable to refresh insights. Showing the previous result."
              : "Insights are temporarily unavailable."}
          </p>
          {errorMessage && !insight && (
            <p className="ai-campaign-analyst__error-detail">{errorMessage}</p>
          )}
        </div>
      )}

      {insight && !isPending && !isError && (
        <div className="ai-campaign-analyst__intro-card ai-campaign-analyst__intro-card--success">
          <p>Insights are ready below.</p>
        </div>
      )}
    </section>
  );
};
