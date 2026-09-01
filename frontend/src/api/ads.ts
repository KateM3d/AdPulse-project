import type { AdDetail, AdSummary } from "../types/api";
import { apiClient } from "./client";

export const getAds = (): Promise<AdSummary[]> => {
  return apiClient<AdSummary[]>("/ads");
};

export const getAd = (adId: string): Promise<AdDetail> => {
  return apiClient<AdDetail>(`/ads/${encodeURIComponent(adId)}`);
};
