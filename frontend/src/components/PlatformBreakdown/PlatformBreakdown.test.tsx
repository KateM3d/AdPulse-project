import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";

import type { PlatformSummary } from "../../types/api";
import { PlatformBreakdown } from "./PlatformBreakdown";

const platforms = [
  {
    platform: "Google",
    impressions: 100_000,
    clicks: 1_200,
    engagements: 1_800,
    ctr: 1.2,
    engagement_rate: 1.8,
  },
  {
    platform: "LinkedIn",
    impressions: 80_000,
    clicks: 800,
    engagements: 1_280,
    ctr: 1,
    engagement_rate: 1.6,
  },
  {
    platform: "Meta",
    impressions: 120_000,
    clicks: 1_560,
    engagements: 2_280,
    ctr: 1.3,
    engagement_rate: 1.9,
  },
] satisfies PlatformSummary[];

describe("PlatformBreakdown", () => {
  it("defaults to CTR", () => {
    render(<PlatformBreakdown platforms={platforms} />);

    expect(
      screen.getByRole("combobox", {
        name: /platform comparison metric/i,
      }),
    ).toHaveValue("ctr");
  });

  it("allows the comparison metric to be changed", async () => {
    const user = userEvent.setup();

    render(<PlatformBreakdown platforms={platforms} />);

    const select = screen.getByRole("combobox", {
      name: /platform comparison metric/i,
    });

    await user.selectOptions(select, "engagement_rate");

    expect(select).toHaveValue("engagement_rate");
  });

  it("renders a custom title", () => {
    render(
      <PlatformBreakdown
        platforms={platforms}
        title="Ad performance by platform"
      />,
    );

    expect(
      screen.getByRole("heading", {
        name: "Ad performance by platform",
      }),
    ).toBeInTheDocument();
  });
});
