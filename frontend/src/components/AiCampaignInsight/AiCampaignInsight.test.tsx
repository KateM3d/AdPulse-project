import { render, screen } from "@testing-library/react";

import type { AiCampaignInsight as AiCampaignInsightData } from "../../types/api";
import { AiCampaignInsight } from "./AiCampaignInsight";

const insight = {
  summary: "The ad performs above the campaign benchmark.",
  strengths: ["CTR is above the campaign benchmark."],
  risks: ["Meta CTR is below the campaign benchmark."],
  recommended_next_experiment: "Test clearer ad copy on Meta.",
  hypothesis: "Clearer copy will improve Meta CTR.",
  metrics_to_measure: ["CTR on Meta", "Engagement rate on Meta"],
} satisfies AiCampaignInsightData;

describe("AiCampaignInsight", () => {
  it("renders summary, strengths, risks, and the recommended experiment", () => {
    render(<AiCampaignInsight insight={insight} />);

    expect(
      screen.getByText("The ad performs above the campaign benchmark."),
    ).toBeInTheDocument();
    expect(
      screen.getByText("CTR is above the campaign benchmark."),
    ).toBeInTheDocument();
    expect(
      screen.getByText("Meta CTR is below the campaign benchmark."),
    ).toBeInTheDocument();
    expect(
      screen.getByText("Test clearer ad copy on Meta."),
    ).toBeInTheDocument();
    expect(
      screen.getByText("Clearer copy will improve Meta CTR."),
    ).toBeInTheDocument();
    expect(screen.getByText("CTR on Meta")).toBeInTheDocument();
    expect(screen.getByText("Engagement rate on Meta")).toBeInTheDocument();
  });
});
