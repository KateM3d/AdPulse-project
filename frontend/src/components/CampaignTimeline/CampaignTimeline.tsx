import {
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import type { TimelinePoint } from "../../types/api";
import { formatDate, formatNumber } from "../../utils/formatters";

import "./CampaignTimeline.scss";

interface CampaignTimelineProps {
  timeline: TimelinePoint[];
  title?: string;
}

export const CampaignTimeline = ({
  timeline,
  title = "Campaign timeline",
}: CampaignTimelineProps) => (
  <section className="campaign-timeline">
    <div className="campaign-timeline__header">
      <div>
        <span className="campaign-timeline__eyebrow">Performance over time</span>
        <h2>{title}</h2>
      </div>
    </div>

    <div className="campaign-timeline__chart">
      <ResponsiveContainer width="100%" height={360}>
        <LineChart data={timeline}>
          <CartesianGrid stroke="#edf0f6" strokeDasharray="4 4" />

          <XAxis dataKey="date" tickFormatter={(value: string) => formatDate(value)} />

          <YAxis tickFormatter={(value: number) => formatNumber(value)} />

          <Tooltip
            labelFormatter={(value) => formatDate(String(value))}
            formatter={(value, name) => [formatNumber(Number(value)), String(name)]}
          />

          <Line
            type="monotone"
            dataKey="impressions"
            stroke="#3458ff"
            strokeWidth={2.5}
            dot={false}
          />

          <Line
            type="monotone"
            dataKey="clicks"
            stroke="#7b55ff"
            strokeWidth={2.5}
            dot={false}
          />

          <Line
            type="monotone"
            dataKey="engagements"
            stroke="#e657a5"
            strokeWidth={2.5}
            dot={false}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  </section>
);
