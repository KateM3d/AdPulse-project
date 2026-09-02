import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { render, screen, waitFor } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { beforeEach, describe, expect, it, vi } from "vitest";

import { getAd } from "../api/ads";
import type { AdDetail } from "../types/api";
import { AdDetailPage } from "./AdDetailPage";

vi.mock("../api/ads", () => ({
  getAd: vi.fn(),
}));

const mockedGetAd = vi.mocked(getAd);

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
  });

  it("provides navigation back to the campaign", async () => {
    mockedGetAd.mockResolvedValue(ad);

    renderPage();

    const backLink = await screen.findByRole("link", {
      name: /back to campaign/i,
    });

    expect(backLink).toHaveAttribute("href", "/");
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
