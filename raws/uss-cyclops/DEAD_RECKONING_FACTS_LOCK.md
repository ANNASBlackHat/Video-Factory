# DEAD RECKONING — USS CYCLOPS SHORT: FACTS LOCK

**Purpose:** the single contract every on-screen number, VO line, and caption must obey.
**Rule:** no number/name/date may appear in the composition unless it greps true against this table and its source.
**Scope:** the **Short** ("The Ship That Wasn't Sunk by a U‑Boat", ~45–55s), cross-posting the verdict.

## Source key

| ID | Source | Tier | Notes |
|----|--------|------|-------|
| **R1** | `USS Cyclops Disappearance Research.pdf` — *Forensic Assessment of the Loss of USS Cyclops (AC-4): Operational Audit, Naval Architecture, and the Physics of Catastrophic Failure* (16-pg forensic) | Primary/documentary | Authoritative; includes NHHC/DANFS, BdU KTB war-diaries, Barbados port, weather |
| **R2** | `Excellent choice. _Dead Reckoning_ gives you a lot.pdf` — Episode-1 blueprint + fact-check plan | Secondary/planning | Flags claims to verify; e.g. ore density `~4.5 t/m³` |
| **E1** | `Dead_Reckoning_Ep1_USS_Cyclops_Script.md` — full episode script | Production | Derived from R1/R2; source cards; verdict |
| **S1** | `Dead_Reckoning_Ep1_USS_Cyclops_short_script.md` — the Short | Production | The copy being voiced |

## Locked facts

| # | Claim (VO / on-screen) | Exact value | Source | Risk / note |
|---|------------------------|-------------|--------|-------------|
| F1 | It was a **US Navy ship** | USS Cyclops, **AC-4**, a **collier** (fleet fuel ship No. 4) | R1 Intro, R1 Voyage Record | Neutrally phrased in Short as "US Navy ship ... called the Cyclops" |
| F2 | **306 people** vanished | 306 crew + passengers (incl. **15 naval officers**) | R1 Intro & Voyage Record | On-screen "306 people" is safe; strictly 306 crew+passengers |
| F3 | Disappeared **1918**, in **March** | March 1918 (departed ~Mar 4; overdue Mar 13) | R1 | Confirmed |
| F4 | Largest peacetime loss in US naval history | Single largest loss of life in U.S. naval history **not directly involving combat** | R1 Intro | Keep the "not combat" qualifier for accuracy |
| F5 | Ship was **542 ft** steel | 542-foot steel vessel | R1, E1 | Optional on-screen; low risk |
| F6 | **No distress call** / no wreckage | No radio distress; no floating wreckage, lifeboats, or remains | R1 | Confirmed |
| F7 | Carried **10,800 tons of manganese ore** | 10,800 **long tons** commercial manganese ore (inbound); designed/outbound coal was 9,960 long tons | R1 Voyage Record | Use "10,800 tons" |
| F8 | Ore **5× denser than coal** | Manganese ore ≈ **4.5 t/m³** (R2) vs bituminous coal ≈ **0.9 t/m³** → **~5× denser** | R2 (density) + E1/S1 ("five times denser") | **Derived, minor risk.** Phrase as script: "five times denser than the coal she was built for". Do not sharpen to a precise ratio on screen. |
| F9 | **One of two engines broken** | Starboard engine disabled — **fractured high-pressure cylinder**; max speed cut **14.6 → 8–10 knots** | R1 timeline + failure-mode | Confirmed; Short says "one of her two engines was broken" |
| F10 | **Waterline underwater** leaving port | **Plimsoll mark fully submerged** at departure from Bridgetown, Barbados (overload) | R1 | Confirmed; Short: "waterline mark was fully underwater when she left port" |
| F11 | **Zero German subs** near her | **Zero Imperial German submarines operated west of the 40th meridian** in March 1918 | R1 | Confirmed; Long-range U-boats (U-Kreuzer) not in Caribbean/N.Atlantic |
| F12 | First U-boat reached US waters **May 15, 1918** | **U-151** — arrived off the Virginia coast **May 15, 1918** (>2 months after) | R1 + E1 | Optional supporting beat |
| F13 | **No one claimed the kill** | No U-boat commander claimed her; a torpedo/mining strike would have left debris/oil-slick signature — none found | R1 (no signature) + E1 (no claim) | Confirm with R1 if possible; E1 states it plainly |
| F14 | She sailed into a **gale** | **Force 8–10 gale**, winds 35–50 kt, off the Virginia Capes, **March 9–10, 1918** | R1 | Confirmed; Short: "Then she sailed straight into a gale" |
| F15 | Verdict **PROBABLE** | Case status **PROBABLE (~75%)** | E1 | Confirmed; the wreck was never found — honest caveat |
| F16 | (supporting) **Sister ships Proteus & Nereus** also lost carrying dense ore | Proteus (AC-9) & Nereus (AC-10), both lost in late 1941 carrying dense **bauxite** ore — class precedent | R1 | Optional supporting point; do NOT include if it pulls runtime |

## Route / timeline (background, not necessarily on-screen)

- Feb 16 1918 — departs Rio de Janeiro; starboard engine disabled (cracked cylinder), 10 kt cap.
- Feb 20 — reaches Salvador (Bahia), completes loading 10,800 LT manganese ore.
- Feb 22 — departs Bahia, nonstop course declared for Baltimore, MD.
- Mar 3 — unscheduled stop Bridgetown, Barbados; takes on 600 tons bunker coal + rations.
- ~Mar 4 — departs Barbados; Plimsoll mark fully submerged (last confirmed sighting).
- Mar 9–10 — Force 8–10 gale strikes east of the Virginia Capes.
- Mar 13 — ETA Baltimore passes; vessel declared overdue.
- Apr 16, 1918 — Asst. Secretary of the Navy **Franklin D. Roosevelt** declares ship lost with all hands.
- R1

## Build-time rule (carry into Phase 5/6)
- Every numeral in the composition must appear in `DEAD_RECKONING_FACTS_LOCK.md` → verified at lint/QA (`grep` audit).
- Numbers are double-checked both directions: transcript→script (what was *said*), script→facts (what was *meant*).
- On-screen source cards (Tier 1/2): NHHC loss summary · USN postwar review *German Submarine Activities on the Atlantic Coast* · US Weather Bureau *Monthly Weather Review*, March 1918 · Proteus-class sister-ship record.