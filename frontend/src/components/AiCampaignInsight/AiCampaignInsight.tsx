import type { AiCampaignInsight as AiCampaignInsightData } from "../../types/api";

import "./AiCampaignInsight.scss";

type AiCampaignInsightProps = {
  insight: AiCampaignInsightData;
};

export const AiCampaignInsight = ({ insight }: AiCampaignInsightProps) => {
  return (
    <section className="ai-campaign-insight" aria-label="AI campaign insight">
      <div className="ai-campaign-insight__card">
        <p className="ai-campaign-insight__label">Performance summary</p>
        <p>{insight.summary}</p>
      </div>

      <div className="ai-campaign-insight__columns">
        <div className="ai-campaign-insight__card">
          <p className="ai-campaign-insight__label">What&apos;s working</p>

          <ul>
            {insight.strengths.map((strength) => (
              <li key={strength}>{strength}</li>
            ))}
          </ul>
        </div>

        <div className="ai-campaign-insight__card">
          <p className="ai-campaign-insight__label">Watch</p>

          <ul>
            {insight.risks.map((risk) => (
              <li key={risk}>{risk}</li>
            ))}
          </ul>
        </div>
      </div>

      <div className="ai-campaign-insight__card ai-campaign-insight__experiment">
        <p className="ai-campaign-insight__label">
          Recommended next experiment
        </p>

        <p className="ai-campaign-insight__experiment-text">
          {insight.recommended_next_experiment}
        </p>

        <div className="ai-campaign-insight__experiment-grid">
          <div>
            <p className="ai-campaign-insight__label">Hypothesis</p>
            <p>{insight.hypothesis}</p>
          </div>

          <div>
            <p className="ai-campaign-insight__label">Measure</p>

            <ul>
              {insight.metrics_to_measure.map((metric) => (
                <li key={metric}>{metric}</li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    </section>
  );
};
