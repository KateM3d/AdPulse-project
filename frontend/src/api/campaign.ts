import type { CampaignResponse } from "../types/api";
import { apiClient } from "./client";

export const getCampaign = (): Promise<CampaignResponse> => {
  return apiClient<CampaignResponse>("/campaign");
};
