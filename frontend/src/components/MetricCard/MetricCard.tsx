import { MetricTooltip } from "../MetricTooltip/MetricTooltip";

import "./MetricCard.scss";

interface MetricCardProps {
  label: string;
  value: string;
  description?: string;
  tooltip?: string;
}

export const MetricCard = ({
  label,
  value,
  description,
  tooltip,
}: MetricCardProps) => (
  <article className="metric-card">
    <span className={tooltip ? "metric-card__label metric-label" : "metric-card__label"}>
      {label}
      {tooltip ? <MetricTooltip label={label} text={tooltip} /> : null}
    </span>
    <strong className="metric-card__value">{value}</strong>

    {description && (
      <span className="metric-card__description">{description}</span>
    )}
  </article>
);
