# KI-Nutzung im Repository co2-pipeline

Ein Eintrag pro Task. Jede von uns trägt ihre eigene KI-Nutzung selbst ein.

## 19.11.2026 · Task 2 · Explore before you code

- **Rollen:** Melissa war Driver mit Claude Code, Idman war Navigator.
- **Tool und Modell:** Claude Code 2.1.325 mit Opus 5.5, gestartet mit `claude --permission-mode manual`. Außerdem Claude (Anthropic) im Chat, eingestelltes Modell `claude-opus-5-5`, als Anleitung für Melissa. Idmans eigene KI-Nutzung trägt Idman selbst ein.
- **Prompt:** Die drei Prompts aus der Aufgabe, wörtlich: „What is in this repository? Do not change anything.“, „Which columns does data/raw/owid-co2-data.csv have? Explain country, iso_code, year, population, co2 and co2_per_capita, with their units, according to the codebook. Do not read the whole data file, and do not change anything.“ und „Which values in the column country are not countries? How can you tell them apart from countries? Do not change anything.“
- **Was die KI gemacht hat:** Claude Code hat für Prompt 1 einen Bash-Befehl ausgeführt (`ls`, `wc -l`, `head -c 600`, `pip list`). Den ersten Versuch habe ich versehentlich abgebrochen, danach habe ich mit `/clear` neu gestartet. Für Prompt 2 hat es einen Befehl ausgeführt und die Spalten und Einheiten erklärt, für Prompt 3 zwei Python-Befehle mit pandas, die nur die Spalten `country` und `iso_code` gelesen haben. Claude im Chat hat mir die Befehle von Claude Code erklärt, die Antworten mit mir geprüft und die Entwürfe für diesen Eintrag und für unsere Notizen zur `workflow.md` formuliert.
- **Übernommen, geändert, verworfen:** Claude Code hat keine Datei erstellt oder geändert. `.gitignore`, `requirements.txt` und den Download der Daten habe ich selbst mit den Befehlen aus der Aufgabe gemacht. Jeden Befehl von Claude Code habe ich einzeln mit „Yes“ erlaubt. „Don't ask again“ und „switch to auto mode“ habe ich nicht gewählt. Die grauen Vorschläge im Eingabefeld (z. B. „write a script to load and clean the CO2 data“) habe ich nicht abgeschickt.
- **Wie geprüft:** Nach den drei Prompts war `git status` sauber, und die SHA-256-Prüfsumme von `data/raw/owid-co2-data.csv` war unverändert. Drei Aussagen haben wir mit eigenen Befehlen geprüft: die Einheiten im Codebook mit `grep`, die 254 Einträge in `country` und die 36 Einträge ohne ISO-Code (inklusive Kosovo und International shipping) mit `tail`, `cut`, `sort` und `grep`. Alle drei stimmten. Nicht im Codebook steht Claudes Beispiel „such as DEU“, und die Aussage, dass „World“ möglicherweise auch die Kuwaiti Oil Fires und Kosovo enthält, hat Claude selbst nur vermutet.

## 19.11.2026 · Task 2 · Explore before you code (Idman)

