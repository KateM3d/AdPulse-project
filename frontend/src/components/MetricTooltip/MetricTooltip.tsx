import "./MetricTooltip.scss";

type MetricTooltipProps = {
  label: string;
  text: string;
};

export const MetricTooltip = ({ label, text }: MetricTooltipProps) => {
  return (
    <span className="metric-tooltip">
      <button
        className="metric-tooltip__trigger"
        type="button"
        aria-label={`About ${label}`}
      >
        i
      </button>

      <span className="metric-tooltip__content" role="tooltip">
        {text}
      </span>
    </span>
  );
};
