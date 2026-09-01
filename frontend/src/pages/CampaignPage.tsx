import { useCampaign } from "../hooks/useCampaign";

export const CampaignPage = () => {
  const { data, isPending, isError, error } = useCampaign();

  if (isPending) {
    return <main>Loading campaign data...</main>;
  }

  if (isError) {
    return (
      <main>
        <h1>Campaign Dashboard</h1>
        <p role="alert">
          {error instanceof Error
            ? error.message
            : "Unable to load campaign data"}
        </p>
      </main>
    );
  }

  return (
    <main>
      <h1>Campaign Dashboard</h1>

      <section>
        <h2>Overview</h2>

        <p>Impressions: {data.summary.total_impressions}</p>
        <p>Clicks: {data.summary.total_clicks}</p>
        <p>Engagements: {data.summary.total_engagements}</p>
        <p>CTR: {data.summary.ctr}%</p>
        <p>Engagement rate: {data.summary.engagement_rate}%</p>
      </section>
    </main>
  );
};
