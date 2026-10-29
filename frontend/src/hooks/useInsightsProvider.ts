import { useQuery } from "@tanstack/react-query";

import { getInsightsProvider } from "../api/insights";

export const useInsightsProvider = () => {
  return useQuery({
    queryKey: ["insights-provider"],
    queryFn: getInsightsProvider,
    staleTime: Infinity,
    retry: false,
  });
};