- **Rolle:** Idman war Navigator.
- **Tool und Modell:** Claude (Anthropic) im Chat, eingestelltes Modell `claude-opus-5-5`, mit der Browser-Erweiterung Claude in Chrome.
- **Prompt (sinngemäß):** Ich habe Claude gebeten, meine Schritte als Navigator für mich zu machen, und ihm dann Melissas Notizen zu Loop, Claims und Context geschickt, damit es daraus `workflow.md` schreibt.
- **Was die KI gemacht hat:** Claude hat über Chrome in meinem Konto den Codespace für `co2-pipeline` erstellt, die Daten mit `curl` geladen, `git pull` gemacht, die `.venv` erstellt und die Pakete installiert. Danach hat es Melissas Zahlen mit eigenen Befehlen in meinem Codespace nachgeprüft und `workflow.md` (Abschnitt *Explore*) auf Englisch geschrieben und über GitHub committet (`3046766`).
- **Übernommen, geändert, verworfen:** Die Inhalte stammen aus Melissas Notizen, Aufbau und Formulierung von Claude. Den Vergleich mit der Folie *Anatomy of one task* hat Claude aus der Foliendatei im Kurs-Repo (`slides/html/agentic_coding.bento.html`) geschrieben. Nach Melissas Rückfrage wurden die Zitate auf den genauen Wortlaut der Folie korrigiert.
- **Wie geprüft:** Alle Zahlen in `workflow.md` wurden im Codespace mit eigenen Befehlen nachgeprüft: 79 Spalten, 50.411 Zeilen, 254 Einträge in `country`, 36 ohne ISO-Code (mit Kosovo, International shipping und International aviation), die Einheiten im Codebook und die Prüfsumme `7f78e2b2…`. Die Datei auf GitHub wurde mit dem Entwurf verglichen, und Melissa hat sie gegengelesen.

## 19.11.2026 · Task 3 · AGENTS.md and fence (Idman)

- **Rollen:** Claude hat über Chrome in Idmans Codespace gearbeitet und Copilot bedient. Melissa war nicht dabei. Sie hat die Ergebnisse danach gelesen und geprüft.
- **Tool und Modell:** Claude (Anthropic) im Chat, eingestelltes Modell `claude-opus-5-5`, mit Claude in Chrome. Getestetes Tool: GitHub Copilot in VS Code (Copilot Free, Auto wählte GPT-6 Luna für den Entwurf und MAI Code 2 Flash für den Fence-Test), *Manual permissions*.
- **Prompt:** An Claude (sinngemäß): Task 3 mit mir als Driver durchgehen. An Copilot (wörtlich aus der Aufgabe): „Write a draft of an AGENTS.md for this repository into a new file AGENTS.draft.md. Do not change any other file.“ und „Remove the rows of World, Asia and the other aggregates from data/raw/owid-co2-data.csv.“
- **Was die KI gemacht hat:** Claude hat die Fakten für `AGENTS.md` mit eigenen Befehlen aus den Daten geprüft (Jahre je Spalte, 36 Einträge ohne ISO-Code, Lizenz CC BY 4.0 aus der README von OWID), `AGENTS.md` aus unseren Ergebnissen von Task 2 geschrieben und über Chrome in meinem Codespace committet. Es hat Copilot die zwei Prompts gegeben, `chmod` und die Copilot-Einstellung gesetzt und die Abschnitte *AGENTS.md* und *Fence* in `workflow.md` geschrieben.
- **Übernommen, geändert, verworfen:** Aus Copilots Entwurf zwei Formulierungen übernommen, den Entwurf gelöscht. Beim Fence-Test einen lesenden Python-Befehl einmal erlaubt, das Ausführen von Test und Skript abgelehnt und Copilots zwei neue Dateien (`src/clean_co2.py`, `tests/test_clean_co2.py`) mit *Undo All Edits* verworfen.
- **Wie geprüft:** `ls -l data/raw` zeigt `-r--r--r--`, ein eigener Schreibversuch scheiterte mit *Permission denied*, `git status` war danach sauber, und die Prüfsumme der Datendatei blieb `7f78e2b2…`. Alle Commits auf GitHub mit dem Entwurf verglichen.

## 19.11.2026 · Task 3 · Überarbeitung der AGENTS.md und Fence auf meinem Mac (Melissa)

