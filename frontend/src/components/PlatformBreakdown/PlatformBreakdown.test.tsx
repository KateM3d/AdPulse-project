import { render, screen } from "@testing-library/react";

import type { PlatformSummary } from "../../types/api";
import { PlatformBreakdown } from "./PlatformBreakdown";

const platforms: PlatformSummary[] = [
  {
    platform: "Google",
    impressions: 120000,
    clicks: 1500,
    engagements: 2100,
    ctr: 1.25,
    engagement_rate: 1.75,
  },
  {
    platform: "Meta",
    impressions: 90000,
    clicks: 1800,
    engagements: 2500,
    ctr: 2,
    engagement_rate: 2.78,
  },
];

describe("PlatformBreakdown", () => {
  it("renders each platform", () => {
    render(<PlatformBreakdown platforms={platforms} />);

    expect(screen.getByRole("heading", { name: "Google" })).toBeInTheDocument();

    expect(screen.getByRole("heading", { name: "Meta" })).toBeInTheDocument();
  });

  it("renders formatted platform metrics", () => {
    render(<PlatformBreakdown platforms={platforms} />);

    expect(screen.getByText("120,000")).toBeInTheDocument();
    expect(screen.getByText("1.25%")).toBeInTheDocument();
    expect(screen.getByText("2.78%")).toBeInTheDocument();
  });
});
