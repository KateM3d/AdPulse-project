import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { beforeEach, describe, expect, it, vi } from "vitest";

import { getAds } from "../../api/ads";
import type { AdSummary } from "../../types/api";
import { AdNavigation } from "./AdNavigation";

vi.mock("../../api/ads", () => ({
  getAds: vi.fn(),
}));

const mockedGetAds = vi.mocked(getAds);

const ads = [
  {
    ad_id: "first-ad",
    title: "First Ad",
    image: "first.png",
    total_impressions: 1000,
    total_clicks: 10,
    total_engagements: 20,
    ctr: 1,
    engagement_rate: 2,
  },
  {
    ad_id: "middle-ad",
    title: "Middle Ad",
    image: "middle.png",
    total_impressions: 2000,
    total_clicks: 20,
    total_engagements: 40,
    ctr: 1,
    engagement_rate: 2,
  },
  {
    ad_id: "last-ad",
    title: "Last Ad",
    image: "last.png",
    total_impressions: 3000,
    total_clicks: 30,
    total_engagements: 60,
    ctr: 1,
    engagement_rate: 2,
  },
] satisfies AdSummary[];

const renderNavigation = (currentAdId: string) => {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: {
        retry: false,
      },
    },
  });

  return render(
    <QueryClientProvider client={queryClient}>
      <MemoryRouter>
        <AdNavigation currentAdId={currentAdId} />
      </MemoryRouter>
    </QueryClientProvider>,
  );
};

describe("AdNavigation", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    mockedGetAds.mockResolvedValue(ads);
  });

  it("links to the previous and next ads", async () => {
    renderNavigation("middle-ad");

    expect(await screen.findByRole("link", { name: "Previous" })).toHaveAttribute(
      "href",
      "/ads/first-ad",
    );
    expect(screen.getByRole("link", { name: "Next" })).toHaveAttribute(
      "href",
      "/ads/last-ad",
    );
  });

  it("disables previous on the first ad", async () => {
    renderNavigation("first-ad");

    expect(await screen.findByText("Previous")).toHaveAttribute(
      "aria-disabled",
      "true",
    );
    expect(screen.queryByRole("link", { name: "Previous" })).not.toBeInTheDocument();
    expect(screen.getByRole("link", { name: "Next" })).toHaveAttribute(
      "href",
      "/ads/middle-ad",
    );
  });

  it("disables next on the last ad", async () => {
    renderNavigation("last-ad");

    expect(await screen.findByRole("link", { name: "Previous" })).toHaveAttribute(
      "href",
      "/ads/middle-ad",
    );
    expect(screen.getByText("Next")).toHaveAttribute("aria-disabled", "true");
    expect(screen.queryByRole("link", { name: "Next" })).not.toBeInTheDocument();
  });
});
