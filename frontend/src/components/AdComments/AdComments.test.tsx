import { render, screen } from "@testing-library/react";

import type { AdComment } from "../../types/api";
import { AdComments } from "./AdComments";

const comments: AdComment[] = [
  {
    date: "2026-03-17",
    platform: "LinkedIn",
    comment: "Interesting approach to payroll.",
  },
  {
    date: "2026-03-18",
    platform: "Meta",
    comment: "Would love to learn more about this.",
  },
];

describe("AdComments", () => {
  it("renders audience comments", () => {
    render(<AdComments comments={comments} />);

    expect(
      screen.getByRole("heading", { name: "Comments" }),
    ).toBeInTheDocument();

    expect(screen.getByText("2 comments")).toBeInTheDocument();

    expect(
      screen.getByText("Interesting approach to payroll."),
    ).toBeInTheDocument();

    expect(
      screen.getByText("Would love to learn more about this."),
    ).toBeInTheDocument();

    expect(screen.getByText("LinkedIn")).toBeInTheDocument();
    expect(screen.getByText("Meta")).toBeInTheDocument();
  });

  it("renders an empty state when there are no comments", () => {
    render(<AdComments comments={[]} />);

    expect(
      screen.getByText("No comments available for this ad."),
    ).toBeInTheDocument();

    expect(screen.getByText("0 comments")).toBeInTheDocument();
  });
});
