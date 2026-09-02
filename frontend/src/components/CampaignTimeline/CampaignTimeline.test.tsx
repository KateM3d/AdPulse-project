import { render, screen } from "@testing-library/react";

import type { TimelinePoint } from "../../types/api";
import { CampaignTimeline } from "./CampaignTimeline";

const timeline: TimelinePoint[] = [
  {
    date: "2026-03-02",
    impressions: 1000,
    clicks: 20,
    engagements: 30,
    ctr: 2,
    engagement_rate: 3,
  },
];

describe("CampaignTimeline", () => {
  it("renders the timeline heading", () => {
    render(<CampaignTimeline timeline={timeline} />);

    expect(
      screen.getByRole("heading", {
        name: "Performance over time",
      }),
    ).toBeInTheDocument();

    expect(screen.getByRole("heading", { name: "Reach" })).toBeInTheDocument();
    expect(
      screen.getByRole("heading", { name: "Efficiency" }),
    ).toBeInTheDocument();
  });

  it("renders a custom title", () => {
    render(
      <CampaignTimeline
        timeline={timeline}
        title="Ad performance over time"
      />,
    );

    expect(
      screen.getByRole("heading", {
        name: "Ad performance over time",
      }),
    ).toBeInTheDocument();
  });

  it("renders a zero-impression point without invalid rates", () => {
    render(
      <CampaignTimeline
        timeline={[
          {
            date: "2026-03-03",
            impressions: 0,
            clicks: 10,
            engagements: 10,
            ctr: 0,
            engagement_rate: 0,
          },
        ]}
      />,
    );

    expect(screen.getByRole("heading", { name: "Efficiency" })).toBeInTheDocument();
    expect(document.body.textContent).not.toMatch(/NaN|Infinity/);
  });
});
