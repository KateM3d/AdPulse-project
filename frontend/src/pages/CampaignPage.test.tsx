import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { render, screen } from "@testing-library/react";
import { vi } from "vitest";

import { getCampaign } from "../api/campaign";
import { CampaignPage } from "./CampaignPage";

vi.mock("../api/campaign", () => ({
  getCampaign: vi.fn(),
}));

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

    const queryClient = new QueryClient({
      defaultOptions: {
        queries: {
          retry: false,
        },
      },
    });

    render(
      <QueryClientProvider client={queryClient}>
        <CampaignPage />
      </QueryClientProvider>,
    );

    expect(
      await screen.findByRole("heading", {
        name: "Campaign Dashboard",
      }),
    ).toBeInTheDocument();

    expect(screen.getByText("Impressions: 1281840")).toBeInTheDocument();
  });
});
