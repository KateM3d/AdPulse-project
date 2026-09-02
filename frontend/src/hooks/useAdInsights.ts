import { useQuery } from "@tanstack/react-query";

import { generateAdInsights } from "../api/insights";

export const useAdInsights = (adId: string) => {
  return useQuery({
    queryKey: ["ad-insights", adId],
    queryFn: () => generateAdInsights(adId),
    enabled: false,
    retry: false,
    staleTime: Infinity,
  });
};
