import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { vi } from "vitest";

import { getAds } from "../api/ads";
import { getCampaign } from "../api/campaign";
import { CampaignPage } from "./CampaignPage";

vi.mock("../api/ads", () => ({
  getAds: vi.fn(),
}));

vi.mock("../api/campaign", () => ({
  getCampaign: vi.fn(),
}));

const mockedGetAds = vi.mocked(getAds);
const mockedGetCampaign = vi.mocked(getCampaign);

describe("CampaignPage", () => {
  it("renders campaign metrics", async () => {
    mockedGetCampaign.mockResolvedValue({
      summary: {
        total_impressions: 1281840,
        total_clicks: 15220,
        total_engagements: 24666,
        ctr: 1.1874,
        engagement_rate: 1.9243,
        start_date: "2026-03-02",
        end_date: "2026-05-04",
      },
      timeline: [],
      platforms: [],
    });

    mockedGetAds.mockResolvedValue([]);

    const queryClient = new QueryClient({
      defaultOptions: {
        queries: {
          retry: false,
        },
      },
    });

    render(
      <QueryClientProvider client={queryClient}>
        <MemoryRouter>
          <CampaignPage />
        </MemoryRouter>
      </QueryClientProvider>,
    );

    expect(
      await screen.findByRole("heading", {
        name: "Campaign Performance",
      }),
    ).toBeInTheDocument();

    expect(screen.getByText("Impressions")).toBeInTheDocument();
    expect(screen.getByText("1,281,840")).toBeInTheDocument();
  });
});