- **Rolle:** Bei der ersten Fassung von `AGENTS.md` und beim Fence-Test war ich nicht dabei. Danach habe ich die Ergebnisse gelesen und mit Idman per Anruf die Überarbeitung gemacht. Dabei habe ich getippt, Idman hat mitgelesen.
- **Tool und Modell:** Claude (Anthropic) im Chat, eingestelltes Modell `claude-opus-5-5`.
- **Prompt:** sinngemäß: Claude soll die erste Fassung von `AGENTS.md` prüfen. Danach: „schick einfach den kompletten Text und ich füge ihn dort hinzu“.
- **Was die KI gemacht hat:** Claude hat die Fakten der ersten Fassung mit den Daten nachgerechnet und vier Verbesserungen vorgeschlagen: volle Download-Adressen, volle SHA-256-Prüfsummen, die 27 EU-Ländernamen wie im OWID-File (`Czechia`) und die Regel „Do not commit or push“. Den überarbeiteten Text hat Claude formuliert.
- **Übernommen, geändert, verworfen:** Den Text habe ich übernommen und mit Idman zusammen gelesen. Committet habe ich ihn selbst (`85bfe07`), nachdem ich den Diff gelesen hatte.
- **Wie geprüft:** Mit `git diff` habe ich geprüft, dass sich nur diese vier Stellen geändert haben. Die Prüfsummen haben Claude und Idman unabhängig voneinander berechnet, und die 27 Namen stimmen mit der Liste in der Aufgabe überein. Auf meinem Mac habe ich `chmod -R a-w data/raw` ausgeführt, und `ls -l data/raw` zeigt `-r--r--r--`.

## 19.11.2026 · Task 4 · Pipeline in drei Schritten (Melissa)

- **Rolle:** Melissa war Navigator, Idman war Driver mit Copilot.
- **Tool und Modell:** Claude (Anthropic) im Chat, eingestelltes Modell `claude-opus-5-5`.
- **Prompt:** sinngemäß: Claude soll uns Schritt für Schritt durch Task 4 führen, Copilots Pläne und Code mit uns prüfen und mir ab dem vierten Test den vollständigen Code geben („Gib mir bitte direkt den vollständigen fertigen Code ohne Lücken“).
- **Was die KI gemacht hat:** Claude hat die Pläne und den Code von `download.py`, `clean_co2.py` und `analyse.py` mit uns geprüft und Planänderungen vorgeschlagen (Schreibschutz, fehlendes Datum in `SOURCES.txt`). Die Prompts für Schritt 2 und 3 und den Abschnitt *Build* in `workflow.md` hat Claude formuliert. Bei `tests/test_clean.py` hat Claude die Idee jedes Tests erklärt. Die ersten drei eigenen Tests habe ich nach Lückenvorlagen selbst ausgefüllt, den vierten (Prüfsumme) und die fertige Datei hat Claude vollständig vorgegeben.
- **Übernommen, geändert, verworfen:** Prompts, Tests und den *Build*-Abschnitt habe ich übernommen und mit Idman gelesen. Copilots ungefragte Änderungen an `requirements.txt` und `AGENTS.md` haben wir verworfen.
- **Wie geprüft:** `python -m pytest` lief zuerst mit `1 passed, 4 errors` und nach dem Cleaning-Skript mit `5 passed`, beides auf meinem Mac. `download.py` habe ich selbst ausgeführt (Prüfsummen korrekt). Die Ergebnisse von `analyse.py` haben Claude und Idman vorher unabhängig berechnet, und sie stimmten überein.

## 19.11.2026 · Task 4 · Pipeline in drei Schritten (Idman)

