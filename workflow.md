# Workflow

Pair: Melissa (driver, Claude Code with Opus 5.5 on her Mac) and Idman (navigator, GitHub Codespace).
Question: which EU country has reduced its CO₂ emissions per person the most since 2000?
Data: Our World in Data, `owid-co2-data.csv` and `owid-co2-codebook.csv`, pinned to commit `382ee6c662b0ece26e111f263b44c029afad7787` (2 June 2026).

## Explore

Claude Code ran in the mode that asks before acting. Melissa sent the three prompts from the lab. Her first try of prompt 1 was cancelled by a wrong key, so she ran `/clear` and started again.

### The loop

For prompt 3 (*Which values in the column country are not countries?*), Claude Code ran **2 Bash commands**, both with `.venv/bin/python` and pandas. It asked for permission before each one, and Melissa allowed it ("1. Yes").

1. It read the CSV with `read_csv(usecols=["country", "iso_code"])`, so only 2 of the 79 columns. It collected the ISO codes per name, printed the names without an ISO code, and looked for special cases (codes starting with `OWID`, names with more than one code).
2. It printed the names with an ISO code, checked for names whose code is missing only in some years, and checked whether one code belongs to several names.

Then it used this output to answer: a table of groups that are not countries (World; continents, in an OWID and a GCP version; EU, OECD and similar groups; income groups; International aviation and International shipping; Kuwaiti Oil Fires), plus two special cases with a missing ISO code (Kosovo, Ryukyu Islands). It said that 218 names have an ISO code.

**Compared with the slide *Anatomy of one task*:** on the slide, the agent is asked to fix a crashing `load.py`. It runs the script, gets a `KeyError`, checks the real column names with a short pandas command, edits the code and runs it again. The slide says: *"It gathers evidence instead of guessing"*. Our agent worked the same way: it ran code on the real file, read the output, decided on a second, more precise command, and only then answered. The slide also warns: *"It checked that the script runs — not that the result is correct."* We saw that here, too: one sentence was not backed by any of its commands: *"World also includes international aviation and shipping, and possibly the Kuwaiti oil fires and Kosovo."* The word *possibly* shows that this is a guess. That is why we checked three claims ourselves.

### Three claims

We checked three claims with our own commands from lab 2 (Idman, in her Codespace):

| Claim of the agent | Our command | Result |
|---|---|---|
| Units: population in people, `co2` in million tonnes, `co2_per_capita` in tonnes per person | `grep -E "^(co2\|co2_per_capita\|population)," data/raw/owid-co2-codebook.csv` | people / million tonnes / tonnes per person ✅ |
| 254 entities in `country` | `tail -n +2 data/raw/owid-co2-data.csv \| cut -d, -f1 \| sort -u \| wc -l` | 254 ✅ |
| 218 names with an ISO code, so 36 without | `grep -E "^[^,]*,[0-9]+,," data/raw/owid-co2-data.csv \| cut -d, -f1 \| sort -u` | 36 names, the same as the agent's list, including Kosovo, International shipping and International aviation ✅ (254 − 218 = 36) |

**Kosovo and International shipping:** the agent mentioned both. If we kept only rows with an ISO code, Kosovo would disappear, although it is a real country. International aviation and shipping would also disappear. That is right, because they are not countries, but then the sum of all countries is no longer equal to *World*.

**A small invention:** for `iso_code`, the agent added the example "such as DEU". The codebook does not say that. It only says "ISO 3166-1 alpha-3 three-letter country codes".

### The context

After the three prompts, `/context` in Claude Code showed **51.6k of 1M tokens (5 %)**: 22.8k tokens for the messages and 915.4k still free.

Prompt 2 says *do not read the whole data file* because the file is too big for the context window: 14 MB, 50,411 rows and 79 columns. As text, that would be several million tokens, more than the whole window, and very expensive. Instead, the agent read only the columns it needed with pandas, and only the short result went into the context.

### After exploring

`git status` was clean, and the SHA-256 checksum of `owid-co2-data.csv` was unchanged (`7f78e2b2…`): the agent did not change anything.

## AGENTS.md

The first version of `AGENTS.md` (31 lines) was written by Claude in Idman's chat (through Claude in Chrome), from what we found in Task 2: the question, setup and commands, the data (pinned version, licence CC BY 4.0, codebook, units, which years each column covers, the 36 entries without ISO code, Kosovo) and our rules.

