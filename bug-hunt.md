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
| 5 | `biggest_cuts` | Filters (off by one) | `year > 1990` leaves out 1990, so the base year is 1991. Probably `>=` was meant. Also, first against last value is only comparable if all countries cover the same years. | `sub = eu[eu.year >= 1990].sort_values("year"); sub.groupby("country")["year"].agg(["min", "max"]).query("min != 1990 or max != @sub.year.max()")` → `{}`: all countries cover 1990 to the last year · `biggest_cuts(eu).nsmallest(3, "tonnes")` → Luxembourg −21.8, Estonia −15.4, Denmark −7.6 t · `biggest_cuts(eu, since=1989).nsmallest(3, "tonnes")` (includes 1990) → Luxembourg −20.7, Estonia −17.1, Germany −6.2 t: with 1990 as the first year, Denmark drops out of the top 3. |
| 6 | `chart` | Units and scales | The label says "(t)", but `co2` is in million tonnes (Mt). The y-axis starts at 2000: the territorial value falls from about 3,700 to 2,400 (to about 65 %), but the visible bars shrink from 1,700 to 400 (to about 24 %), so the fall looks almost three times as dramatic. The title "EU-27" is only right if 1 gives 27 countries. | `eu_report.py`: `ax.set_ylabel("CO2 emissions (t)")` and `ax.set_ylim(2000, None)` · the chart `eu_report.png` · codebook unit of `co2`: million tonnes (checked in Task 2) |

Checked, not an error: the latest year (2023) is complete for `consumption_co2`. `df[df.country.isin(MEMBERS.country) & (df.year == 2023)]["consumption_co2"].isna().sum()` → 0.

## Task 6 · The agent's review

Fresh Claude Code session in Melissa's terminal (20.11.2026, 15:46), with the prompt from the lab. It ran its own checks and changed no file (`git status`: working tree clean). It also read our committed `bug-hunt.md`, so its review was not fully independent of our list.

| Error | We found it | Agent found it | Agent's evidence |
|---|---|---|---|
| `Czech Republic` vs. `Czechia` in `MEMBERS` (`eu_members`) | yes (row 1) | yes (#1) | Totals with Czechia: 3,870.3 / 2,485.0 Mt, the same as the `European Union (27)` row |
| `dropna(subset=["consumption_co2"])` removes 2024, so the report ends in 2023 (`eu_members`) | partly (row 1, no number) | yes, but listed it as a "smaller point", not as an error in the numbers | It removes exactly 27 rows from 1990 onwards, all in 2024; only `consumption_co2` is missing in 2024 |
| Unweighted mean of per-person values (`per_person`) | yes (row 3) | yes (#2) | Total CO₂ / total population: 9.21 / 5.51 t, −40.2 %, the same as the EU-27 row |
| World total sums all rows, including aggregates (`world_share`) | yes (row 4) | yes (#3) | In 1990 the sum is 6.8 times the `World` row; correct share 17.0 / 6.5 %, the same as `share_global_co2` |
| `year > since` makes 1991 the base year (`biggest_cuts`) | yes (row 5) | yes (#4) | Denmark 12.44 t in 1991 vs. 10.40 t in 1990; top 3 with both fixes: Luxembourg −20.7, Estonia −17.1, Czechia −8.2 t |
| Y-axis label "(t)" instead of Mt, axis starts at 2,000 (`chart`) | yes (row 6) | yes (#6) | A 35 % fall looks like a fall of about 75 % |

**Not an error in the numbers:** The agent's #5 says "emissions embedded in imports" should be called net trade (OWID's `trade_co2`). The numbers are consumption-based minus territorial, as the report says, and apart from the missing Czechia they equal `trade_co2` (490 / 817 Mt). We count this as an imprecise label, not as one of the errors.

**One number checked:** We checked the agent's Czechia −8.2 t and Denmark's 10.40 / 12.44 t directly in `data/raw/owid-co2-data.csv`, without `eu_report.py` → 15.94 t (1990), 7.70 t (2023), difference −8.2 t; Denmark 10.40 / 12.44 t. The agent's numbers are right and inherit no error. Our own evidence in row 5 does inherit one: Germany is third there only because Czechia was missing (error 1).

## Conclusion

The error in `world_share` changed the report the most: the EU's share of world emissions rose from 2.4 % to 17.0 % in 1990, about seven times the wrong value. The most convincing wrong number was the fall in CO₂ per person, −45.7 % instead of −41.5 %: it looks precise, it is close to the right value and it flatters the EU, so nobody in a presentation would have questioned it, while a share of 2.4 % might at least have surprised someone who knows the EU is a large emitter. The agent was faster and more thorough with evidence: in about a minute it checked every suspicion against Our World in Data's own rows and explained why Denmark's cut looked too big (its high value in 1991). We were better at judging what matters: the agent called the missing year 2024 a "smaller point", while we counted it as an error, and when we checked its numbers ourselves we also found that our own evidence in row 5 had inherited error 1.