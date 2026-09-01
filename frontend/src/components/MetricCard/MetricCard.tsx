import "./MetricCard.scss";

interface MetricCardProps {
  label: string;
  value: string;
  description?: string;
}

export const MetricCard = ({ label, value, description }: MetricCardProps) => (
  <article className="metric-card">
    <span className="metric-card__label">{label}</span>
    <strong className="metric-card__value">{value}</strong>

    {description && (
      <span className="metric-card__description">{description}</span>
    )}
  </article>
);
