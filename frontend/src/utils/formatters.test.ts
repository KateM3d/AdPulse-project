import {
  formatDate,
  formatNumber,
  formatPercentage,
} from "./formatters";

describe("formatters", () => {
  it("formats numbers with separators", () => {
    expect(formatNumber(1281840)).toBe("1,281,840");
  });

  it("formats percentages to two decimal places", () => {
    expect(formatPercentage(1.1873557)).toBe("1.19%");
  });

  it("formats ISO dates for display", () => {
    expect(formatDate("2026-03-02")).toBe("Mar 2, 2026");
  });
});
