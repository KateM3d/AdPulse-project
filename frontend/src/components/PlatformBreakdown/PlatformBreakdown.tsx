import { useState } from "react";
import {
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import type { PlatformSummary } from "../../types/api";
import { formatNumber, formatPercentage } from "../../utils/formatters";

import "./PlatformBreakdown.scss";

interface PlatformBreakdownProps {
  platforms: PlatformSummary[];
  title?: string;
  description?: string;
}

type PlatformMetric =
  | "ctr"
  | "engagement_rate"
  | "impressions"
  | "clicks"
  | "engagements";

interface MetricConfig {
  label: string;
  formatValue: (value: number) => string;
}

const metricConfig: Record<PlatformMetric, MetricConfig> = {
  ctr: {
    label: "CTR",
    formatValue: formatPercentage,
  },
  engagement_rate: {
    label: "Engagement rate",
    formatValue: formatPercentage,
  },
  impressions: {
    label: "Impressions",
    formatValue: formatNumber,
  },
  clicks: {
    label: "Clicks",
    formatValue: formatNumber,
  },
  engagements: {
    label: "Engagements",
    formatValue: formatNumber,
  },
};

export const PlatformBreakdown = ({
  platforms,
  title = "Performance by platform",
  description = "Compare campaign performance across platforms.",
}: PlatformBreakdownProps) => {
  const [metric, setMetric] = useState<PlatformMetric>("ctr");

  const selectedMetric = metricConfig[metric];

  const chartData = platforms.map((platform) => ({
    platform: platform.platform,
    value: platform[metric],
  }));

  return (
    <section className="platform-breakdown">
      <header className="platform-breakdown__header">
        <div>
          <h2>{title}</h2>
          <p>{description}</p>
        </div>

        <label className="platform-breakdown__metric">
          <span className="platform-breakdown__metric-label">Metric</span>

          <select
            value={metric}
            onChange={(event) =>
              setMetric(event.target.value as PlatformMetric)
            }
            aria-label="Platform comparison metric"
          >
            <option value="ctr">CTR</option>
            <option value="engagement_rate">Engagement rate</option>
            <option value="impressions">Impressions</option>
            <option value="clicks">Clicks</option>
            <option value="engagements">Engagements</option>
          </select>
        </label>
      </header>

      <div className="platform-breakdown__chart">
        <ResponsiveContainer width="100%" height={260}>
          <BarChart
            data={chartData}
            layout="vertical"
            margin={{
              top: 8,
              right: 48,
              bottom: 8,
              left: 12,
            }}
          >
            <CartesianGrid
              stroke="#edf0f4"
              strokeDasharray="3 3"
              horizontal={false}
            />

            <XAxis
              type="number"
              tickFormatter={selectedMetric.formatValue}
              tick={{
                fontSize: 14,
                fill: "#667174",
              }}
              tickLine={false}
              axisLine={false}
            />

            <YAxis
              type="category"
              dataKey="platform"
              width={90}
              tick={{
                fontSize: 14,
                fill: "#1f2729",
                fontWeight: 600,
              }}
              tickLine={false}
              axisLine={false}
            />

            <Tooltip
              cursor={{ fill: "#f6f7fb" }}
              formatter={(value) => [
                selectedMetric.formatValue(Number(value)),
                selectedMetric.label,
              ]}
            />

            <Bar
              dataKey="value"
              name={selectedMetric.label}
              fill="#3154ff"
              radius={[0, 6, 6, 0]}
              maxBarSize={32}
            />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </section>
  );
};
