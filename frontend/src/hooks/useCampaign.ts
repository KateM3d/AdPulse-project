import { useQuery } from "@tanstack/react-query";

import { getCampaign } from "../api/campaign";

export const useCampaign = () => {
  return useQuery({
    queryKey: ["campaign"],
    queryFn: getCampaign,
  });
};