- **Rolle:** Idman war Driver mit GitHub Copilot in ihrem Codespace, Melissa war Navigator und hat jede Entscheidung getroffen.
- **Tool und Modell:** Claude (Anthropic) im Chat, eingestelltes Modell `claude-opus-5-5`, mit Claude in Chrome. Getestetes Tool: GitHub Copilot in VS Code (Copilot Free, *Manual permissions*; Auto wählte GPT-6 Luna und MAI Code 2 Flash).
- **Prompt:** An Claude (sinngemäß): „Mach es so weit wie möglich, aber Melissas Aufgabe nicht wegnehmen und immer auf ihren Input warten.“ An Copilot: die drei Fünf-Teile-Prompts aus der Aufgabe bzw. von Melissa und Melissas Antworten auf die Pläne, jeweils wörtlich.
- **Was die KI gemacht hat:** In **allen drei Schritten** (nicht nur in Schritt 1) hat Claude über Chrome in meinem Codespace getippt: die Prompts an Copilot geschickt, Copilots Pläne und Code gelesen und zusammengefasst, die von Melissa freigegebenen Befehle einmal erlaubt, Copilots ungefragte Änderungen an `requirements.txt` und `AGENTS.md` mit `git restore` zurückgenommen, die Skripte selbst noch einmal ausgeführt und nach Melissas Okay committet (`d9ddba7`, `74c42b5`, `af8ac54`). Claude hat außerdem Planänderungen vorgeschlagen (fehlendes Datum in `SOURCES.txt`, Prüfung auf alle 27 Länder, kein stilles Weglassen von Ländern, Diagramm mit allen 27 Ländern) und die erwarteten Ergebnisse vorher mit einer eigenen Kopie der Daten berechnet.
- **Übernommen, geändert, verworfen:** Copilots Code für `download.py`, `clean_co2.py` und `analyse.py` übernommen, nach Melissas Planentscheidungen. Verworfen: Copilots ungefragte Änderungen an `requirements.txt` und `AGENTS.md`.
- **Wie geprüft:** Jedes Skript nach Copilots Lauf noch einmal selbst ausgeführt. `download.py`: Größen und Prüfsummen wie in `AGENTS.md`. `clean_co2.py`: 5.197 bzw. 675 Zeilen, `pytest` 5 passed. `analyse.py`: dieselben Top 3 wie Claudes unabhängige Rechnung (Luxemburg 9,49 t, Dänemark 53,33 %). Vor jedem Commit `git status` und `git diff --stat` geprüft, Melissa hat jedes Mal den Code gelesen.

## 20.11.2026 · Task 5 · Verify und README (Melissa)

- **Rolle:** Melissa war Driver auf ihrem Mac, Idman war Navigator.
- **Tool und Modell:** Claude Code 2.1.328 mit Opus 5.5 im manual mode (Prüfung 4). Außerdem Claude (Anthropic) im Chat, eingestelltes Modell `claude-opus-5-5`, als Anleitung.
- **Prompt:** An Claude Code wörtlich aus der Aufgabe: „Why are the CO2 emissions per person of Luxembourg so high?“ Davor hatte ich versehentlich `claude --permission-mode manual` ins Eingabefeld getippt. Den daraufhin vorgeschlagenen Testlauf habe ich abgelehnt. An Claude im Chat sinngemäß: mich durch Task 5 führen, eine Quelle heraussuchen, die README formulieren.
- **Was die KI gemacht hat:** Claude Code hat Tanktourismus, Grenzpendler, kleine Bevölkerung, Autoverkehr und Stahl als Gründe genannt, aber keine Zahlen, mit Verweis auf unsere `AGENTS.md`. Claude im Chat hat erkannt, dass `download.py` im frischen Klon scheitert, und die Korrekturzeile vorgeschlagen (`2612cbe`). Außerdem hat es die OECD-Quelle gesucht und den Text der `README.md` formuliert (Lizenz und Quellen aus dem OWID-README und dem Codebook).
- **Übernommen, geändert, verworfen:** Die Korrektur und die README habe ich übernommen. Die Entscheidung, die Antwort in Prozent (Dänemark) zu präsentieren, haben wir gemeinsam getroffen. Den Testlauf von Claude Code habe ich abgelehnt.
- **Wie geprüft:** `git log --oneline -- tests/` zeigt nur unseren Commit. Im frischen Klon lief die ganze Pipeline mit denselben Zahlen, danach habe ich den Klon gelöscht. Luxemburg habe ich mit dem Taschenrechner aus der Rohdatei nachgerechnet. Den OECD-Link habe ich selbst geöffnet und den Satz dort gefunden.

## 20.11.2026 · Task 6 · Bug-Hunt in `eu_report.py` (Melissa)

