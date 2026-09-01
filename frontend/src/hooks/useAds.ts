import { useQuery } from "@tanstack/react-query";

import { getAds } from "../api/ads";

export const useAds = () =>
  useQuery({
    queryKey: ["ads"],
    queryFn: getAds,
  });
