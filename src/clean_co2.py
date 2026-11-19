from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_FILE = PROJECT_ROOT / "data" / "raw" / "owid-co2-data.csv"
OUTPUT_FILE = PROJECT_ROOT / "data" / "processed" / "co2_eu.csv"

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

COLUMNS = [
    "country",
    "iso_code",
    "year",
    "population",
    "co2",
    "co2_per_capita",
]


def main() -> None:
    df = pd.read_csv(RAW_FILE, usecols=COLUMNS)

    df = df[df["country"].isin(EU27)]
    print(f"Rows after filtering to EU27 countries: {len(df)}")

    df = df[df["year"] >= 2000]
    print(f"Rows after filtering to years >= 2000: {len(df)}")

    present_countries = set(df["country"])
    missing_countries = sorted(set(EU27) - present_countries)
    if missing_countries:
        raise SystemExit(
            "Missing EU countries after filtering: "
            + ", ".join(missing_countries)
        )

    missing_values = df[COLUMNS].isna().sum()
    missing_values = missing_values[missing_values > 0]
    if not missing_values.empty:
        details = ", ".join(
            f"{column}={count}" for column, count in missing_values.items()
        )
        raise SystemExit(f"Missing values remain after filtering: {details}")

    df = df[COLUMNS].sort_values(["country", "year"]).reset_index(drop=True)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"Wrote {len(df)} rows to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