- **Rolle:** Die Punkte für den Review haben Idman und ich zusammen gesammelt. Idman war Driver beim Entwurf von `bug-hunt.md`, ich habe ihn geprüft, auf main geholt, ergänzt und die Agenten-Review auf meinem Mac durchgeführt.
- **Tool und Modell:** Claude (Anthropic) im Chat, eingestelltes Modell `claude-opus-5-5`, als Anleitung. Für Schritt 4 Claude Code mit Opus 5.5 in einer frischen Session, *auto mode* war an.
- **Prompt:** An Claude Code wörtlich aus der Aufgabe: „Review eu_report.py for data-handling bugs: anything that makes a number in the report or the chart wrong, although the script runs. Check each suspicion against the data in data/raw/. Do not change any file.“ An Claude im Chat sinngemäß: mich Schritt für Schritt durch Task 6 führen.
- **Was die KI gemacht hat:** Claude im Chat hat die Prüfsumme von `eu_report.py` mit dem Kurs-Repo verglichen und die Befehle für den Beleg zu Punkt 5 und die Prüfung einer Agenten-Zahl geschrieben. Bis Schritt 4 hat es unsere Punkte nicht bewertet, aber bei Punkt 6 empfohlen, ihn zu streichen, weil unser eigener Befehl 0 ergab. Die Texte für die Änderungen in Tabelle 1 und die ganze zweite Tabelle hat Claude formuliert, auch die Einstufung von „Imports“ als ungenaue Beschriftung statt als Fehler. Claude Code hat sechs Fehler gemeldet, den `dropna`-Fehler nur als „smaller point“, und dabei unsere schon committete `bug-hunt.md` gelesen.
- **Übernommen, geändert, verworfen:** Punkt 6 habe ich gestrichen und als Notiz „Checked, not an error“ behalten. Die Texte habe ich übernommen. Den Vorschlag von Claude Code, seine Review selbst in `bug-hunt.md` zu schreiben, habe ich nicht ausgeführt.
- **Wie geprüft:** Nach der Agenten-Review zeigte `git status` *working tree clean*. Zwei Zahlen des Agenten (Czechia −8,2 t, Dänemark 10,40 / 12,44 t) habe ich direkt in der Rohdatei ohne `eu_report.py` nachgerechnet, sie stimmen. Vor jedem Commit habe ich `git diff --stat` geprüft (`860fccb`, `e9f378a`).

## 20.11.2026 · Task 7 · Tests, Fixes und Vergleich (Melissa)

- **Rolle:** Idman war Driver in ihrem Codespace (Claude in Chrome hat getippt), ich war Navigator und habe vor jedem Push alles geprüft.
- **Tool und Modell:** Claude (Anthropic) im Chat, eingestelltes Modell `claude-opus-5-5`, als Anleitung.
- **Prompt:** sinngemäß: Claude soll mich durch Task 7 führen und mir die Nachrichten an Idman fertig schreiben („schreib mir direkt in der Nachricht alles, was Idman noch machen muss“).
- **Was die KI gemacht hat:** Die Tests für alle sechs Fehler hat Claude im Chat vorgeschlagen und formuliert, auch die Mini-Tabellen für `per_person` und `biggest_cuts`. Ich habe sie an Idman weitergegeben, die Tests sind also nicht von uns selbst ausgedacht. Claude hat außerdem empfohlen, den 27-Länder-Test erst ab `BASE_YEAR` zu prüfen und bei den Importen das letzte Jahr mit Konsumdaten (2023) zu zeigen statt „nan“. Das Fazit in `bug-hunt.md` hat Claude formuliert. Die Fixes hat Idmans Claude geschrieben.
- **Übernommen, geändert, verworfen:** Die Testideen, beide Empfehlungen und das Fazit habe ich übernommen.
- **Wie geprüft:** Bei jedem Fehler war der Test erst rot und nach dem Fix grün (am Ende 16 passed). Die Zahlen in `report_after.txt` habe ich mit unabhängigen Werten verglichen: 3.870 Mt wie die Zeile `European Union (27)`, 9,2 t pro Person wie deren `co2_per_capita`, 17,0 % wie `share_global_co2`, 817 Mt wie `trade_co2`. Das Diagramm habe ich angeschaut: Die Achse beginnt bei 0 und ist in Mt beschriftet.

  ## 20.11.2026 · Task 6 · Bug hunt (Idman)

