import {
  CartesianGrid,
  Legend,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import type { TimelinePoint } from "../../types/api";
import { formatNumber, formatPercentage } from "../../utils/formatters";

import "./CampaignTimeline.scss";

interface CampaignTimelineProps {
  timeline: TimelinePoint[];
  title?: string;
  description?: string;
}

interface TimelineChartPoint extends TimelinePoint {
  engagementRate: number;
}

const formatAxisDate = (date: string) =>
  new Intl.DateTimeFormat("en-US", {
    month: "short",
    day: "numeric",
  }).format(new Date(`${date}T00:00:00`));

const getRate = (value: number, impressions: number) => {
  if (impressions === 0) {
    return 0;
  }

  return (value / impressions) * 100;
};

const axisTick = {
  fontSize: 14,
  fill: "#667174",
};

export const CampaignTimeline = ({
  timeline,
  title = "Performance over time",
  description = "See how campaign reach and efficiency changed over time.",
}: CampaignTimelineProps) => {
  const chartData: TimelineChartPoint[] = timeline.map((point) => ({
    ...point,
    ctr: getRate(point.clicks, point.impressions),
    engagementRate: getRate(point.engagements, point.impressions),
  }));

  return (
    <section className="campaign-timeline">
      <header className="campaign-timeline__header">
        <h2>{title}</h2>
        <p>{description}</p>
      </header>

      <div className="campaign-timeline__section">
        <div className="campaign-timeline__section-header">
          <h3>Reach</h3>
          <p>Impressions</p>
        </div>

        <div className="campaign-timeline__chart">
          <ResponsiveContainer width="100%" height={220}>
            <LineChart
              data={chartData}
              margin={{
                top: 8,
                right: 16,
                left: 0,
                bottom: 0,
              }}
            >
              <CartesianGrid
                stroke="#edf0f4"
                strokeDasharray="3 3"
                vertical={false}
              />

              <XAxis
                dataKey="date"
                tickFormatter={formatAxisDate}
                tick={axisTick}
                tickLine={false}
                axisLine={false}
                minTickGap={28}
              />

              <YAxis
                tickFormatter={(value: number) => formatNumber(value)}
                tick={axisTick}
                tickLine={false}
                axisLine={false}
                width={72}
              />

              <Tooltip
                labelFormatter={(label) => formatAxisDate(String(label))}
                formatter={(value) => [
                  formatNumber(Number(value)),
                  "Impressions",
                ]}
              />

              <Line
                type="monotone"
                dataKey="impressions"
                name="Impressions"
                stroke="#3154ff"
                strokeWidth={3}
                dot={false}
                activeDot={{ r: 5 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="campaign-timeline__divider" />

      <div className="campaign-timeline__section">
        <div className="campaign-timeline__section-header">
          <h3>Efficiency</h3>
          <p>CTR and engagement rate</p>
        </div>

        <div className="campaign-timeline__chart">
          <ResponsiveContainer width="100%" height={240}>
            <LineChart
              data={chartData}
              margin={{
                top: 8,
                right: 16,
                left: 0,
                bottom: 0,
              }}
            >
              <CartesianGrid
                stroke="#edf0f4"
                strokeDasharray="3 3"
                vertical={false}
              />

              <XAxis
                dataKey="date"
                tickFormatter={formatAxisDate}
                tick={axisTick}
                tickLine={false}
                axisLine={false}
                minTickGap={28}
              />

              <YAxis
                tickFormatter={(value: number) => `${value.toFixed(1)}%`}
                tick={axisTick}
                tickLine={false}
                axisLine={false}
                width={58}
              />

              <Tooltip
                labelFormatter={(label) => formatAxisDate(String(label))}
                formatter={(value, name) => [
                  formatPercentage(Number(value)),
                  String(name),
                ]}
              />

              <Legend
                wrapperStyle={{
                  fontSize: "14px",
                }}
              />

              <Line
                type="monotone"
                dataKey="ctr"
                name="CTR"
                stroke="#7b55ff"
                strokeWidth={3}
                dot={false}
                activeDot={{ r: 5 }}
              />

              <Line
                type="monotone"
                dataKey="engagementRate"
                name="Engagement rate"
                stroke="#e657a5"
                strokeWidth={3}
                dot={false}
                activeDot={{ r: 5 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    </section>
  );
};