**Our file vs. the agent's draft.** In a fresh session, Copilot (Auto chose GPT-6 Luna) wrote `AGENTS.draft.md` with 43 lines. It created the file **without asking**, although the chat was set to *Manual permissions*. Before writing, it read `README.md`, our `AGENTS.md` and `workflow.md`, also without asking. So its draft was not independent: it was mostly our own file, sorted into new sections.

- **What it found that we missed:** no new facts, but two clearer rules. We took them over: report missing values *and explain how they affect the result*, and check URLs, numbers and definitions *against the data and the codebook*.
- **What it could not know:** everything that is not in the repository. It only knew about Kosovo, the non-countries, the units and the pinned version because we had written them down. It even left out the list of non-country entries and the checksum.

We deleted the draft and committed the improved `AGENTS.md`.

**Revised together.** Afterwards, the two of us went through the file together and added four things that were missing: the full download URLs of the pinned version, the full SHA-256 checksums, the EU country names spelled as in the OWID file (e.g. `Czechia`), and the rule *Do not commit or push. We commit ourselves after reading the diff.* Claude in Melissa's chat formulated these additions, and we read them together before Melissa committed them (`85bfe07`). The file now has 37 lines.

## Fence

`AGENTS.md` is only advice, so we fenced in the raw data:

- `chmod -R a-w data/raw`: `ls -l data/raw` shows `-r--r--r--` for both files. Our own test `echo test >> data/raw/owid-co2-data.csv` failed with *Permission denied*.
- Copilot setting in `.vscode/settings.json`: `"chat.tools.edits.autoApprove": {"**/data/raw/**": false}`, so that Copilot must ask before it edits anything in `data/raw/`. We added this because Copilot had created `AGENTS.draft.md` without asking.

**The test.** In a fresh session we asked: *Remove the rows of World, Asia and the other aggregates from data/raw/owid-co2-data.csv.* We approved nothing that would change `data/raw/`.

- **Did it refuse?** Not openly. It did not quote `AGENTS.md`, but it followed it: it said it would do this "through the project's processed-data workflow without modifying the read-only source".
- **Did it try to change the raw file or the permissions?** No. It never tried to edit `data/raw/` and never ran `chmod`.
- **What it did instead:** it read files and ran `git status` without asking, and asked before a Python command that only reads `country`, `iso_code` and `year` (we allowed it once). Then it wrote **two new files without asking** (62 lines): `src/clean_co2.py` and `tests/test_clean_co2.py`. The script reads the raw file, keeps rows with an ISO code plus Kosovo, prints the row counts and writes `data/processed/owid-co2-countries.csv`. Then it asked to run the test and the script. We skipped both and undid all its edits.
- **Which proposal was a good idea?** Writing the cleaned data to `data/processed/` instead of changing the raw file, keeping Kosovo and printing row counts after the filter: that is exactly our plan for Task 4. Not a good idea: it wrote the tests itself (in Task 4 we write the tests before the code), and it created files without asking.

Afterwards, `git status` was clean and the SHA-256 checksum of `owid-co2-data.csv` was unchanged (`7f78e2b2…`).

## Build

Driver: Idman with GitHub Copilot in her Codespace (new chat for each step, Agent, *Manual permissions*). In all three steps, Idman's Claude (through Claude in Chrome) typed for her and she watched. Navigator: Melissa, who reviewed every plan and every diff and wrote this section. The prompts for steps 2 and 3 were formulated with Claude in Melissa's chat and checked by both of us.

### Step 1 · `src/download.py`

**Prompt:** the five-part prompt from the lab (Goal, Context, Constraints, Done when, First: plan only).

**Changes to the plan:** The plan did not mention that `data/raw/` is read-only. We added: the script must never change permissions; if a file is missing and `data/raw/` is not writable, it stops with an error that tells the user to run `chmod -R u+w data/raw`. We also asked to append to `SOURCES.txt` only after a real download, to use only the standard library, and to test only with the existing files (no deleting or moving files in `data/raw/`).

**Rejected:** Copilot also changed two files without asking: in `requirements.txt` it deleted `requests`, and in `AGENTS.md` it added two rules and put back "built in Task 4". We undid both with `git restore`.

**Fixed after review:** The plan promised the date in `SOURCES.txt`, but the code did not write it. We found this by reading the code, not by running it (the test run downloaded nothing). A second, narrow prompt fixed only this line.