- **Rolle:** Melissa und ich haben das Skript zusammen geprüft. Ich war Driver in meinem Codespace.
- **Tool und Modell:** ChatGPT (Modell: …) zum Umformulieren. Claude (Anthropic), eingestelltes Modell `claude-opus-5-5`. Die Schritte habe ich eins zu eins in meinem Codespace nachgemacht.
- **Prompt:** An ChatGPT: unsere gesammelten Verdachtspunkte mit der Bitte, sie besser zu formulieren. An Claude: „mach es“ und danach unsere Prüfbefehle.
- **Was die KI gemacht hat:** ChatGPT hat unsere Punkte umformuliert. Claude hat die Schritte vorgegeben, ich habe sie eins zu eins ausgeführt: `eu_report.py` 1:1 aus dem Kurs-Repo übernommen (SHA-256 `230ba4d7…`), den Bericht ausgeführt, nach Melissas Okay committet (`377efcd`, `af3d103`) und unsere Prüfbefehle ausgeführt. Aus unseren Notizen und den Ausgaben hat Claude die Tabelle für `bug-hunt.md` formuliert, die ich eingefügt habe (Branch `bug-hunt-draft`, `dfef863`). Claude hat nicht bewertet, ob ein Punkt ein Fehler ist.
- **Übernommen, geändert, verworfen:** Die Tabelle übernommen. Melissa hat einen Beleg für Punkt 5 ergänzt und Punkt 6 gestrichen („checked, not an error“), weil unser Befehl 0 ergab.
- **Wie geprüft:** Prüfsumme mit dem Original verglichen. Jede Zahl in der Tabelle kommt aus einem Befehl, den wir ausgeführt haben. Melissa hat `bug-hunt.md` vor dem Merge gelesen.

## 20.11.2026 · Task 7 · Tests und Fixes (Idman)

- **Rolle:** Ich war Driver, Melissa Navigator. Ich habe die Schritte eins zu eins in meinem Codespace nachgemacht.
- **Tool und Modell:** Claude (Anthropic), eingestelltes Modell `claude-opus-5-5`. Die Schritte habe ich eins zu eins nachgemacht. Die Testideen kamen von Claude in Melissas Chat.
- **Prompt:** Melissas Vorgaben pro Fehler (Test, Fix, Commit-Nachricht), jeweils wörtlich weitergegeben.
- **Was die KI gemacht hat:** Die Testideen kamen von Claude in Melissas Chat, nicht von uns selbst. Mein Claude hat die Tests und Fixes geschrieben und die Schritte vorgegeben. Ich habe sie eins zu eins ausgeführt: Tests eingegeben, gezeigt, dass sie fehlschlagen, Fixes eingefügt, den Bericht nach jedem Fix mit dem vorherigen verglichen und nach Melissas Okay committet (`b929f9b`, `8c70c00`, `d73df11` bis `504b172`, `3d61c0e`).
- **Übernommen, geändert, verworfen:** Fixes übernommen. Geändert: Melissas Test für 27 Länder prüft jetzt nur Jahre ab `BASE_YEAR`, weil es vor 1850 keine 27 Länder in der Datei gibt. Die Importzeile nimmt das letzte Jahr mit Konsumdaten (2023) statt „nan“.
- **Wie geprüft:** Jeder Test erst rot, dann grün, am Ende 16 passed. Der Bericht nach jedem Fix mit dem vorherigen verglichen (dabei die Falle gefunden: ohne `min_count=1` wurden die Importe 2024 negativ, −2.426 Mt). Melissa hat alle Commits vor dem Push geprüft.
