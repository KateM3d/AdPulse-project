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

  it("renders a tooltip hint when tooltip text is provided", () => {
    render(
      <MetricCard
        label="CTR"
        value="1.19%"
        tooltip="Click-through rate — the percentage of impressions that resulted in a click."
      />,
    );

    expect(
      screen.getByRole("button", { name: "About CTR" }),
    ).toBeInTheDocument();
    expect(screen.getByRole("tooltip")).toHaveTextContent(
      "Click-through rate — the percentage of impressions that resulted in a click.",
    );
  });
});
