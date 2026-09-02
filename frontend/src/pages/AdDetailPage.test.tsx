import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { render, screen, waitFor } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { beforeEach, describe, expect, it, vi } from "vitest";

import { getAd, getAds } from "../api/ads";
import type { AdDetail, AdSummary } from "../types/api";
import { AdDetailPage } from "./AdDetailPage";

vi.mock("../api/ads", () => ({
  getAd: vi.fn(),
  getAds: vi.fn(),
}));

const mockedGetAd = vi.mocked(getAd);
const mockedGetAds = vi.mocked(getAds);

const ad = {
  ad_id: "payroll_in_minutes",
  title: "Tidewell Payroll",
  body: "Run payroll for your whole team in about four minutes.",
  image: "payroll_in_minutes.png",

  total_impressions: 120000,
  total_clicks: 2400,
  total_engagements: 3600,
  ctr: 2,
  engagement_rate: 3,

  timeline: [
    {
      date: "2026-03-03",
      impressions: 60000,
      clicks: 1200,
      engagements: 1800,
      ctr: 2,
      engagement_rate: 3,
    },
    {
      date: "2026-04-03",
      impressions: 60000,
      clicks: 1200,
      engagements: 1800,
      ctr: 2,
      engagement_rate: 3,
    },
  ],

  platforms: [
    {
      platform: "LinkedIn",
      impressions: 120000,
      clicks: 2400,
      engagements: 3600,
      ctr: 2,
      engagement_rate: 3,
    },
  ],

  comments: [
    {
      date: "2026-03-17",
      platform: "LinkedIn",
      comment: "Great concept.",
    },
  ],
} satisfies AdDetail;

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
    ad_id: ad.ad_id,
    title: ad.title,
    image: ad.image,
    total_impressions: ad.total_impressions,
    total_clicks: ad.total_clicks,
    total_engagements: ad.total_engagements,
    ctr: ad.ctr,
    engagement_rate: ad.engagement_rate,
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

const renderPage = () => {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: {
        retry: false,
      },
    },
  });

  return render(
    <QueryClientProvider client={queryClient}>
      <MemoryRouter initialEntries={["/ads/payroll_in_minutes"]}>
        <Routes>
          <Route path="/ads/:adId" element={<AdDetailPage />} />
        </Routes>
      </MemoryRouter>
    </QueryClientProvider>,
  );
};

describe("AdDetailPage", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    mockedGetAds.mockResolvedValue(ads);
  });

  it("loads the requested ad", async () => {
    mockedGetAd.mockResolvedValue(ad);

    renderPage();

    expect(screen.getByText("Loading ad details...")).toBeInTheDocument();

    await waitFor(() => {
      expect(mockedGetAd).toHaveBeenCalledWith("payroll_in_minutes");
    });

    expect(
      await screen.findByRole("heading", {
        name: "Tidewell Payroll",
        level: 1,
      }),
    ).toBeInTheDocument();
  });

  it("renders the ad data", async () => {
    mockedGetAd.mockResolvedValue(ad);

    renderPage();

    expect(
      await screen.findByRole("heading", {
        name: "Tidewell Payroll",
        level: 1,
      }),
    ).toBeInTheDocument();

    expect(
      screen.getByAltText("Tidewell Payroll creative"),
    ).toHaveAttribute("src", "/ads/payroll_in_minutes.png");

    expect(
      screen.getByText(
        "Run payroll for your whole team in about four minutes.",
      ),
    ).toBeInTheDocument();

    expect(screen.getAllByText("120,000").length).toBeGreaterThan(0);
    expect(screen.getAllByText("2,400").length).toBeGreaterThan(0);
    expect(screen.getAllByText("3,600").length).toBeGreaterThan(0);

    expect(screen.getAllByText("2.00%").length).toBeGreaterThan(0);
    expect(screen.getAllByText("3.00%").length).toBeGreaterThan(0);

    expect(screen.getByText("Great concept.")).toBeInTheDocument();

    expect(screen.queryByText("Ad performance")).not.toBeInTheDocument();
    expect(screen.queryByText("Ad copy")).not.toBeInTheDocument();
    expect(
      screen.queryByText(
        "Review creative performance, platform results, and audience feedback.",
      ),
    ).not.toBeInTheDocument();

    expect(screen.getByRole("heading", { name: "Performance" })).toBeInTheDocument();
    expect(
      screen.getByRole("heading", { name: "Performance over time" }),
    ).toBeInTheDocument();
    expect(
      screen.getByRole("heading", { name: "Audience feedback" }),
    ).toBeInTheDocument();
    expect(screen.getByText("AI Campaign Analyst")).toBeInTheDocument();
    expect(
      screen.getByRole("button", { name: "Generate AI analysis" }),
    ).toBeInTheDocument();
  });

  it("provides navigation back to the campaign", async () => {
    mockedGetAd.mockResolvedValue(ad);

    renderPage();

    const backLink = await screen.findByRole("link", {
      name: /back to campaign/i,
    });

    expect(backLink).toHaveAttribute("href", "/");
  });

  it("links to the previous and next ads", async () => {
    mockedGetAd.mockResolvedValue(ad);

    renderPage();

    expect(await screen.findByRole("link", { name: "Previous" })).toHaveAttribute(
      "href",
      "/ads/first-ad",
    );
    expect(screen.getByRole("link", { name: "Next" })).toHaveAttribute(
      "href",
      "/ads/last-ad",
    );
  });

  it("renders an error state when the ad cannot be loaded", async () => {
    mockedGetAd.mockRejectedValue(new Error("Ad not found"));

    renderPage();

    expect(
      await screen.findByRole("heading", {
        name: "Unable to load ad",
      }),
    ).toBeInTheDocument();

    expect(screen.getByRole("alert")).toHaveTextContent("Ad not found");
  });
});
