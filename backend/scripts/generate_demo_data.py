"""Generate the fictional AdPulse demo dataset.

Every value written by this script is synthetic. "Tidewell" is an invented
payroll-software brand used only to give the demo campaign a coherent story.

The output is deterministic (fixed random seed), so re-running the script
reproduces the committed CSV files byte for byte:

    python scripts/generate_demo_data.py
"""

import csv
import random
from collections.abc import Callable
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
SEED = 2026
CAMPAIGN_START = date(2026, 3, 2)
CAMPAIGN_WEEKS = 10

# A rate curve maps campaign progress (0.0 at the first active week, 1.0 at the
# last) to a percentage rate.
RateCurve = Callable[[float], float]


def flat(rate: float) -> RateCurve:
    return lambda _progress: rate


def linear(start: float, end: float) -> RateCurve:
    return lambda progress: start + (end - start) * progress


@dataclass(frozen=True)
class PlatformPlan:
    platform: str
    weekly_impressions: int
    ctr: RateCurve
    engagement_rate: RateCurve


@dataclass(frozen=True)
class AdPlan:
    ad_id: str
    title: str
    body: str
    image: str
    first_week: int
    last_week: int
    platforms: tuple[PlatformPlan, ...]


AD_PLANS: tuple[AdPlan, ...] = (
    AdPlan(
        ad_id="payroll_in_minutes",
        title="Payroll in four minutes",
        body=(
            "Run payroll for your whole team in about four minutes, with taxes calculated for you."
        ),
        image="payroll_in_minutes.svg",
        first_week=0,
        last_week=9,
        platforms=(
            PlatformPlan("LinkedIn", 12_000, flat(2.2), flat(3.3)),
            PlatformPlan("Google", 9_000, flat(1.9), flat(2.6)),
        ),
    ),
    AdPlan(
        ad_id="global_contractors",
        title="Pay contractors anywhere",
        body=("Send compliant contractor payments to more than 40 countries from one dashboard."),
        image="global_contractors.svg",
        first_week=0,
        last_week=9,
        platforms=(
            PlatformPlan("LinkedIn", 11_000, flat(2.0), flat(2.8)),
            PlatformPlan("Meta", 14_000, flat(0.55), flat(0.9)),
        ),
    ),
    AdPlan(
        ad_id="payday_peace_of_mind",
        title="Payday, minus the panic",
        body="Automatic reminders, approvals, and payslips so payday stays calm.",
        image="payday_peace_of_mind.svg",
        first_week=0,
        last_week=9,
        platforms=(PlatformPlan("Meta", 19_000, flat(0.75), flat(2.6)),),
    ),
    AdPlan(
        ad_id="compliance_checklist",
        title="The small-business payroll checklist",
        body=(
            "A free checklist covering filings, deadlines, and record-keeping for growing teams."
        ),
        image="compliance_checklist.svg",
        first_week=0,
        last_week=9,
        platforms=(
            PlatformPlan("Google", 10_000, linear(1.8, 0.6), linear(2.4, 0.9)),
            PlatformPlan("LinkedIn", 8_000, linear(1.6, 0.7), linear(2.3, 1.0)),
        ),
    ),
    AdPlan(
        ad_id="founder_story",
        title="Why we built Tidewell",
        body="A short story from our founders about fixing payroll for teams under fifty.",
        image="founder_story.svg",
        first_week=7,
        last_week=9,
        platforms=(PlatformPlan("LinkedIn", 9_000, flat(1.7), flat(3.0)),),
    ),
    AdPlan(
        ad_id="benefits_bundle",
        title="Benefits without the paperwork",
        body="Add health, pension, and wellbeing benefits to payroll in a few clicks.",
        image="benefits_bundle.svg",
        first_week=0,
        last_week=9,
        platforms=(
            PlatformPlan("Meta", 13_000, flat(0.6), flat(0.85)),
            PlatformPlan("Google", 7_000, flat(0.7), flat(0.9)),
        ),
    ),
    AdPlan(
        ad_id="switch_in_a_day",
        title="Switch payroll providers in a day",
        body=(
            "Import employee records and payroll history, "
            "then run your first pay cycle the same week."
        ),
        image="switch_in_a_day.svg",
        first_week=0,
        last_week=9,
        platforms=(
            PlatformPlan("Google", 9_500, linear(0.7, 1.8), linear(1.0, 2.4)),
            PlatformPlan("Meta", 12_000, linear(0.6, 1.4), linear(0.9, 2.0)),
        ),
    ),
)

