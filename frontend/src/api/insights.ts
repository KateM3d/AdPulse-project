import type { AiCampaignInsight } from "../types/api";
import { apiClient } from "./client";

export const generateAdInsights = async (
  adId: string,
): Promise<AiCampaignInsight> => {
  return apiClient<AiCampaignInsight>(`/ads/${adId}/insights`, {
    method: "POST",
  });
};
