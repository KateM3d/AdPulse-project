import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";

import type { AdSummary } from "../../types/api";
import { CampaignAds } from "./CampaignAds";

const ads: AdSummary[] = [
  {
    ad_id: "first-ad",
    title: "First Ad",
    image: "first.png",
    total_impressions: 100000,
    total_clicks: 1200,
    total_engagements: 2000,
    ctr: 1.2,
    engagement_rate: 2,
  },
  {
    ad_id: "second-ad",
    title: "Second Ad",
    image: "second.png",
    total_impressions: 150000,
    total_clicks: 2250,
    total_engagements: 3750,
    ctr: 1.5,
    engagement_rate: 2.5,
  },
];

describe("CampaignAds", () => {
  it("renders a metric card for each ad", () => {
    render(
      <MemoryRouter>
        <CampaignAds ads={ads} />
      </MemoryRouter>,
    );

    expect(
      screen.getByRole("heading", { name: "Campaign ads" }),
    ).toBeInTheDocument();

    expect(screen.getByRole("heading", { name: "First Ad" })).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "Second Ad" })).toBeInTheDocument();

    expect(screen.getByText("100,000")).toBeInTheDocument();
    expect(screen.getByText("1,200")).toBeInTheDocument();
    expect(screen.getByText("1.20%")).toBeInTheDocument();
    expect(screen.getAllByText("Engagement rate").length).toBeGreaterThan(0);

    expect(screen.queryByRole("img")).not.toBeInTheDocument();
  });

  it("links each card to the ad analysis page", () => {
    render(
      <MemoryRouter>
        <CampaignAds ads={ads} />
      </MemoryRouter>,
    );

    const links = screen.getAllByRole("link", {
      name: /view full analysis/i,
    });

    expect(links).toHaveLength(2);
    expect(links[0]).toHaveAttribute("href", "/ads/first-ad");
    expect(links[1]).toHaveAttribute("href", "/ads/second-ad");
  });

  it("shows an empty state when there are no campaign ads", () => {
    render(
      <MemoryRouter>
        <CampaignAds ads={[]} />
      </MemoryRouter>,
    );

    expect(
      screen.getByText("No campaign ads available."),
    ).toBeInTheDocument();
  });
});
