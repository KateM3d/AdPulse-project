import { render, screen } from "@testing-library/react";

import { MetricCard } from "./MetricCard";

describe("MetricCard", () => {
  it("renders label and value", () => {
    render(<MetricCard label="Impressions" value="1,281,840" />);

    expect(screen.getByText("Impressions")).toBeInTheDocument();
    expect(screen.getByText("1,281,840")).toBeInTheDocument();
  });

  it("renders description when provided", () => {
    render(
      <MetricCard label="CTR" value="1.19%" description="Click-through rate" />,
    );

    expect(screen.getByText("Click-through rate")).toBeInTheDocument();
  });

  it("does not render a description when omitted", () => {
    const { container } = render(<MetricCard label="Clicks" value="15,220" />);

    expect(
      container.querySelector(".metric-card__description"),
    ).not.toBeInTheDocument();
  });
});
