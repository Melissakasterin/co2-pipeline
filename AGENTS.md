# AGENTS.md

## Project
We answer one question: which EU country has reduced its CO₂ emissions per person (`co2_per_capita`) the most since 2000?

## Setup & commands
- Python environment: `python3 -m venv .venv`, `source .venv/bin/activate`, `python -m pip install -r requirements.txt`
- Activate `.venv` in every new terminal before you start.
- Pipeline (scripts in `src/`, not written yet): `python src/download.py`, then `python src/clean_co2.py`, then `python src/analyse.py`
- Tests: `python -m pytest`

## Data
- Source: Our World in Data, CO₂ dataset, `data/raw/owid-co2-data.csv`
- Version: pinned to commit `382ee6c662b0ece26e111f263b44c029afad7787` of github.com/owid/co2-data (2 June 2026). Do not use the `master` branch.
- Download URLs (use exactly these):
  - `https://raw.githubusercontent.com/owid/co2-data/382ee6c662b0ece26e111f263b44c029afad7787/owid-co2-data.csv`
  - `https://raw.githubusercontent.com/owid/co2-data/382ee6c662b0ece26e111f263b44c029afad7787/owid-co2-codebook.csv`
- SHA-256 checksums:
  - `owid-co2-data.csv`: `7f78e2b218ce4bb8c538bbec04fdc9a7982e8d40bff972e650df603899edd5f6`
  - `owid-co2-codebook.csv`: `33b4f5e00efd58c7b83863f736beba1af4df946b43642b0400c3ec38648e0e8e`
- Licence: CC BY 4.0, credit "Our World in Data".
- Codebook: `data/raw/owid-co2-codebook.csv` (columns: column, title, description, unit, source).
- Size: 50,411 rows, 79 columns, years 1750–2024. Never read the whole file into the chat; read only the columns you need.
- Units: `population` = people, `co2` = million tonnes (Mt), `co2_per_capita` = tonnes per person (t/person).
- Years: `co2`, `co2_per_capita` and `population` go until 2024. The 5 columns with GDP (`gdp`, `co2_per_gdp`, …) end in 2022.
- Not countries: 36 of the 254 entries in `country` have no `iso_code`: World, continents (also in a "(GCP)" version), EU-27/EU-28, income groups, OECD, International aviation, International shipping, Kuwaiti Oil Fires, Ryukyu Islands.
- Exception: Kosovo has no `iso_code` but is a real country. Do not drop it silently.
- EU countries: the 27 current member states, spelled exactly as in the OWID file: Austria, Belgium, Bulgaria, Croatia, Cyprus, Czechia, Denmark, Estonia, Finland, France, Germany, Greece, Hungary, Ireland, Italy, Latvia, Lithuania, Luxembourg, Malta, Netherlands, Poland, Portugal, Romania, Slovakia, Slovenia, Spain, Sweden. Use `Czechia`, not "Czech Republic". Do not use the row "European Union (27)" as a country.

## Rules
- `data/raw/` is read-only: never modify, move or delete files there. Write results to `data/processed/`.
- No new packages without asking. Only use what is in `requirements.txt`.
- Do not change or delete tests to make them pass.
- Print the number of rows after every filter.
- No silent filling of missing values. Report them and explain how they affect the result.
- Never invent URLs, numbers or definitions. Check them against the data and the codebook; if that is not possible, ask.
- Do not commit or push. We commit ourselves after reading the diff.
- Do not commit `data/raw/` or `.venv/`.