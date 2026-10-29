import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";

import { AppLayout } from "./AppLayout";

describe("AppLayout", () => {
  it("renders the AdPulse brand, navigation, and fictional-data notice", () => {
    render(
      <MemoryRouter>
        <AppLayout>
          <p>Page content</p>
        </AppLayout>
      </MemoryRouter>,
    );

    expect(screen.getByRole("link", { name: "AdPulse home" })).toHaveAttribute(
      "href",
      "/",
    );
    expect(
      screen.getByRole("navigation", { name: "Primary" }),
    ).toBeInTheDocument();
    expect(screen.getByText("Page content")).toBeInTheDocument();
    expect(
      screen.getByText(/Tidewell and all campaign data shown here are fictional/),
    ).toBeInTheDocument();
    expect(
      screen.getByRole("link", { name: "Skip to content" }),
    ).toHaveAttribute("href", "#main-content");
  });

  it("marks Campaign as current on ad detail pages", () => {
    render(
      <MemoryRouter initialEntries={["/ads/payroll_in_minutes"]}>
        <AppLayout>
          <p>Ad page</p>
        </AppLayout>
      </MemoryRouter>,
    );

    expect(screen.getByRole("link", { name: "Campaign" })).toHaveAttribute(
      "aria-current",
      "page",
    );
  });
});
