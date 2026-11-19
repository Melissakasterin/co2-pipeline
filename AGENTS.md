# AGENTS.md

## Project
We answer one question: which EU country has reduced its CO₂ emissions per person (`co2_per_capita`) the most since 2000?

## Setup & commands
- Python environment: `python3 -m venv .venv`, `source .venv/bin/activate`, `python -m pip install -r requirements.txt`
- Activate `.venv` in every new terminal before you start.
- Pipeline (scripts in `src/`, built in Task 4): `python src/download.py`, then `python src/clean_co2.py`, then `python src/analyse.py`
- Tests: `python -m pytest`

## Data
- Source: Our World in Data, CO₂ dataset, `data/raw/owid-co2-data.csv`
- Version: pinned to commit `382ee6c662b0ece26e111f263b44c029afad7787` of github.com/owid/co2-data (2 June 2026). SHA-256 of the data file starts with `7f78e2b2`. Do not use the `master` branch.
- Licence: CC BY 4.0, credit "Our World in Data".
- Codebook: `data/raw/owid-co2-codebook.csv` (columns: column, title, description, unit, source).
- Size: 50,411 rows, 79 columns, years 1750–2024. Never read the whole file into the chat; read only the columns you need.
- Units: `population` = people, `co2` = million tonnes (Mt), `co2_per_capita` = tonnes per person (t/person).
- Years: `co2`, `co2_per_capita` and `population` go until 2024. The 5 columns with GDP (`gdp`, `co2_per_gdp`, …) end in 2022.
- Not countries: 36 of the 254 entries in `country` have no `iso_code`: World, continents (also in a "(GCP)" version), EU-27/EU-28, income groups, OECD, International aviation, International shipping, Kuwaiti Oil Fires, Ryukyu Islands.
- Exception: Kosovo has no `iso_code` but is a real country. Do not drop it silently.
- EU countries: the 27 current member states, by ISO code. Do not use the row "European Union (27)" as a country.

## Rules
- `data/raw/` is read-only: never modify, move or delete files there. Write results to `data/processed/`.
- No new packages without asking. Only use what is in `requirements.txt`.
- Do not change or delete tests to make them pass.
- Print the number of rows after every filter.
- No silent filling of missing values. Report them instead.
- Never invent URLs or numbers. If you do not know, ask.
- Do not commit `data/raw/` or `.venv/`.