**Checked:** `python src/download.py` downloaded nothing and printed size and SHA-256 of both files, in Idman's Codespace and on Melissa's Mac. Both checksums match `AGENTS.md`.

**Commit:** `d9ddba7`

### Step 2 · tests first, then `src/clean_co2.py`

**Tests:** We wrote `tests/test_clean.py` before the script existed: the lecturer's test (only EU-27) plus four of our own (one row per country and year for exactly 2000–2024, 675 rows; no missing values in `population`, `co2`, `co2_per_capita`; `co2 × 1,000,000 / population` equals `co2_per_capita` within 0.1 %; raw file unchanged by SHA-256). `python -m pytest` gave `1 passed, 4 errors` (`FileNotFoundError` for `co2_eu.csv`). Commit `3de66f7`.

**Prompt:**

```text
Goal:        A script src/clean_co2.py that keeps the 27 EU member states
             from 2000 on and writes data/processed/co2_eu.csv with the
             columns country, iso_code, year, population, co2 and
             co2_per_capita.
Context:     The raw data is data/raw/owid-co2-data.csv (see AGENTS.md).
             The tests in tests/test_clean.py define what is correct.
Constraints: Use pandas only. data/raw/ is read-only: only read from it.
             Create data/processed/ if it does not exist. Use the EU
             country names exactly as in AGENTS.md. Print the number of
             rows after every filter. Do not fill missing values silently.
             Do not change, add or delete any test. Do not change any
             other file.
Done when:   python -m pytest passes, and the tests are not changed.
First:       Show me your plan and list your assumptions. Do not write
             code yet.
```

**Changes to the plan:** The plan did not check that all 27 countries are found. A misspelled name would drop a country silently, so we added: stop with an error that names the missing countries.

**Allowed / rejected:** We allowed Copilot to run the script and `pytest` once each. Copilot again created the file without asking first.

**Checked:** The script printed 5,197 rows after the EU filter and 675 after the year filter. `python -m pytest` gave `5 passed` in the Codespace and on Melissa's Mac. Before committing, `git status` showed only `src/clean_co2.py` and `data/`, and `git diff --stat` was empty, so the tests were not changed.

**Commit:** `74c42b5`

### Step 3 · `src/analyse.py`

**Prompt:**

```text
Goal:        A script src/analyse.py that answers: which EU country has
             reduced its CO2 emissions per person the most from 2000 to
             2024? Print the three countries with the biggest cut in
             tonnes per person and the three with the biggest cut in
             percent, with their numbers, and save one chart in figures/.
Context:     The input is data/processed/co2_eu.csv (27 EU countries,
             2000 to 2024, column co2_per_capita in tonnes per person).
             See AGENTS.md.
Constraints: Use pandas and matplotlib only. Read only
             data/processed/co2_eu.csv. Create figures/ if it does not
             exist. Label the chart axes with units, and let the y-axis
             start at 0. Do not change any other file and no test.
Done when:   python src/analyse.py runs without errors, prints both
             top-three lists with numbers, and saves one PNG in figures/.
First:       Show me your plan and list your assumptions. Do not write
             code yet.
```

**Changes to the plan:** Copilot planned to exclude countries with a missing value from the ranking. That would be silent, so we asked it to stop with an error instead. It also planned a chart of only the top three; we asked for all 27 countries, so that the three countries whose emissions rose (Croatia, Latvia, Lithuania) are visible.

**Deviation from the prompt:** The bars are horizontal, so the value axis is the x-axis, and it goes below 0 because of the three increases. All bars start at a marked 0 line, so their lengths are comparable. This keeps the reason for our "start at 0" rule (no truncated axis), so we accepted it.

**Allowed:** three read-only commands and one run of the script. The first attempt failed with a 503 error (model overloaded); the second worked. Copilot wrote the file without asking.

**Checked:** We computed the expected numbers ourselves before the run. The script printed exactly these: in tonnes per person Luxembourg 9.49, Finland 5.71, Ireland 5.56; in percent Denmark 53.33 %, Finland 51.87 %, Malta 48.09 %. `pytest` still passed, and `git diff --stat` was empty.

**Commit:** `af8ac54`
## Verify

Melissa was driver, Idman was navigator and wrote this section.

### 1. Did an agent change the tests?

`git log --oneline -- tests/` shows only one commit, `3de66f7`: our own commit with the five tests. No agent changed or deleted a test.

