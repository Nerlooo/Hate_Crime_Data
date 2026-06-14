"""
Shared utility functions used across pages and components.
"""

import pandas as pd
import matplotlib.pyplot as plt
from config import MPL_PARAMS, COLORS, NUM_AGENCIES, POP_COVERED


def apply_mpl_style() -> None:
    """Apply the project's global matplotlib configuration."""
    plt.rcParams.update(MPL_PARAMS)


def print_national_summary(total_row: pd.Series) -> None:
    """
    Display the national summary to console.

    Args:
        total_row: "Total" row from t1_detail.
    """
    print("\n" + "=" * 55)
    print("  NATIONAL SUMMARY 2024")
    print("=" * 55)
    print(f"  Total incidents        : {int(total_row['Incidents']):>8,}")
    print(f"  Total offenses         : {int(total_row['Offenses']):>8,}")
    print(f"  Total victims          : {int(total_row['Victims1']):>8,}")
    print(f"  Known offenders        : {int(total_row['Known\noffenders2']):>8,}")
    print(f"  Participating agencies : {NUM_AGENCIES:>8,}")
    print(f"  Population covered     : {POP_COVERED:>8,}")
    print("=" * 55)


def print_complementary_analyses(
    t12_states: pd.DataFrame,
    t2_clean: pd.DataFrame,
    total_row: pd.Series,
) -> None:
    """
    Display complementary textual analyses.

    Args:
        t12_states: cleaned table 12.
        t2_clean:   cleaned table 2.
        total_row:  "Total" row from t1_detail.
    """
    print("\n" + "=" * 55)
    print("  COMPLEMENTARY ANALYSES")
    print("=" * 55)

    avg_report = t12_states["reporting_rate"].mean()
    top5_report = t12_states.nlargest(5, "reporting_rate")[
        ["Participating State/Federal", "reporting_rate"]
    ]
    print(f"\nAverage agency reporting rate: {avg_report:.1f}%")
    print("  States with best reporting rates:")
    print(top5_report.to_string(index=False))

    print("\nTop 10 States by total incidents:")
    top10 = t12_states.nlargest(10, "Total\nnumber of\nincidents\nreported")[
        ["Participating State/Federal", "Total\nnumber of\nincidents\nreported", "incidents_per_100k"]
    ]
    print(top10.to_string(index=False))

    violent = [
        "Murder and nonnegligent manslaughter",
        "Rape", "Aggravated assault", "Robbery",
    ]
    violent_sum = t2_clean[t2_clean["Offense type"].isin(violent)]["Offenses"].sum()
    print(f"\nViolent offenses (persons): {violent_sum:.0f} offenses")

    victims   = int(total_row["Victims1"])
    incidents = int(total_row["Incidents"])
    print(f"\nAverage victims per incident: {victims / incidents:.2f}")
    print("\nAnalysis completed.")


def bar_label(ax, bars, fmt: str = "{:,}", offset: float = 15) -> None:
    """
    Add labels to the right of horizontal bars.

    Args:
        ax:     matplotlib axes.
        bars:   result of ax.barh().
        fmt:    format string for values.
        offset: horizontal offset in data units.
    """
    for bar in bars:
        w = bar.get_width()
        ax.text(
            w + offset,
            bar.get_y() + bar.get_height() / 2,
            fmt.format(int(w)),
            va="center",
            fontsize=9,
        )