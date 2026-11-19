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
