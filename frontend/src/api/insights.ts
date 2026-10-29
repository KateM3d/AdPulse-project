import type { AdInsights, InsightsProviderStatus } from "../types/api";
import { apiClient } from "./client";

export const generateAdInsights = async (adId: string): Promise<AdInsights> => {
  return apiClient<AdInsights>(`/ads/${adId}/insights`, {
    method: "POST",
  });
};

export const getInsightsProvider = async (): Promise<InsightsProviderStatus> => {
  return apiClient<InsightsProviderStatus>("/insights/provider");
};
