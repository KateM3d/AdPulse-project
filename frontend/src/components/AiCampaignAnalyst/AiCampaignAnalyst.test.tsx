import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";

import type { AdInsights } from "../../types/api";
import { AiCampaignAnalyst } from "./AiCampaignAnalyst";

const insight = {
  summary: "The ad performs above the campaign benchmark.",
  strengths: ["CTR is above the campaign benchmark."],
  risks: ["Meta CTR is below the campaign benchmark."],
  recommended_next_experiment: "Test clearer ad copy on Meta.",
  hypothesis: "Clearer copy will improve Meta CTR.",
  metrics_to_measure: ["CTR on Meta", "Engagement rate on Meta"],
  provider: "demo",
  model: null,
} satisfies AdInsights;

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
      screen.getByRole("button", { name: "Generate insights" }),
    ).toBeInTheDocument();
  });

  it("labels demo mode before anything is generated", () => {
    render(
      <AiCampaignAnalyst
        providerStatus={{ provider: "demo", is_live: false, model: null }}
        isPending={false}
        isError={false}
        onGenerate={() => undefined}
      />,
    );

    expect(screen.getByText("Demo AI · Sample insights")).toBeInTheDocument();
    expect(
      screen.getByText(/no AI model or API key is involved/i),
    ).toBeInTheDocument();
  });

  it("labels live AI with the configured model", () => {
    render(
      <AiCampaignAnalyst
        providerStatus={{ provider: "openai", is_live: true, model: "gpt-4o-mini" }}
        isPending={false}
        isError={false}
        onGenerate={() => undefined}
      />,
    );

    expect(screen.getByText("Live AI · gpt-4o-mini")).toBeInTheDocument();
    expect(screen.queryByText(/Demo AI/)).not.toBeInTheDocument();
  });

  it("prefers the provider reported by the generated insight", () => {
    render(
      <AiCampaignAnalyst
        insight={insight}
        providerStatus={{ provider: "openai", is_live: true, model: "gpt-4o-mini" }}
        isPending={false}
        isError={false}
        onGenerate={() => undefined}
      />,
    );

    expect(screen.getByText("Demo AI · Sample insights")).toBeInTheDocument();
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

    await user.click(screen.getByRole("button", { name: "Generate insights" }));

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
      screen.getByRole("button", { name: "Generating insights…" }),
    ).toBeDisabled();
    expect(screen.getByRole("status")).toHaveTextContent(
      "Analyzing campaign performance and audience signals…",
    );
  });

  it("shows regenerate and a success message when an insight exists", () => {
    render(
      <AiCampaignAnalyst
        insight={insight}
        isPending={false}
        isError={false}
        onGenerate={() => undefined}
      />,
    );

    expect(
      screen.getByRole("button", { name: "Regenerate insights" }),
    ).toBeInTheDocument();
    expect(screen.getByText("Insights are ready below.")).toBeInTheDocument();
    expect(
      screen.queryByText(/Generate an evidence-based analysis/i),
    ).not.toBeInTheDocument();
  });

  it("shows the server error message when generation fails", () => {
    render(
      <AiCampaignAnalyst
        isPending={false}
        isError={true}
        errorMessage="Live AI insights are temporarily unavailable"
        onGenerate={() => undefined}
      />,
    );

    expect(screen.getByRole("alert")).toHaveTextContent(
      "Insights are temporarily unavailable.",
    );
    expect(
      screen.getByText("Live AI insights are temporarily unavailable"),
    ).toBeInTheDocument();
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
      screen.getByText("Unable to refresh insights. Showing the previous result."),
    ).toBeInTheDocument();
  });
});
