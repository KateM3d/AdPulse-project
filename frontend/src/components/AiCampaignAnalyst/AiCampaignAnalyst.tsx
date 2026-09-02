import type { AiCampaignInsight } from "../../types/api";

import "./AiCampaignAnalyst.scss";

type AiCampaignAnalystProps = {
  insight?: AiCampaignInsight;
  isPending: boolean;
  isError: boolean;
  onGenerate: () => void;
};

export const AiCampaignAnalyst = ({
  insight,
  isPending,
  isError,
  onGenerate,
}: AiCampaignAnalystProps) => {
  return (
    <section className="ai-campaign-analyst">
      <div className="ai-campaign-analyst__header">
        <div>
          <p className="ai-campaign-analyst__eyebrow">AI Campaign Analyst</p>

          <h2>Turn performance into the next experiment</h2>
        </div>

        <button
          className="ai-campaign-analyst__button"
          type="button"
          onClick={onGenerate}
          disabled={isPending}
        >
          {isPending
            ? "Generating analysis…"
            : insight
              ? "Regenerate analysis"
              : "Generate AI analysis"}
        </button>
      </div>

      {!insight && !isPending && !isError && (
        <div className="ai-campaign-analyst__intro-card">
          <p>
            Generate an evidence-based analysis using this ad&apos;s
            performance, campaign benchmarks, and audience feedback.
          </p>
        </div>
      )}

      {isPending && (
        <div className="ai-campaign-analyst__intro-card">
          <p>Analyzing campaign performance and audience signals…</p>
        </div>
      )}

      {isError && (
        <div className="ai-campaign-analyst__intro-card">
          <p className="ai-campaign-analyst__error">
            {insight
              ? "Unable to refresh analysis. Showing the previous result."
              : "AI analysis is temporarily unavailable."}
          </p>
        </div>
      )}
    </section>
  );
};
