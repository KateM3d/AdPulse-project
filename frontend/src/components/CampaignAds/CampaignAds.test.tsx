import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
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
  it("renders ad information", () => {
    render(
      <MemoryRouter>
        <CampaignAds ads={ads} />
      </MemoryRouter>,
    );

    expect(
      screen.getByRole("heading", {
        name: "First Ad",
      }),
    ).toBeInTheDocument();

    expect(screen.getByText("100,000 impressions")).toBeInTheDocument();
    expect(
      screen.getByRole("link", {
        name: /view full analysis/i,
      }),
    ).toHaveAttribute("href", "/ads/first-ad");
  });

  it("selects an ad and updates the preview", async () => {
    const user = userEvent.setup();

    render(
      <MemoryRouter>
        <CampaignAds ads={ads} />
      </MemoryRouter>,
    );

    const firstAd = screen.getByRole("button", {
      name: /first ad/i,
    });

    const secondAd = screen.getByRole("button", {
      name: /second ad/i,
    });

    expect(firstAd).toHaveAttribute("aria-pressed", "true");

    await user.click(secondAd);

    expect(secondAd).toHaveAttribute("aria-pressed", "true");
    expect(firstAd).toHaveAttribute("aria-pressed", "false");

    expect(
      screen.getByRole("img", {
        name: "Second Ad creative",
      }),
    ).toHaveAttribute("src", "/ads/second.png");

    expect(
      screen.getByRole("link", {
        name: /view full analysis/i,
      }),
    ).toHaveAttribute("href", "/ads/second-ad");
  });
});