# (week index, ad_id, platform, comment). Written for this demo; not sourced
# from any real audience.
COMMENTS: tuple[tuple[int, str, str, str], ...] = (
    (1, "payroll_in_minutes", "LinkedIn", "Four minutes sounds optimistic, but I'd try it."),
    (2, "payroll_in_minutes", "Google", "Does this handle overtime and bonuses?"),
    (3, "payroll_in_minutes", "LinkedIn", "Signed up for the trial after seeing this."),
    (5, "payroll_in_minutes", "LinkedIn", "Our accountant asked if it exports to our ledger."),
    (6, "payroll_in_minutes", "Google", "Clear message, no fluff. Appreciated."),
    (8, "payroll_in_minutes", "LinkedIn", "Shared with our operations lead."),
    (1, "global_contractors", "LinkedIn", "This is exactly the problem we have with freelancers."),
    (2, "global_contractors", "Meta", "Not relevant to me, why am I seeing this?"),
    (3, "global_contractors", "LinkedIn", "Which countries are supported?"),
    (5, "global_contractors", "Meta", "Scrolled past, then came back. Still unsure."),
    (6, "global_contractors", "LinkedIn", "How are exchange rates handled?"),
    (8, "global_contractors", "Meta", "Too corporate for my feed."),
    (0, "payday_peace_of_mind", "Meta", "Ha, the payday panic is real."),
    (1, "payday_peace_of_mind", "Meta", "Tagging our office manager."),
    (3, "payday_peace_of_mind", "Meta", "Love the illustration style."),
    (4, "payday_peace_of_mind", "Meta", "Cute ad, but what does it actually cost?"),
    (6, "payday_peace_of_mind", "Meta", "This made me laugh. Didn't click though."),
    (7, "payday_peace_of_mind", "Meta", "Would like to see pricing up front."),
    (9, "payday_peace_of_mind", "Meta", "Relatable."),
    (0, "compliance_checklist", "Google", "Downloaded it, genuinely useful."),
    (1, "compliance_checklist", "LinkedIn", "Good reminder on filing deadlines."),
    (4, "compliance_checklist", "Google", "Seen this one a few times now."),
    (6, "compliance_checklist", "LinkedIn", "Is there an updated version?"),
    (8, "compliance_checklist", "Google", "Same checklist again?"),
    (7, "founder_story", "LinkedIn", "Nice to see the people behind the product."),
    (8, "founder_story", "LinkedIn", "Relatable story for anyone who has run a small team."),
    (9, "founder_story", "LinkedIn", "What made you focus on teams under fifty?"),
    (1, "benefits_bundle", "Meta", "Which benefits providers do you work with?"),
    (3, "benefits_bundle", "Google", "Hard to tell what's included."),
    (5, "benefits_bundle", "Meta", "Too vague. Show me an example plan."),
    (7, "benefits_bundle", "Meta", "Not sure this is for small companies."),
    (1, "switch_in_a_day", "Google", "A day? Our last migration took three months."),
    (3, "switch_in_a_day", "Meta", "Sceptical, but curious."),
    (5, "switch_in_a_day", "Google", "The new headline is much clearer."),
    (6, "switch_in_a_day", "Meta", "Booked a demo to see the import tool."),
    (8, "switch_in_a_day", "Google", "Does it migrate year-to-date totals?"),
    (9, "switch_in_a_day", "Meta", "Finally someone talking about switching costs."),
)


def week_date(week: int) -> date:
    return CAMPAIGN_START + timedelta(weeks=week)


def jitter(rng: random.Random, value: float, spread: float) -> float:
    return value * rng.uniform(1 - spread, 1 + spread)


def build_metrics(rng: random.Random) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    for week in range(CAMPAIGN_WEEKS):
        for plan in AD_PLANS:
            if not plan.first_week <= week <= plan.last_week:
                continue

            span = max(plan.last_week - plan.first_week, 1)
            progress = (week - plan.first_week) / span

            for platform in plan.platforms:
                impressions = round(jitter(rng, platform.weekly_impressions, 0.12))
                ctr = jitter(rng, platform.ctr(progress), 0.06)
                engagement_rate = jitter(rng, platform.engagement_rate(progress), 0.06)

                clicks = round(impressions * ctr / 100)
                # Engagements include clicks, so they can never be lower.
                engagements = max(round(impressions * engagement_rate / 100), clicks)

                rows.append(
                    {
                        "date": week_date(week).isoformat(),
                        "ad_id": plan.ad_id,
                        "platform": platform.platform,
                        "impressions": impressions,
                        "clicks": clicks,
                        "engagements": engagements,
                    }
                )

    rows.sort(key=lambda row: (str(row["date"]), str(row["ad_id"]), str(row["platform"])))
    return rows


def build_comments() -> list[dict[str, object]]:
    return [
        {
            "date": (week_date(week) + timedelta(days=2)).isoformat(),
            "ad_id": ad_id,
            "platform": platform,
            "comment": comment,
        }
        for week, ad_id, platform, comment in COMMENTS
    ]


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    rng = random.Random(SEED)

    ads: list[dict[str, object]] = [
        {"ad_id": plan.ad_id, "title": plan.title, "body": plan.body, "image": plan.image}
        for plan in AD_PLANS
    ]
    metrics = build_metrics(rng)
    comments = build_comments()

    write_csv(DATA_DIR / "ad_set.csv", ["ad_id", "title", "body", "image"], ads)
    write_csv(
        DATA_DIR / "metrics.csv",
        ["date", "ad_id", "platform", "impressions", "clicks", "engagements"],
        metrics,
    )
    write_csv(DATA_DIR / "comments.csv", ["date", "ad_id", "platform", "comment"], comments)

    print(f"Wrote {len(ads)} ads, {len(metrics)} metric rows, {len(comments)} comments")


if __name__ == "__main__":
    main()
