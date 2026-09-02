import { render, screen } from "@testing-library/react";

import { CTR_TOOLTIP } from "../../utils/metricTooltips";
import { MetricTooltip } from "./MetricTooltip";

describe("MetricTooltip", () => {
  it("renders an accessible hint trigger and tooltip content", () => {
    render(<MetricTooltip label="CTR" text={CTR_TOOLTIP} />);

    expect(
      screen.getByRole("button", { name: "About CTR" }),
    ).toBeInTheDocument();
    expect(screen.getByRole("tooltip")).toHaveTextContent(CTR_TOOLTIP);
  });
});
