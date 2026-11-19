from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent
INPUT_FILE = PROJECT_ROOT / "data" / "processed" / "co2_eu.csv"
OUTPUT_FILE = PROJECT_ROOT / "figures" / "co2_per_capita_reductions.png"

EU27 = [
    "Austria",
    "Belgium",
    "Bulgaria",
    "Croatia",
    "Cyprus",
    "Czechia",
    "Denmark",
    "Estonia",
    "Finland",
    "France",
    "Germany",
    "Greece",
    "Hungary",
    "Ireland",
    "Italy",
    "Latvia",
    "Lithuania",
    "Luxembourg",
    "Malta",
    "Netherlands",
    "Poland",
    "Portugal",
    "Romania",
    "Slovakia",
    "Slovenia",
    "Spain",
    "Sweden",
]


def main() -> None:
    data = pd.read_csv(
        INPUT_FILE,
        usecols=["country", "year", "co2_per_capita"],
    )
    endpoints = data[data["year"].isin([2000, 2024])]
    print(f"Rows after filtering to 2000 and 2024: {len(endpoints)}")

    unexpected_countries = sorted(set(data["country"]) - set(EU27))
    if unexpected_countries:
        raise SystemExit(
            "Unexpected countries in input: " + ", ".join(unexpected_countries)
        )

    values = endpoints.pivot(
        index="country",
        columns="year",
        values="co2_per_capita",
    ).reindex(index=EU27, columns=[2000, 2024])
    missing = values.isna()
    if missing.any().any():
        missing_endpoints = [
            f"{country} ({year})"
            for country in EU27
            for year in [2000, 2024]
            if missing.loc[country, year]
        ]
        raise SystemExit(
            "Missing co2_per_capita value(s) for: " + ", ".join(missing_endpoints)
        )

    zero_baselines = values.index[values[2000] == 0].tolist()
    if zero_baselines:
        raise SystemExit(
            "Cannot calculate percentage reduction with a zero 2000 value for: "
            + ", ".join(zero_baselines)
        )

    results = pd.DataFrame(
        {
            "country": EU27,
            "cut_tonnes_per_person": (
                values[2000].to_numpy() - values[2024].to_numpy()
            ),
            "cut_percent": (
                (values[2000].to_numpy() - values[2024].to_numpy())
                / values[2000].to_numpy()
                * 100
            ),
        }
    )

    by_tonnes = results.sort_values(
        "cut_tonnes_per_person", ascending=False, kind="stable"
    )
    by_percent = results.sort_values("cut_percent", ascending=False, kind="stable")

    print("Top 3 reductions in tonnes per person (2000 to 2024):")
    for row in by_tonnes.head(3).itertuples(index=False):
        print(f"  {row.country}: {row.cut_tonnes_per_person:.2f} tonnes/person")

    print("Top 3 reductions in percent (2000 to 2024):")
    for row in by_percent.head(3).itertuples(index=False):
        print(f"  {row.country}: {row.cut_percent:.2f}%")

    chart_data = by_tonnes
    fig, ax = plt.subplots(figsize=(12, 9))
    ax.barh(chart_data["country"], chart_data["cut_tonnes_per_person"])
    ax.axvline(0, color="black", linewidth=0.8)
    ax.invert_yaxis()
    ax.set_xlabel("Reduction in CO₂ emissions per capita (tonnes per person)")
    ax.set_ylabel("Country")
    ax.set_title("Change in EU CO₂ emissions per capita, 2000–2024")
    fig.tight_layout()

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT_FILE, dpi=150)
    plt.close(fig)
    print(f"Saved chart to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
