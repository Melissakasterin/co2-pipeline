# Bug hunt

## Task 6 · Our review (before the agent's review)

Melissa and Idman reviewed `eu_report.py` function by function with the slide *Review checklist for data code*. The suspicions are ours; ChatGPT reformulated our notes. Idman's Claude ran our check commands in her Codespace (20.11.2026) and wrote this table from our notes and the outputs. Report under review: `report_before.txt`.

Setup for all commands:

```python
import pandas as pd
from eu_report import *
df = load(); eu = eu_members(df)
ref = df[df.country == "European Union (27)"].set_index("year")
t = eu_totals(eu)
```

| # | Function | Checklist row | What goes wrong | Evidence: command → output (1990 / 2023) |
|---|---|---|---|---|
| 1 | `eu_members` | Joins and merges, Row counts | The merge needs exactly the same names. A member state that is spelled differently in the two tables (`Czech Republic` in `MEMBERS`, `Czechia` in the file) drops out without a warning. Then `dropna` also removes rows without `consumption_co2`, and with them their territorial values. | `eu.groupby("year")["country"].nunique()` → 26 in 1990, 2000, 2022 and 2023, not 27 · `set(MEMBERS["country"]) - set(df["country"])` → `{'Czech Republic'}` · *No separate number yet for the `dropna` part.* |
| 2 | `eu_totals` | Row counts (follows from 1) | The totals are lower than Our World in Data's own row for the EU, because countries are missing. | `t.loc[[1990, 2023], "co2"]` → 3,706.0 / 2,401.8 Mt · `ref.loc[[1990, 2023], "co2"]` → 3,870.3 / 2,485.0 Mt · `consumption_co2`: 4,208.7 / 3,202.2 vs. 4,360.2 / 3,302.2 Mt |
| 3 | `per_person` | Aggregation | A simple mean of ratios: Luxembourg counts as much as Germany. Right: total CO₂ divided by total population. | `g = eu.groupby("year"); g["co2"].sum() * 1e6 / g["population"].sum()` → 9.05 / 5.46 t · `per_person(eu)` → 9.87 / 5.35 t · `ref["co2_per_capita"]` → 9.22 / 5.51 t |
| 4 | `world_share` | Filters (aggregates excluded?) | The denominator sums all rows of `country`, including `World`, continents, income groups and `European Union (27)`. The world is counted several times, and the EU share is far too small. | `t["co2"] / df[df.country == "World"].set_index("year")["co2"] * 100` → 16.3 / 6.3 % · `ref["share_global_co2"]` → 17.02 / 6.52 % · `world_share(df, eu)` → 2.4 / 0.99 % |
| 5 | `biggest_cuts` | Filters (off by one) | `year > 1990` leaves out 1990, so the base year is 1991. Probably `>=` was meant. Also, first against last value is only comparable if all countries cover the same years. | `sub = eu[eu.year >= 1990].sort_values("year"); sub.groupby("country")["year"].agg(["min", "max"]).query("min != 1990 or max != @sub.year.max()")` → `{}`: all countries cover 1990 to the last year · *Open: no number yet for the effect of `>` vs. `>=`.* |
| 6 | `eu_members`, `main` | Time | The latest year could be incomplete for `consumption_co2`, so `dropna` would remove countries only in that year. | `df[df.country.isin(MEMBERS.country) & (df.year == 2023)]["consumption_co2"].isna().sum()` → 0 · *Open: keep or drop this point?* |
| 7 | `chart` | Units and scales | The label says "(t)", but `co2` is in million tonnes (Mt). The y-axis starts at 2000: the territorial value falls from about 3,700 to 2,400 (to about 65 %), but the visible bars shrink from 1,700 to 400 (to about 24 %), so the fall looks almost three times as dramatic. The title "EU-27" is only right if 1 gives 27 countries. | `eu_report.py`: `ax.set_ylabel("CO2 emissions (t)")` and `ax.set_ylim(2000, None)` · the chart `eu_report.png` · codebook unit of `co2`: million tonnes (checked in Task 2) |

## Task 6 · The agent's review

*Follows after this file is committed (step 4).*
