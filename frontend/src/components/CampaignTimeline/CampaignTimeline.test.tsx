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
    render(<CampaignTimeline data={timeline} />);

    expect(
      screen.getByRole("heading", {
        name: "Campaign timeline",
      }),
    ).toBeInTheDocument();
  });
});