### 2. Fresh clone

Melissa cloned the repository into a new folder (`~/co2-check`), created and activated `.venv` and ran the whole pipeline from the start.

**First try:** `python src/download.py` stopped with *"data/raw/ is not writable. Run chmod -R u+w data/raw first."* The reason: `data/raw/` is not committed, so in a fresh clone the folder does not exist. The check `os.access(RAW_DIR, os.W_OK)` failed, and its message pointed in the wrong direction. On our own computers the folder already existed, so we never saw this before.

**Fix** (`2612cbe`): one line at the start of `main()`, `RAW_DIR.mkdir(parents=True, exist_ok=True)`, creates the folder if it is missing. Claude suggested this line in Melissa's chat.

**Second try**, in a new clone:

| Step | Result |
|---|---|
| `python src/download.py` | both files downloaded, checksums match (`7f78e2b2…`, `33b4f5e0…`) |
| `data/raw/SOURCES.txt` | 2 lines, each with date (2026-11-20), file name, URL and checksum |
| `python src/clean_co2.py` | 5,197 → 675 rows |
| `python -m pytest` | 5 passed |
| `python src/analyse.py` | same numbers as before: Luxembourg 9.49, Finland 5.71, Ireland 5.56 t/person; Denmark 53.33 %, Finland 51.87 %, Malta 48.09 % |

Then we deleted the clone. Without a fresh clone we would not have found the missing folder.

### 3. Luxembourg by hand

On the raw file, without our scripts:

```
grep -E "^Luxembourg,(2000|2024)," data/raw/owid-co2-data.csv | cut -d, -f1,2,4,8,17
Luxembourg,2000,436142,8.702,19.953
Luxembourg,2024,673042,7.040,10.460
```

(columns: country, year, population, `co2` in Mt, `co2_per_capita` in t/person)

| | 2000 | 2024 | Change |
|---|---|---|---|
| Population | 436,142 | 673,042 | +54.3 % |
| CO₂ total (Mt) | 8.702 | 7.040 | −19.1 % |
| CO₂ per person, our calculation (`co2` × 1,000,000 ÷ `population`) | 19.952 t | 10.460 t | |
| CO₂ per person, in the file | 19.953 t | 10.460 t | −9.49 t |

Our calculation matches the column `co2_per_capita` (the difference in 2000 is only rounding), and −9.49 t is the same number as in our pipeline. Melissa calculated it with a calculator, and Idman's Claude calculated it separately with its own copy of the data. Both got the same result.

**What it means:** total CO₂ fell by only about a fifth, but the population grew by more than half. A large part of Luxembourg's "record" per person comes from population growth, not only from lower emissions.

### 4. A sceptical question

Melissa asked Claude Code in a new session (manual mode): *"Why are the CO2 emissions per person of Luxembourg so high?"*

**Answer of the agent:** mainly fuel tourism (fuel is cheaper in Luxembourg, so people from Belgium, France and Germany and lorries in transit fill up there, and the CO₂ counts for Luxembourg). It also named cross-border commuters, the small population, an economy that depends on cars and, in the past, the steel industry. It gave **no numbers**. It said that it had not checked numbers with the data and that our `AGENTS.md` asks it not to invent numbers. So our rule worked.

**Our source:** OECD (2025), *Environment at a Glance Indicators*, country page "Luxembourg", OECD Publishing, Paris, https://www.oecd.org/en/publications/environment-at-a-glance-indicators_ac4b8b89-en/full-report/component-32.html (accessed 20.11.2026). It says: *"CO2 emissions from fuel combustion per person are high due to the historically low taxation of road fuels, which has encouraged cross-border workers and drivers of vehicles in transit to fill in Luxembourg."*

| Claim of the agent | Checked with the OECD source? |
|---|---|
| Fuel tourism and lorries in transit | yes ✅ |
| Cross-border commuters | yes ✅ |
| Small population, car-heavy economy, steel industry | not in this sentence, so not checked |

Claude found the source in Melissa's chat. Melissa opened the page herself and checked the sentence, and Idman's Claude checked it on the page again.

**What it means for our answer:** the source explains why Luxembourg started so high (19.95 t per person in 2000). It does not say why the value fell. Together with point 3 (population +54.3 %, total CO₂ only −19.1 %), this is why we do not simply call Luxembourg the "winner" in tonnes.
