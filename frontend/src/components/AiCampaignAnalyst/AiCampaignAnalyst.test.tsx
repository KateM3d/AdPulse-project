import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";

import type { AiCampaignInsight } from "../../types/api";
import { AiCampaignAnalyst } from "./AiCampaignAnalyst";

const insight = {
  summary: "The ad performs above the campaign benchmark.",
  strengths: ["CTR is above the campaign benchmark."],
  risks: ["Meta CTR is below the campaign benchmark."],
  recommended_next_experiment: "Test clearer ad copy on Meta.",
  hypothesis: "Clearer copy will improve Meta CTR.",
  metrics_to_measure: ["CTR on Meta", "Engagement rate on Meta"],
} satisfies AiCampaignInsight;

describe("AiCampaignAnalyst", () => {
  it("shows the initial generate CTA", () => {
    render(
      <AiCampaignAnalyst
        isPending={false}
        isError={false}
        onGenerate={() => undefined}
      />,
    );

    expect(screen.getByText("AI Campaign Analyst")).toBeInTheDocument();
    expect(
      screen.getByRole("heading", {
        name: "Turn performance into the next experiment",
      }),
    ).toBeInTheDocument();
    expect(
      screen.getByText(/Generate an evidence-based analysis/i),
    ).toBeInTheDocument();
    expect(
      screen.getByRole("button", { name: "Generate AI analysis" }),
    ).toBeInTheDocument();
  });

  it("calls onGenerate when the CTA is clicked", async () => {
    const user = userEvent.setup();
    const onGenerate = vi.fn();

    render(
      <AiCampaignAnalyst
        isPending={false}
        isError={false}
        onGenerate={onGenerate}
      />,
    );

    await user.click(
      screen.getByRole("button", { name: "Generate AI analysis" }),
    );

    expect(onGenerate).toHaveBeenCalledTimes(1);
  });

  it("disables the button while pending", () => {
    render(
      <AiCampaignAnalyst
        isPending={true}
        isError={false}
        onGenerate={() => undefined}
      />,
    );

    expect(
      screen.getByRole("button", { name: "Generating analysis…" }),
    ).toBeDisabled();
    expect(
      screen.getByText(
        "Analyzing campaign performance and audience signals…",
      ),
    ).toBeInTheDocument();
  });

  it("shows regenerate when an insight already exists", () => {
    render(
      <AiCampaignAnalyst
        insight={insight}
        isPending={false}
        isError={false}
        onGenerate={() => undefined}
      />,
    );

    expect(
      screen.getByRole("button", { name: "Regenerate analysis" }),
    ).toBeInTheDocument();
    expect(
      screen.queryByText(/Generate an evidence-based analysis/i),
    ).not.toBeInTheDocument();
  });

  it("keeps the previous insight messaging when a refresh fails", () => {
    render(
      <AiCampaignAnalyst
        insight={insight}
        isPending={false}
        isError={true}
        onGenerate={() => undefined}
      />,
    );

    expect(
      screen.getByText(
        "Unable to refresh analysis. Showing the previous result.",
      ),
    ).toBeInTheDocument();
  });
});
