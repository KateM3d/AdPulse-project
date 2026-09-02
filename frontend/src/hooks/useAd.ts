import { useQuery } from "@tanstack/react-query";

import { getAd } from "../api/ads";

export const useAd = (adId: string) =>
  useQuery({
    queryKey: ["ads", adId],
    queryFn: () => getAd(adId),
    enabled: Boolean(adId),
  });
