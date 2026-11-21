#!/usr/bin/env python3
"""Generate the per-app privacy / terms / support pages served by GitHub Pages.

One entry per app in APPS; every claim here is checked against the app's
project.yml, Info.plist, PrivacyInfo.xcprivacy and store/metadata.md (see the
"facts" lists in each entry). Prices come from studio/aso/pricing.json — do not
invent them here; copy the four numbers from that file.

    python3 build.py            # writes <slug>/{privacy,terms,support}/index.html
    python3 build.py --check    # fails if any slug lacks one of the three pages

Served at https://nguyenanhducdeveloper86.github.io/legal/<slug>/<page>/
"""
from __future__ import annotations

import sys
from pathlib import Path

EMAIL = "nguyenanhducdeveloper@gmail.com"
EULA = "https://www.apple.com/legal/internet-services/itunes/dev/stdeula/"
APPLE_PRIVACY = "https://www.apple.com/legal/privacy/"
REPORT_PROBLEM = "https://reportaproblem.apple.com"
GOOGLE_PARTNER = "https://policies.google.com/technologies/partner-sites"
FIREBASE_PRIVACY = "https://firebase.google.com/support/privacy"
REVENUECAT_PRIVACY = "https://www.revenuecat.com/privacy"
UPDATED = "19 November 2026"

STYLE = (
    ':root{color-scheme:light dark}'
    'body{font:16px/1.65 -apple-system,BlinkMacSystemFont,"Segoe UI",system-ui,sans-serif;'
    'max-width:46rem;margin:0 auto;padding:2.5rem 1.25rem 5rem}'
    'h1{font-size:1.9rem;margin:0 0 1rem}'
    'h2{font-size:1.25rem;margin:2.2rem 0 .6rem}'
    'h3{font-size:1.05rem;margin:1.6rem 0 .4rem}'
    'p,li{margin:0 0 .8rem}'
    'ul{padding-left:1.1rem}'
    'table{border-collapse:collapse;width:100%;margin:0 0 1rem}'
    'th,td{text-align:left;padding:.45rem .5rem;border-bottom:1px solid rgba(128,128,128,.35)}'
    'code{font-size:.9em}'
    'nav a{margin-right:1rem}'
    'a{color:#0b62d6}'
)

# ---------------------------------------------------------------- app facts
# analytics/crash/ads/tracking are the *linked* SDKs, not the shared Integrations
# source: every app ships Integrations/*.swift, but only these link the SDK.
APPS = [
    dict(
        slug="voltcalc", name="VoltCalc",
        purpose="VoltCalc does voltage drop, wire ampacity and conduit fill to the NEC, and cites the table next to every number.",
        local=[
            "Voltage drop from source voltage, load current, run length and conductor size, for single or three phase, copper or aluminum.",
            "Ampacity from NEC Table 310.16 at 60, 75 and 90 °C for AWG 14 to 1000 kcmil, with the 310.15(C)(1) adjustment when more than three current-carrying conductors share a raceway.",
            "Conduit fill percentage against the Chapter 9 Table 1 limits.",
            "A PDF record of a saved calculation, created on the device and shared only when you share it.",
        ],
        free="VoltCalc works without a purchase; Pro unlocks unlimited saved calculations and PDF job records.",
        prices=dict(weekly="$2.99", monthly="$6.99", yearly="$29.99", lifetime="$59.99"),
        analytics=False, crash=False, ads=False, tracking=False,
        disclaimer=(
            "<p><strong>Not professional advice.</strong> VoltCalc performs published NEC formulas and table lookups. "
            "It is not electrical design, is not a substitute for a licensed electrician or a stamped design, and "
            "does not replace your jurisdiction's adopted code book. Local amendments can change the requirements. "
            "Every result shows the formula and the table it came from so a qualified person can check it.</p>"
        ),
        faq=[
            ("A result looks wrong.",
             "Every calculation prints the formula and the NEC table it used. Check the inputs against the code edition "
             "your jurisdiction adopts. If a value still looks wrong, email us the app version, the inputs and the result "
             "shown — we treat those reports as bugs."),
            ("Does it work offline?",
             "Yes. All three calculations run on the phone; no network is used for them."),
            ("How do I keep a calculation?",
             "Save the record, then share or export its PDF from the record screen. The PDF stays on your device until you "
             "send it somewhere yourself."),
        ],
    ),
    dict(
        slug="dosecalc", name="DoseCalc",
        purpose="DoseCalc does IV drip rate, weight-based dose and dilution, and prints the formula and the substituted numbers next to every answer.",
        local=[
            "IV drip rate from volume, infusion time and drop factor (10, 15, 20 or 60 gtt/mL).",
            "Dose by weight from ordered mg/kg, patient weight in kilograms or pounds, and the concentration on the vial.",
            "Dilution, C1 × V1 = C2 × V2, solved for whichever term you leave blank.",
            "A one-page PDF record of a saved calculation, created on the device.",
        ],
        free="DoseCalc works without a purchase; Pro unlocks unlimited saved calculations and PDF records.",
        prices=dict(weekly="$2.99", monthly="$6.99", yearly="$29.99", lifetime="$59.99"),
        analytics=False, crash=False, ads=False, tracking=False,
        disclaimer=(
            "<p><strong>Not professional advice, and not a protocol.</strong> DoseCalc is an arithmetic aid. It does not "
            "replace your hospital's policies, a pharmacist's verification or clinical judgment, and it is not a dosing "
            "reference. Double-check every calculation before a dose is administered. Do not use it for neonates or "
            "infants unless you have verified the dose against a neonatal reference.</p>"
        ),
        faq=[
            ("A result looks wrong.",
             "Every result prints the formula and the numbers substituted into it. Recheck the units first — gtt/mL of the "
             "set in hand changes the drip rate. Email us the app version, the inputs and the result shown if it still "
             "looks wrong."),
            ("Does it work offline?",
             "Yes. All three calculations run on the phone."),
            ("Can I record what I calculated?",
             "Save the calculation and share it as a one-page PDF from the record screen."),
        ],
    ),
    dict(
        slug="ductcalc", name="DuctCalc",
        purpose="DuctCalc sizes ductwork from airflow and velocity: the round diameter, the matching rectangle, and a warning when velocity leaves the supply or return band.",
        local=[
            "Round diameter from CFM and fpm (A = CFM ÷ fpm, D = 12 × √(4A ÷ π)) in inches and millimetres.",
            "Rectangular equivalent for the same area at an aspect ratio from 1:1 to 4:1.",
            "Velocity warnings against 600–1200 fpm for supply and 1200–1600 fpm for return.",
            "CMF or m³/h in, fpm or m/s out, chosen in the app.",
            "A local job log of saved sizes, shared as text only when you share it.",
        ],
        free="DuctCalc works without a purchase; Pro unlocks unlimited saved duct sizes and the job log.",
        prices=dict(weekly="$2.99", monthly="$6.99", yearly="$29.99", lifetime="$59.99"),
        analytics=False, crash=False, ads=False, tracking=False,
        disclaimer=(
            "<p><strong>Not professional advice.</strong> DuctCalc is sizing only. It does not perform a Manual J load "
            "calculation, does not total fitting pressure drop and does not choose a friction rate. It is not a stamped "
            "Manual D design and is not a substitute for a licensed HVAC contractor. Velocity bands follow common ACCA "
            "Manual D practice; your jurisdiction and your engineer's specification govern.</p>"
        ),
        faq=[
            ("Why does it not tell me how much air a room needs?",
             "That is a load calculation (Manual J), which DuctCalc does not do. Enter the CFM from your own load calculation "
             "or equipment schedule."),
            ("A velocity warning fired.",
             "The band shown is 600–1200 fpm for supply and 1200–1600 fpm for return. A warning is information, not a "
             "verdict — the design specification wins."),
            ("How do I share a size?",
             "Save it to the job log, then share the log as text."),
        ],
    ),
    dict(
        slug="pdfsqueeze", name="PDFSqueeze",
        purpose="PDFSqueeze compresses a PDF to a size you choose, on the device, keeping the sharpest file that still fits.",
        local=[
            "Pick a target from 50 KB to 5 MB; each page is rendered at several scales and JPEG qualities and the biggest "
            "file that still fits the target is kept.",
            "Before and after size, percentage saved and page count on the result screen.",
            "The compressed file is handed to the iOS share sheet; you choose where it goes.",
            "Compression rasterises pages, so selectable text, links and form fields do not survive it.",
        ],
        free="Three compressions are free. Pro unlocks unlimited compressions at any target size.",
        prices=dict(weekly="$2.99", monthly="$4.99", yearly="$19.99", lifetime="$39.99"),
        analytics=False, crash=False, ads=False, tracking=False,
        disclaimer=None,
        faq=[
            ("My text is no longer selectable.",
             "Compression turns each page into an image — that is how the file gets smaller. Keep the original if you need a "
             "searchable document."),
            ("It says the target cannot be reached.",
             "Very small targets on long documents can drop below readable quality. Raise the target, or split the document "
             "and compress the pages you need to shrink."),
            ("Is anything uploaded?",
             "No. PDFSqueeze reads and writes only files you pick, and it works in airplane mode."),
        ],
    ),
    dict(
        slug="contactshelf", name="ContactShelf",
        purpose="ContactShelf exports your iPhone address book as CSV or vCard, with the columns you tick, without an account or an upload.",
        local=[
            "Choose fields (name, company, title, phone, email, postal address, birthday), preview the rows, then export.",
            "CSV with RFC 4180 quoting and UTF-8, so accented names and commas survive Excel, Numbers and Google Sheets.",
            "vCard 3.0 (.vcf) for Apple Contacts, Google Contacts and Outlook.",
            "Long address books are split into numbered files of 500 contacts.",
        ],
        free="The first 25 contacts of the address book export free. Pro exports the whole address book, in files of 500 contacts.",
        prices=dict(weekly="$1.99", monthly="$3.99", yearly="$14.99", lifetime="$24.99"),
        analytics=False, crash=False, ads=False, tracking=False,
        lines=[
            "<p><strong>Contacts permission is used on the device only.</strong> ContactShelf asks for read access to your "
            "contacts so it can build the CSV or vCard file. It reads them, writes the export to a file on the phone, and "
            "sends nothing anywhere. It never edits, creates or deletes a contact. Revoke the permission at any time in "
            "iOS Settings → Apps → ContactShelf → Contacts; the app then cannot read the address book and cannot export.</p>",
        ],
        disclaimer=None,
        faq=[
            ("Nothing exports.",
             "Check iOS Settings → Apps → ContactShelf → Contacts. Without read access the app has nothing to export. "
             "Full access is required; limited access shows only the contacts you selected."),
            ("Where does the exported file go?",
             "Wherever you send it from the share sheet — Files, Mail, AirDrop, another app. ContactShelf does not keep a "
             "copy on a server because there is no server."),
            ("Is this a backup?",
             "It is an export tool. Keep the exported file somewhere safe, and check an export before importing it into "
             "another address book."),
        ],
    ),
    dict(
        slug="permitprep", name="PermitPrep",
        purpose="PermitPrep is practice for the California learner's permit test: 150 hand-written questions, 40 per session, progress saved on the phone.",
        local=[
            "Sessions draw 40 questions from 150, each with four answers, one correct choice and a short explanation.",
            "Every answer is saved on the device, so a session resumes where you stopped.",
            "Ten handbook topics, from right-of-way and signs to BAC limits, sharing the road and licence penalties.",
            "Only the California set is available in this version; other states are marked as coming and are not sold as content.",
        ],
        free="One practice session a day is free. Pro removes the daily session limit for the content that is available; it does not add states or questions that this build does not contain.",
        prices=dict(weekly="$2.99", monthly="$6.99", yearly="$19.99", lifetime="$29.99"),
        analytics=False, crash=False, ads=False, tracking=False,
        disclaimer=(
            "<p><strong>Not affiliated with any DMV.</strong> PermitPrep is an independent study aid. It is not affiliated "
            "with, endorsed by, or connected to the California Department of Motor Vehicles or any other state agency. "
            "Questions are written from the published California Driver's Handbook; they are not the official exam, and a "
            "score in this app is not an official pass or fail. Always check the current handbook and your state's rules.</p>"
        ),
        faq=[
            ("Where are the other 49 states?",
             "Not in this version. The state picker shows them as unavailable, and no purchase unlocks them."),
            ("The daily session limit reset.",
             "One session per day is free. A Pro purchase removes the limit."),
            ("Are these the real exam questions?",
             "No. They are hand-written practice questions based on the published handbook, and the app says so."),
        ],
    ),
    dict(
        slug="lexi6k", name="Lexi6k",
        purpose="Lexi6k is 6,000 English vocabulary flashcards with spaced repetition and Vietnamese meanings, offline.",
        local=[
            "6,000 word cards in the app bundle, with meanings from an open CC BY-SA 4.0 dictionary; audio is the system voice.",
            "Spaced repetition schedules each card from your own answers.",
            "Progress and settings are stored on the phone.",
            "Free tier: set 1 (1,000 words) and 20 new words a day.",
        ],
        free="Set 1 (1,000 words) and 20 new words a day are free. Pro unlocks sets 1–6 (6,000 words) and 60 new words a day.",
        prices=dict(weekly="$2.99", monthly="$6.99", yearly="$29.99", lifetime="$49.99"),
        analytics=True, crash=True, ads=False, tracking=False,
        disclaimer=None,
        faq=[
            ("My purchase did not unlock the full word list.",
             "Open the unlock screen and tap Restore Purchases. Make sure the device is signed in with the same Apple "
             "Account that bought it."),
            ("Can I study offline?",
             "Yes. All 6,000 cards ship inside the app; no download and no account are needed."),
            ("Where do the Vietnamese meanings come from?",
             "An open dictionary published under CC BY-SA 4.0. The About screen names it."),
        ],
    ),
    dict(
        slug="quietqr", name="QuietQR",
        purpose="QuietQR generates QR codes for Wi-Fi, contacts, links, events and more, entirely on the phone.",
        local=[
            "Ten code types: Wi-Fi (WPA/WEP/open, hidden networks), vCard 3.0, MECARD, URL, text, email, SMS, phone, "
            "geo location and VEVENT.",
            "54 ready-made templates, editable after you pick one.",
            "Correct escaping of SSID and name characters; UTF-8, so Vietnamese diacritics survive a scan.",
            "Save the PNG to Photos, share it anywhere, and reopen past codes from a local history.",
        ],
        free="Five exports are free. Pro unlocks unlimited codes, all templates and the local history.",
        prices=dict(weekly="$1.99", monthly="$3.99", yearly="$14.99", lifetime="$24.99"),
        analytics=False, crash=False, ads=False, tracking=False,
        lines=[
            "<p><strong>Photos access is add-only.</strong> QuietQR asks for permission to add images to your photo library "
            "when you save a code. It cannot read, browse or modify the rest of your library, and nothing is uploaded.</p>",
            "<p><strong>No camera.</strong> QuietQR only creates codes. It does not scan codes and cannot read anyone else's "
            "code.</p>",
        ],
        disclaimer=None,
        faq=[
            ("A saved code is missing from Photos.",
             "Check iOS Settings → Apps → QuietQR → Photos. Add-only access is enough to save; without it, use the share "
             "sheet instead."),
            ("Does it scan QR codes?",
             "No. It is a generator. Use the iOS Camera app to scan."),
            ("Wi-Fi codes with a hidden network.",
             "Tick the hidden-network option in the Wi-Fi form; some scanners require it to join."),
        ],
    ),
    dict(
        slug="calmtiles", name="CalmTiles",
        purpose="CalmTiles is mahjong solitaire: 2,000 layouts generated on the device, unlimited undo, hints and shuffle, and no timer.",
        local=[
            "800 easy, 800 medium and 400 three-layer boards, each generated from a fixed seed and solvable by construction.",
            "Unlimited undo, a hint that follows a proven path to a cleared board, and a shuffle into a new solvable "
            "arrangement.",
            "Cleared levels and preferences stay on the phone.",
            "No timer and no accounts.",
        ],
        free="The game is free with ads. Pro removes all ad formats; it does not add boards, and nothing else is promised.",
        prices=dict(weekly="$0.99", monthly="$1.99", yearly="$9.99", lifetime="$14.99"),
        # project.yml declares FirebaseAnalytics/FirebaseCrashlytics in a second
        # "dependencies:" key, which YAML drops, and packages: lists only
        # google-mobile-ads — CalmTiles.xcodeproj has no Firebase reference, so
        # this build links AdMob only. Flip these two when the SDK is really linked.
        analytics=False, crash=False, ads=True, tracking=True, rewarded=True,
        disclaimer=None,
        faq=[
            ("How do I remove the ads?",
             "Buy the ad-free upgrade on the upgrade screen, then Restore Purchases on another device signed in with the same "
             "Apple Account. Ad-free does not add levels — every layout is already included."),
            ("A board looks impossible.",
             "Every board is solvable by construction. Undo as far back as you like, ask for a hint that follows a proven "
             "path, or shuffle the remaining tiles into a new solvable arrangement."),
            ("Can I turn off ad tracking?",
             "Yes. iOS Settings → Privacy & Security → Tracking. In the EEA and UK, Google's consent form appears before ads "
             "are requested the first time."),
        ],
    ),
    dict(
        slug="jigsawcalm", name="JigsawCalm",
        purpose="JigsawCalm is jigsaw puzzles: 40 photographs and 12 generated abstract scenes, three cuts each, progress saved per puzzle.",
        local=[
            "52 pictures — 40 photographs shipped in the app, 12 abstract scenes drawn on the device — and three cuts each "
            "(3×3, 4×4, 8×6).",
            "Pieces snap in when you get close; progress is saved per picture and per cut on the phone.",
            "Pictures and cuts are never downloaded; the game works in airplane mode.",
        ],
        free="The game is free with ads. Pro removes all ad formats; it does not add pictures or cuts, and nothing else is promised.",
        prices=dict(weekly="$0.99", monthly="$1.99", yearly="$9.99", lifetime="$14.99"),
        analytics=False, crash=False, ads=True, tracking=True, rewarded=False,
        disclaimer=None,
        faq=[
            ("How do I remove the ads?",
             "Buy the ad-free upgrade on the upgrade screen. On another device, sign in with the same Apple Account and tap "
             "Restore Purchases. Every picture and cut is already included either way."),
            ("My progress disappeared.",
             "Progress is per picture and per cut, stored on this phone. Deleting the app deletes it, and there is no cloud "
             "sync to restore it from."),
            ("Can I turn off ad tracking?",
             "Yes. iOS Settings → Privacy & Security → Tracking. In the EEA and UK, Google's consent form appears before ads "
             "are requested the first time."),
        ],
    ),
    dict(
        slug="quietsolitaire", name="QuietSolitaire",
        purpose="QuietSolitaire is FreeCell: numbered deals, unlimited undo and hints that name one legal move.",
        local=[
            "Numbered, seeded deals — the same number always restores the same 52 cards.",
            "Unlimited undo with no counter, and hints that name and highlight one legal move without playing it for you.",
            "No timer, no gambling, no chips, and no account.",
        ],
        free="The game is free with ads. Pro removes all ad formats; undo and hints are free and stay free.",
        prices=dict(weekly="$0.99", monthly="$1.99", yearly="$9.99", lifetime="$14.99"),
        analytics=False, crash=False, ads=True, tracking=True, rewarded=True,
        disclaimer=None,
        faq=[
            ("How do I remove the ads?",
             "Buy the ad-free upgrade on the upgrade screen, then Restore Purchases on another device signed in with the "
             "same Apple Account."),
            ("Can I play a specific deal again?",
             "Yes. Every deal is seeded, so deal 1287 is the same 52 cards in the same order on any device."),
            ("Is undo limited?",
             "No. Undo is unlimited and is not part of any purchase."),
        ],
    ),
    dict(
        slug="sudokuquiet", name="SudokuQuiet",
        purpose="SudokuQuiet is sudoku with exactly one solution per puzzle and hints that name the technique instead of printing the answer.",
        local=[
            "Puzzles generated on the phone by backtracking, with cells removed only while the puzzle keeps a single "
            "solution.",
            "Hints name the technique — naked single, hidden single, locked candidates — and show why it works.",
            "Levels are set by the deduction the puzzle forces, not by the number of blank cells.",
            "Pencil marks and unlimited undo, on the phone only. A clock counts up if you want it; nothing expires and "
            "nothing fails you when it runs long.",
        ],
        free="The game is free with ads. Pro removes all ad formats; hints, levels and undo are free and stay free.",
        prices=dict(weekly="$0.99", monthly="$1.99", yearly="$9.99", lifetime="$14.99"),
        analytics=False, crash=False, ads=True, tracking=True, rewarded=True,
        disclaimer=None,
        faq=[
            ("How do I remove the ads?",
             "Buy the ad-free upgrade on the upgrade screen, then Restore Purchases on another device signed in with the "
             "same Apple Account."),
            ("The hint does not give me a number.",
             "That is deliberate. A hint names the technique and the cells, so you find the number yourself."),
            ("Can I turn off ad tracking?",
             "Yes. iOS Settings → Privacy & Security → Tracking. In the EEA and UK, Google's consent form appears before ads "
             "are requested the first time."),
        ],
    ),
    dict(
        slug="fruitfizz", name="Fruit Fizz: Match Quest",
        purpose="Fruit Fizz is a soda-bar match-3: swap neighbouring fruits, clear the order and watch the glass fizz over.",
        local=[
            "Eight-by-eight boards of six fruit shapes; swap two neighbours to line up three or more and the matches "
            "clear, fruit falls and new fruit fills in.",
            "Four in a line leaves a row or column fizz, crossing lines leave a bomb, five in a line leaves a colour burst.",
            "200 levels, each measured by a practice bot and tuned until it sits in its own difficulty band; a breather "
            "every tenth level and a badge on every twenty-fifth.",
            "Goals are an order of one fruit, jelly tiles to clear or crates to drop to the floor. Each board has a move "
            "budget and no timer.",
            "The board is seeded, so the same moves always replay to the same board; when no swap is left the board "
            "shuffles instead of ending the round.",
            "Coins are earned by finishing levels and by the daily reward, and are spent on hints and undo pockets. "
            "Progress, coins and settings stay on the phone.",
        ],
        free=("The game is free with ads. Remove Ads is one payment that stops every ad format; the Starter Pack adds coins "
              "and undo pockets. No purchase unlocks a level — all 200 are already in the app."),
        prices=dict(removeads="$3.99", starter="$2.99",
                    coins_small="$1.99", coins_medium="$4.99", coins_large="$9.99"),
        subs=False,
        analytics=False, crash=False, ads=True, tracking=True, rewarded=True,
        disclaimer=None,
        faq=[
            ("How do I remove the ads?",
             "Buy Remove Ads on the shop screen, then Restore Purchases on another device signed in with the same Apple "
             "Account. It stops ad requests for good; levels, coins and hints are unchanged otherwise."),
            ("A board feels impossible.",
             "Each board has a move budget measured by a bot, so it has been finished inside that budget. Undo as far "
             "back as you like, spend 30 coins on a hint, or take the optional video for one after your first win."),
            ("I ran out of moves.",
             "The lose sheet offers five more moves for coins, or a rewarded video. Nothing expires and you can replay "
             "the level as often as you like."),
            ("Can I turn off ad tracking?",
             "Yes. iOS Settings → Privacy & Security → Tracking. In the EEA and UK, Google's consent form appears before "
             "ads are requested the first time, and declining still leaves non-personalised ads."),
            ("Where is my progress?",
             "On this phone only. There is no account and no cloud sync, so deleting the app deletes progress and coins."),
        ],
    ),
    dict(
        slug="llamalatin", name="Llama Lines: Latin Square",
        purpose=("Llama Lines is a latin-square number puzzle: every row, every column and every chained group of cells "
                 "holds each number from 1 to N exactly once."),
        local=[
            "Grids from 4x4 to 7x7. A chain hops sideways, up and diagonally, so the regions are drawn leashes rather "
            "than square boxes.",
            "Every level is generated on the phone with exactly one solution; a clue is dropped only while the solver can "
            "still prove the answer is unique.",
            "Hints place or repair one digit from that solution, undo covers every move, and pencil notes stay in the "
            "round until you clear them.",
            "No countdown timer: each level has a move budget shown as moves remaining. Progress, coins and settings are "
            "stored on the phone only.",
        ],
        free=("The game is free with ads. Remove Ads is one payment that stops every ad format; the Starter Pack adds coins "
              "and hints. No purchase unlocks a level — levels past 200 are generated in the app."),
        prices=dict(removeads="$3.99", starter="$2.99",
                    coins_small="$1.99", coins_medium="$4.99", coins_large="$9.99"),
        subs=False,
        analytics=False, crash=False, ads=True, tracking=True, rewarded=True,
        disclaimer=None,
        faq=[
            ("How do I remove the ads?",
             "Buy Remove Ads on the shop screen, then Restore Purchases on another device signed in with the same Apple "
             "Account. It stops ad requests for good; levels, coins and hints are unchanged otherwise."),
            ("What is a chain?",
             "A chain is one leash of N cells drawn across the grid. Those cells must also hold 1 to N once each, on top "
             "of the row and column rules."),
            ("Is it sudoku?",
             "No. Sudoku boxes are 3x3 squares; here a chain can bend and hop in eight directions, and the grid is 4x4 to "
             "7x7. The rule it shares with sudoku is the one about no repeats."),
            ("I ran out of moves.",
             "The lose sheet offers five more moves for coins, and you can replay the level as often as you like. "
             "Nothing expires."),
            ("Can I turn off ad tracking?",
             "Yes. iOS Settings → Privacy & Security → Tracking. In the EEA and UK, Google's consent form appears before "
             "ads are requested the first time, and declining still leaves non-personalised ads."),
            ("Where is my progress?",
             "On this phone only. There is no account and no cloud sync, so deleting the app deletes progress and coins."),
        ],
    ),
    dict(
        slug="noodleconnect", name="NoodleConnect",
        purpose="NoodleConnect is a number-link puzzle: 1,000 bowls of 5×5 to 7×7 where every meatball is joined to its twin "
                "and every level ships with exactly one solution.",
        local=[
            "1,000 levels, each generated on the device and checked by a solver to have exactly one solution before it is "
            "handed to a player.",
            "Three bowl sizes — 5×5, 6×6 and 7×7 — that grow as you finish levels.",
            "Drag from one meatball to its twin; noodles never cross and the bowl is full when every cell is covered.",
            "A hint that draws one whole noodle, unlimited undo, restart, and a pause that keeps the round you are in.",
            "Coins for finishing a level for the first time, spent on hints, undos and two extra noodle colours. No timer.",
        ],
        free="The game is free with ads. Every level, the hint and unlimited undo are free. The shop sells Remove Ads, a "
             "one-time Starter Pack (500 coins and 5 hints) and three coin packs; nothing in it is a subscription, and "
             "nothing expires.",
        subs=False,
        prices=dict(removeads="$3.99", starter="$2.99", coins_small="$1.99", coins_medium="$4.99", coins_large="$9.99"),
        analytics=False, crash=False, ads=True, tracking=True, rewarded=True,
        disclaimer=None,
        faq=[
            ("How do I remove the ads?",
             "Buy Remove Ads in the shop, or the Starter Pack, which also removes forced ads. On another device signed in "
             "with the same Apple Account, tap Restore purchases."),
            ("A bowl looks like it has two answers.",
             "It does not: every level is generated on the phone and only kept when a solver finds one solution. If a "
             "second answer really works, send us the level number — we treat it as a bug."),
            ("Can I buy coins twice?",
             "Yes, coin packs repeat as often as you like. Remove Ads and the Starter Pack are one-time purchases and stay "
             "active for the life of the Apple Account that bought them."),
            ("Can I turn off ad tracking?",
             "Yes. iOS Settings → Privacy & Security → Tracking. In the EEA and UK, Google's consent form appears before ads "
             "are requested the first time."),
        ],
    ),
    dict(
        slug="boomgarden", name="Boom Garden: No-Guess Mines",
        purpose=("Boom Garden is a deduction puzzle: dig the soil, read the seed-packet numbers and plant a flower on every "
                 "mole trap you can prove is buried there. No garden ever needs a lucky click."),
        local=[
            "Boards run from 8x8 up to 14x18 with three hearts per garden. A trap costs one heart and plays a cartoon "
            "boing; the round ends after the third, and retrying the same garden is free.",
            "All 200 gardens are run through a solver before they ship — single-cell logic, the pair rule and the "
            "end-game trap count. A garden that could not be finished without guessing is thrown out.",
            "Pinch to zoom between 1x and 3.5x and drag to pan the wide plots, with a chip that snaps the board back.",
            "A first clear pays 15 to 25 coins depending on stars. One hint costs 30 coins, three undos cost 20, and the "
            "daily worm fund pays 25 to 200 coins. Three cosmetic neckerchiefs are bought with earned coins.",
            "Progress, coins and settings stay in this app's own storage on the phone, with no account and no sync.",
        ],
        free=("The game is free with ads. Remove Ads is one payment that stops every ad format; the Starter Pack adds 500 "
              "coins and 5 hints. No purchase unlocks a level — all 200 are already in the app."),
        prices=dict(removeads="$3.99", starter="$2.99",
                    coins_small="$1.99", coins_medium="$4.99", coins_large="$9.99"),
        subs=False,
        analytics=False, crash=False, ads=True, tracking=True, rewarded=True,
        disclaimer=None,
        faq=[
            ("How do I remove the ads?",
             "Buy Remove Ads in Moley's tool shed, then Restore Purchases on another device signed in with the same Apple "
             "Account. It stops ad requests for good; gardens, coins and hints are unchanged otherwise."),
            ("A garden feels like a coin flip.",
             "It is not: every garden is finished by a solver using only provable moves before it ships, so there is "
             "always a next move you can prove. Send the level number if you find one that needs a guess — we treat it "
             "as a bug and replace the garden."),
            ("I ran out of hearts.",
             "The lose screen offers five spare hearts and one undo for 20 coins, an optional video, or a free retry of "
             "the same garden. Nothing expires."),
            ("Can I turn off ad tracking?",
             "Yes. iOS Settings → Privacy & Security → Tracking. In the EEA and UK, Google's consent form appears before "
             "ads are requested the first time, and declining still leaves non-personalised ads."),
            ("Where is my progress?",
             "On this phone only. There is no account and no cloud sync, so deleting the app deletes progress and coins."),
        ],
    ),
    dict(
        slug="lamplab", name="Lamp Lab: Light Up Puzzle",
        purpose=("Lamp Lab is a lamp-placement logic puzzle: hang bulbs until every cell is lit, keep bulbs out of each "
                 "other's line of sight, and match the number on every wall."),
        local=[
            "Akari rules on boards from 7x7 to 10x10: a bulb lights its row and column until a wall stops the beam, a "
            "numbered wall wants exactly that many bulbs beside it, and two bulbs may never see each other.",
            "Each level is generated on the phone from its own number with a fixed seed, so level 37 is the same board "
            "on every launch and on any phone. The trail has no fixed end.",
            "A hint highlights one bulb of a proven solution, undo is unlimited and free, and a first clear pays coins.",
            "Progress, stars, coins and settings stay in this app's own storage on the phone, with no account and no sync.",
        ],
        free=("The game is free with ads. Remove Ads is one payment that stops every ad format; the Starter Pack adds 500 "
              "coins and 5 hints, and the three coin packs are optional. No purchase unlocks a level."),
        prices=dict(removeads="$3.99", starter="$2.99",
                    coins_small="$1.99", coins_medium="$4.99", coins_large="$9.99"),
        subs=False,
        analytics=False, crash=False, ads=True, tracking=True, rewarded=True,
        disclaimer=None,
        faq=[
            ("How do I remove the ads?",
             "Buy Remove Ads in Watts' supply bench, then Restore Purchases on another device signed in with the same "
             "Apple Account. It stops banner and interstitial requests for good; optional reward videos stay optional."),
            ("The board will not light up.",
             "Every level is solved by the app's own solver before the light is drawn, so a solvable answer always "
             "exists. Check the wall numbers first — a hidden number still applies — and tap Hint for one bulb that "
             "belongs. Send the level number if a board still looks impossible; we treat it as a bug."),
            ("Do I need a subscription?",
             "No. There is no subscription in this app. Every purchase is charged once, and the free game plays every "
             "level in the trail."),
            ("Can I turn off ad tracking?",
             "Yes. iOS Settings → Privacy & Security → Tracking. In the EEA and UK, Google's consent form appears before "
             "ads are requested the first time, and declining still leaves non-personalised ads."),
            ("Where is my progress?",
             "On this phone only. There is no account and no cloud sync, so deleting the app deletes progress and coins."),
        ],
    ),
    dict(
        slug="traffictantrum", name="Traffic Tantrum: Unblock",
        purpose=("Traffic Tantrum is a slide-the-traffic puzzle: nudge the toy cars along their own lanes until the "
                 "grumpy red car rolls out of the exit."),
        local=[
            "Tap or drag a car and it rolls as far as its lane allows. Vehicles only move along their own line, and the "
            "run ends when the hero car leaves the right edge of the yellow row.",
            "Every jam is built on the phone from the level number with a fixed seed, then solved by a breadth-first "
            "search that proves the shortest route, so level 37 is the same jam on every launch and on any phone. The "
            "trail has no fixed end.",
            "Stars follow the move count against that proven shortest route; each level has a move budget and no timer.",
            "A hint highlights one move of a proven solution, undo pockets are spent one at a time, a first clear pays "
            "coins and the map pays a daily bonus. Optional reward videos can pay a free hint, five extra moves or double "
            "a win.",
            "Progress, stars, coins and settings stay in this app's own storage on the phone, with no account and no sync.",
        ],
        free=("The game is free with ads. Remove Ads is one payment that stops every ad format; the Starter Pack adds 500 "
              "coins and 5 hints, and the three coin packs are optional. No purchase unlocks a level."),
        prices=dict(removeads="$3.99", starter="$2.99",
                    coins_small="$1.99", coins_medium="$4.99", coins_large="$9.99"),
        subs=False,
        analytics=False, crash=False, ads=True, tracking=True, rewarded=True,
        disclaimer=None,
        faq=[
            ("How do I remove the ads?",
             "Buy Remove Ads in the shop, then Restore Purchases on another device signed in with the same Apple Account. "
             "It stops banner and interstitial requests for good; optional reward videos stay optional."),
            ("The jam looks impossible.",
             "Every jam is solved by the app's own solver before it is drawn, so a route always exists. Tap Hint for the "
             "next move of a proven one. If a level still looks stuck, send the level number; we treat it as a bug."),
            ("Do I need a subscription?",
             "No. There is no subscription in this app. Every purchase is charged once, and the free game plays every "
             "level in the trail."),
            ("Can I turn off ad tracking?",
             "Yes. iOS Settings → Privacy & Security → Tracking. In the EEA and UK, Google's consent form appears before "
             "ads are requested the first time, and declining still leaves non-personalised ads."),
            ("Where is my progress?",
             "On this phone only. There is no account and no cloud sync, so deleting the app deletes progress, stars and "
             "coins."),
        ],
    ),
    dict(
        slug="hamsterhaul", name="Hamster Haul",
        purpose=("Hamster Haul is a crate-pushing puzzle: nudge Biscuit the hamster around a snack warehouse until every "
                 "wooden crate sits on a glowing dot. Walking is free and only a push spends the move budget."),
        local=[
            "One to four crates in rooms from 6×6 to 9×9. The level you open is generated on the phone from its number "
            "and solved by the app's own search before it is drawn, so a route always exists and level 37 is the same "
            "warehouse on every launch. The trail has no fixed end.",
            "Stars follow the push count against the level's proven best. There is no timer, and every tenth level is "
            "pitched at the easy end of its band as a breather.",
            "A hint shows the next push of a proven route and undo steps back one push; both are paid from coins, and "
            "coins are earned for free as well.",
            "Finishing a level pays coins, the daily snack tin pays 25 to 200 coins across a seven-day streak, and coins "
            "also buy the mint and sunset hamster coats. Optional reward videos can pay a hint, double a win or double "
            "the daily reward.",
            "Progress, stars, coins and settings stay in this app's own storage on the phone, with no account and no "
            "sync.",
        ],
        free=("The game is free with ads. Remove Ads is one payment that stops every ad format; the Starter Pack adds 500 "
              "coins and 5 hints; the three coin packs are optional. No purchase unlocks a level."),
        prices=dict(removeads="$3.99", starter="$2.99",
                    coins_small="$1.99", coins_medium="$4.99", coins_large="$9.99"),
        subs=False,
        analytics=False, crash=False, ads=True, tracking=True, rewarded=True,
        disclaimer=None,
        faq=[
            ("How do I remove the ads?",
             "Buy Remove Ads in the snack pantry, then Restore Purchases on another device signed in with the same Apple "
             "Account. It stops banner and interstitial requests for good; optional reward videos stay optional."),
            ("A crate is stuck in a corner.",
             "Undo steps back one push, and a hint shows the next push of the route the app proved before it drew the "
             "room. Nothing in this game needs a purchase to be cleared; if a level still looks stuck, send the level "
             "number and we treat it as a bug."),
            ("Do I need a subscription?",
             "No. There is no subscription in this app. Every purchase is charged once, and the free game plays every "
             "level in the trail."),
            ("Can I turn off ad tracking?",
             "Yes. iOS Settings → Privacy & Security → Tracking. In the EEA and UK, Google's consent form appears before "
             "ads are requested the first time, and declining still leaves non-personalised ads."),
            ("Where is my progress?",
             "On this phone only. There is no account and no cloud sync, so deleting the app deletes progress, stars and "
             "coins."),
        ],
    ),
    dict(
        slug="pixelpickle", name="Pixel Pickle: Nonograms",
        purpose=("Pixel Pickle is a nonogram (picross) puzzle: every row and column carries a list of clue numbers, and "
                 "filling exactly those runs draws the hidden picture. The game's own line solver decides every cell of "
                 "a puzzle before it is shown, so a board can always be finished without guessing."),
        local=[
            "Boards grow from 5×5 warm-ups to full 15×15 pictures: 5×5 for levels 1–20, 10×10 for 21–200, 10×15 for "
            "201–600 and 15×15 from 601. The trail has no fixed end — each level is generated on the phone from its "
            "number, so level 201 is the same picture on every launch.",
            "Tap to fill a pixel, drag to paint a row, and switch to X notes to mark the cells you have proven empty. "
            "Clue numbers fade once their row or column is finished.",
            "A hint fills one cell that your own notes already prove, and undo steps back one pixel; both are paid from "
            "coins, and coins are earned for free as well.",
            "Challenge mode ends a round after three pixels that contradict the picture; Relax mode removes that limit "
            "and lets you work the same puzzles without pressure.",
            "Finishing a picture pays coins, the daily reward adds more, and coins also buy the mint and sunset skins. A "
            "reward video can continue a round that ran out in challenge mode.",
            "Progress, coins, skins and settings stay in this app's own storage on the phone, with no account and no "
            "sync.",
        ],
        free=("The game is free with ads. Remove Ads is one payment that stops banner and interstitial ads; the Starter "
              "Pack adds coins and hints; the three coin packs are optional. No purchase unlocks a level."),
        prices=dict(removeads="$3.99", starter="$2.99",
                    coins_small="$1.99", coins_medium="$4.99", coins_large="$9.99"),
        subs=False,
        analytics=False, crash=False, ads=True, tracking=True, rewarded=True,
        disclaimer=None,
        faq=[
            ("How do I remove the ads?",
             "Buy Remove Ads in the shop, then Restore Purchases on another device signed in with the same Apple Account. "
             "It stops banner and interstitial requests for good; the optional reward video stays optional."),
            ("I am stuck on a puzzle.",
             "You never have to guess: mark the cells you have proven empty with X notes and re-read the clues — a row or "
             "column with one long run plus an X or two usually collapses. A hint fills a single cell your own notes "
             "already prove, so it never reveals the picture for you."),
            ("Do I need a subscription?",
             "No. There is no subscription in this app. Every purchase is charged once, and the free game plays every "
             "level in the trail."),
            ("Can I turn off ad tracking?",
             "Yes. iOS Settings → Privacy & Security → Tracking. In the EEA and UK, Google's consent form appears before "
             "ads are requested the first time, and declining still leaves non-personalised ads."),
            ("Where is my progress?",
             "On this phone only. There is no account and no cloud sync, so deleting the app deletes progress, coins and "
             "skins."),
        ],
    ),
    dict(
        slug="monstermath", name="Monster Math: Cage Sums",
        purpose=("Monster Math is a cage-sums number puzzle: every cage must reach its corner number with addition, "
                 "subtraction, multiplication or division, and every row and column holds 1 to N exactly once. A level is "
                 "kept only when the counting solver finds exactly one solution."),
        local=[
            "Grids run from 3×3 up to 7×7. Each level is generated on the phone from its own number, so level 40 is the "
            "same puzzle on every launch, and the trail keeps producing new levels as you climb.",
            "Cages carry a target and an operator: + and × anywhere, − and ÷ only between two cells. Single-cell cages "
            "ship filled in, so each cage is a real clue.",
            "Difficulty is the hardest rule a puzzle actually needs — naked single, cage combinations, hidden single, "
            "naked pair. A level that would need trial and error is regenerated or simplified before you see it.",
            "A hint names the technique that applies and points at the cell it decides; undo steps the board back a move. "
            "One hint costs a hint token, or 30 coins.",
            "The first clear of a level pays coins depending on your stars; the seven-day snack tin adds more. Coins buy "
            "hints, three undos and the two extra Chomper skins.",
            "Progress, coins, skins and settings stay in this app's own storage on the phone, with no account and no sync.",
        ],
        free=("The game is free with ads. Remove Ads is one payment that stops banner and interstitial ads; the Starter "
              "Pack adds 500 coins and 5 hints; the three coin packs are optional. No purchase unlocks a level."),
        prices=dict(removeads="$3.99", starter="$2.99",
                    coins_small="$1.99", coins_medium="$4.99", coins_large="$9.99"),
        subs=False,
        analytics=False, crash=False, ads=True, tracking=True, rewarded=True,
        disclaimer=None,
        faq=[
            ("How do I remove the ads?",
             "Buy Remove Ads in Chomper's cave shop, then Restore purchases on another device signed in with the same "
             "Apple Account. It stops banner and interstitial requests; the optional reward video stays optional."),
            ("A cage looks like it has two answers.",
             "It does not: a cage merge is kept only if the counting solver still finds exactly one solution, and the "
             "test suite replays generated levels to a win. If a grid genuinely has a second answer, send the level "
             "number — we treat it as a bug."),
            ("Do I need a subscription?",
             "No. There is no subscription in this app. Remove Ads, the Starter Pack and the coin packs are charged once."),
            ("Can I turn off ad tracking?",
             "Yes. iOS Settings → Privacy & Security → Tracking. In the EEA and UK, Google's consent form appears before "
             "ads are requested the first time, and declining still leaves non-personalised ads."),
            ("Where is my progress?",
             "On this phone only. There is no account and no cloud sync, so deleting the app deletes progress, coins and "
             "skins."),
        ],
    ),
]


def head(title: str) -> str:
    return (
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        f'<title>{title}</title><style>{STYLE}</style></head><body>'
    )


def nav(slug: str, name: str) -> str:
    base = f"/legal/{slug}"
    return (
        f'<nav><a href="/legal/">All apps</a>'
        f'<a href="{base}/privacy/">Privacy</a>'
        f'<a href="{base}/terms/">Terms</a>'
        f'<a href="{base}/support/">Support</a></nav>'
    )


def tail() -> str:
    return (
        f'<p style="opacity:.6;margin-top:3rem">Contact: '
        f'<a href="mailto:{EMAIL}">{EMAIL}</a></p></body></html>\n'
    )


def ul(items: list[str]) -> str:
    return "<ul>\n" + "\n".join(f"<li>{item}</li>" for item in items) + "\n</ul>\n"


def faq_html(app: dict) -> str:
    out = []
    for question, answer in app["faq"]:
        out.append(f"<h3>{question}</h3>\n<p>{answer}</p>")
    return "\n".join(out) + "\n"


def privacy(app: dict) -> str:
    name, slug = app["name"], app["slug"]
    collect = [
        "No account, no sign-in, no profile. We never ask for your name, email address or phone number.",
        "No advertising identifier and no advertising SDK are used by this app."
        if not app["ads"] else
        "Advertising identifiers are used only through Google AdMob, as described under <em>Ads</em> below.",
    ]
    if app["analytics"]:
        collect.append(
            "Usage analytics through Firebase Analytics (Google): which screens are opened, app version, device model, "
            "operating system version, language and an app-instance identifier. It is not linked to your name or account, "
            "because there is no account."
        )
    if app["crash"]:
        collect.append(
            "Crash reports through Firebase Crashlytics (Google): the stack trace, app version, device model and operating "
            "system version at the moment of a crash. Crash reports carry no name, email address or contact data."
        )
    collect.append(
        "Purchases are verified by the App Store. We receive sales and proceeds reports from Apple in aggregate; we do not "
        "receive your name, address or payment details."
    )
    collect.append("We do not sell your personal information, and we do not share it with data brokers.")

    body = [nav(slug, name), f"<h1>{name} Privacy Policy</h1>",
            f'<p style="opacity:.6">Last updated {UPDATED}. Applies to {name} for iPhone.</p>',
            "<h2>Short version</h2>",
            f"<p>{app['purpose']} There is no account. "
            + ("The app shows ads, and ads are the only reason it uses an advertising identifier." if app["ads"]
               else "Nothing you type, open or save is uploaded.")
            + "</p>",
            "<h2>What the app does on your device</h2>", ul(app["local"]),
            "<h2>What we collect</h2>", ul(collect)]
    body += app.get("lines", [])

    if app["ads"]:
        body.append("<h2>Ads</h2>")
        rewarded = (" and, only when you choose to watch one in exchange for a hint, a rewarded video"
                    if app.get("rewarded") else "")
        body.append(
            "<p>Ads are supplied by Google AdMob: a banner at the bottom of the game screen, an interstitial after a "
            f"finished board{rewarded}. "
            "To select and measure those ads, Google may process a device advertising identifier, an IP-derived coarse "
            "location, device type, operating-system version and ad interaction events. We receive aggregate revenue "
            "reports, never personal information about you.</p>"
        )
        body.append(
            "<p><strong>Consent comes first.</strong> Before any ad is requested, the app runs Google's User Messaging "
            "Platform consent flow. In the EEA, UK and Switzerland that form lets you choose whether personalised ads may "
            "be based on your identifier; declining still serves non-personalised ads. On iOS you are also asked once, "
            "through Apple's App Tracking Transparency prompt, whether the app may track you across apps. You can change "
            "that at any time in iOS Settings → Privacy &amp; Security → Tracking, and read Google's practices at "
            f'<a href="{GOOGLE_PARTNER}">{GOOGLE_PARTNER}</a>.</p>'
        )
        body.append(
            "<p>Buying the ad-free upgrade stops ad requests being made by the app. It does not delete data Google has "
            "already collected.</p>"
        )

    if app["analytics"] or app["crash"]:
        body.append("<h2>Firebase</h2>")
        body.append(
            "<p>Analytics and crash reporting are provided by Google Firebase. Data is transmitted over TLS and retained "
            f'by Google under its terms: <a href="{FIREBASE_PRIVACY}">{FIREBASE_PRIVACY}</a>. Analytics collection is not '
            "linked to an identity, and the app has no way to identify you personally. If you would rather not send crash "
            "reports, iOS Settings → Privacy &amp; Security → Analytics &amp; Improvements → Share With App Developers "
            "turns off the system-level share; the app's own uploads stop when the network is unavailable, which is also "
            "how the app behaves in airplane mode.</p>"
        )

    body.append("<h2>Purchases</h2>")
    body.append(
        "<p>Payment for any purchase is handled entirely by Apple through your Apple Account. We never see your card, "
        "your billing address or your Apple Account credentials. Apple tells the app whether an entitlement is active; "
        "the receipt stays on your device and, for a subscription, with Apple. Apple's handling of your data is "
        f'described at <a href="{APPLE_PRIVACY}">{APPLE_PRIVACY}</a>.</p>'
    )

    if app["ads"] or app["analytics"] or app["crash"]:
        body.append("<h2>Network use</h2>")
        usage = []
        if app["ads"]:
            usage.append("requesting and displaying ads, and the consent form that precedes them;")
        if app["analytics"] or app["crash"]:
            usage.append("sending analytics events and crash reports to Google Firebase;")
        usage.append("checking an App Store purchase with Apple.")
        body.append("<p>The app uses the network only for:</p>" + ul(usage) +
                    "<p>Everything else it does happens on the phone, without a connection.</p>")

    body.append("<h2>Storage and deletion</h2>")
    body.append(
        "<p>Your data — the records, progress, history and settings this app keeps — is stored in the app's own "
        "container on the phone. It is not uploaded and there is no restore service. Deleting the app deletes it, "
        "and any file you exported beforehand stays wherever you sent it.</p>"
    )
    body.append("<h2>Children</h2>")
    body.append(
        "<p>This app is not directed at children under 13, and we do not knowingly collect personal information from "
        "anyone, including children.</p>"
    )
    body.append("<h2>Your rights</h2>")
    # Only an app that ships Google SDKs has Google-held data to write about; the
    # no-collection apps must not claim collection in the same paragraph.
    google_controller = (
        "For the advertising and analytics data described above, Google is the controller of that processing and its "
        "privacy pages explain how to exercise your rights there. "
        if app["ads"] or app["analytics"] or app["crash"] else ""
    )
    body.append(
        "<p>We hold no personal data that identifies you, so there is nothing on our side to export, correct or delete. "
        "Data on your device is under your control: change it in the app, or delete the app. "
        + google_controller
        + "If you have a question about this policy or a request under the GDPR, UK GDPR or "
        f'CCPA, write to <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>'
    )
    body.append("<h2>Changes</h2>")
    body.append(
        "<p>If this policy changes, the new version appears at this address with a new date above. A change that matters "
        "will be noted in the app's release notes.</p>"
    )
    body.append("<h2>Contact</h2>")
    body.append(
        f'<p>Privacy questions: <a href="mailto:{EMAIL}">{EMAIL}</a>. '
        f'The publisher is an independent developer, and this address reaches the person who wrote the app.</p>'
    )
    return head(f"{name} Privacy Policy") + "\n".join(body) + "\n" + tail()


def purchase_terms(app: dict) -> list[str]:
    """Pricing prose: the 12 subscription apps, or a catalogue of one-off purchases.

    The games sell Remove Ads, a starter pack and three coin packs — nothing renews, so
    auto-renewal and cancellation text would describe a product that does not exist.
    """
    p = app["prices"]
    if app.get("subs", True):
        return [
            "<h2>Free features and Pro</h2>",
            f"<p>{app['free']}</p>",
            "<p>Pro is one entitlement. It is sold in four forms for one app: a weekly, monthly or yearly auto-renewable "
            "subscription, or a one-time lifetime purchase. The features Pro unlocks are the same whichever form you buy; "
            "the difference is how long it lasts and how it is paid for.</p>",
            "<h2>Price and billing</h2>",
            f'<p>Prices are shown in US dollars. The App Store charges the price for your local storefront, in your local '
            "currency, and shows that price in the app before you confirm. Payment is charged to your Apple Account when "
            "you confirm the purchase.</p>",
            "<table>\n<thead><tr><th>Option</th><th>What it is</th><th>Price</th></tr></thead>\n<tbody>",
            f"<tr><td>Weekly</td><td>Auto-renewable, one week</td><td>{p['weekly']}</td></tr>",
            f"<tr><td>Monthly</td><td>Auto-renewable, one month</td><td>{p['monthly']}</td></tr>",
            f"<tr><td>Yearly</td><td>Auto-renewable, one year</td><td>{p['yearly']}</td></tr>",
            f"<tr><td>Lifetime</td><td>One payment, does not renew</td><td>{p['lifetime']}</td></tr>",
            "</tbody></table>",
            "<h2>Auto-renewal</h2>",
            "<p>A subscription renews automatically for the same period at the same price unless auto-renewal is turned "
            "off at least 24 hours before the end of the current period. The renewal is charged to your Apple Account "
            "within the 24 hours before the period ends. Where the store offers a price change, it is presented to you "
            "for confirmation first.</p>",
            "<h2>Managing and cancelling</h2>",
            "<p>Manage or cancel in <code>iOS Settings → Apple Account → Subscriptions</code>, or in the App Store app "
            "under your account, or at <a href=\"https://apps.apple.com/account/subscriptions\">apps.apple.com/account/"
            "subscriptions</a>. Cancelling stops the next renewal and keeps Pro until the period you already paid for "
            "ends. Deleting the app does not cancel a subscription.</p>",
            "<h2>Lifetime purchase</h2>",
            f"<p>The lifetime purchase is a single non-consumable payment of {p['lifetime']}. It does not renew, has no "
            "end date and has nothing to cancel. It stays active unless the store refunds it.</p>",
        ]
    return [
        "<h2>What you can buy</h2>",
        f"<p>{app['free']}</p>",
        "<p>There is no subscription in this app: nothing renews and there is nothing to cancel. Each purchase below is "
        "charged once to your Apple Account, at the price your App Store storefront shows before you confirm.</p>",
        "<table>\n<thead><tr><th>Purchase</th><th>What it is</th><th>Price</th></tr></thead>\n<tbody>",
        f"<tr><td>Remove Ads</td><td>One payment, permanent; stops every ad format</td><td>{p['removeads']}</td></tr>",
        f"<tr><td>Starter Pack</td><td>One payment, permanent; a coin bundle and five hints, once</td>"
        f"<td>{p['starter']}</td></tr>",
        f"<tr><td>Coins — small</td><td>Consumable, spent in the game</td><td>{p['coins_small']}</td></tr>",
        f"<tr><td>Coins — medium</td><td>Consumable, spent in the game</td><td>{p['coins_medium']}</td></tr>",
        f"<tr><td>Coins — large</td><td>Consumable, spent in the game</td><td>{p['coins_large']}</td></tr>",
        "</tbody></table>",
        "<h2>Coins</h2>",
        "<p>Coins are spent inside the game and are not returned once spent. They are also earned by finishing levels "
        "and by the daily reward, so no purchase is needed to play any level.</p>",
    ]


def terms(app: dict) -> str:
    name, slug = app["name"], app["slug"]
    body = [nav(slug, name), f"<h1>{name} Terms of Use</h1>",
            f'<p style="opacity:.6">Last updated {UPDATED}. These terms cover {name} for iPhone and every purchase made '
            "inside it.</p>",
            "<h2>Licence</h2>",
            f'<p>{name} is licensed, not sold, to you for use on Apple devices you own or control, under Apple\'s standard '
            f'End User License Agreement: <a href="{EULA}">{EULA}</a>. Where these terms and Apple\'s agreement differ, '
            "Apple's agreement governs the licensed application itself. Nothing in these terms limits rights Apple's EULA "
            "gives you.</p>",
            *purchase_terms(app),
            "<h2>Restoring a purchase</h2>",
            "<p>Tap <em>Restore Purchases</em> on the purchase screen, signed in with the same Apple Account that bought "
            "it. Purchases cannot be transferred between Apple Accounts. If a restore does not bring Pro back, write to "
            f'<a href="mailto:{EMAIL}">{EMAIL}</a> with the product name and the date of purchase.</p>',
            "<h2>Refunds</h2>",
            "<p>Refunds are handled by Apple, not by us — we cannot see or reverse a charge. Request one at "
            f'<a href="{REPORT_PROBLEM}">{REPORT_PROBLEM}</a>. '
            + ("A refunded purchase stops unlocking Pro; work you already saved on the device is kept.</p>"
               if app.get("subs", True) else
               "A refunded purchase is removed from your Apple Account; coins you already spent and levels you already "
               "cleared on the device are kept.</p>"),
            "<h2>What you may not do</h2>",
            "<p>Do not redistribute the app or its content, resell access, reverse-engineer it except where the law "
            "allows, remove proprietary notices, or use the app to break the law. Do not use the app's output as if it "
            "were a certified professional result where a licence or a stamped document is required.</p>",
        ]
    if app["disclaimer"]:
        body.append("<h2>Professional disclaimer</h2>")
        body.append(app["disclaimer"])
    body.append("<h2>No warranty</h2>")
    body.append(
        "<p>The app is provided as is. To the extent the law allows, we make no warranty that it is error-free or fit "
        "for a particular purpose, and we are not liable for indirect or consequential loss, or for lost data. Nothing "
        "in these terms excludes liability that cannot lawfully be excluded, or your statutory rights as a consumer.</p>"
    )
    body.append("<h2>Changes to these terms</h2>")
    body.append(
        "<p>A change appears at this address with a new date above. A change to what a purchase includes applies from "
        "your next renewal, not to a period you have already paid for.</p>"
    )
    return head(f"{name} Terms of Use") + "\n".join(body) + "\n" + tail()


def support(app: dict) -> str:
    name, slug = app["name"], app["slug"]
    body = [nav(slug, name), f"<h1>{name} Support</h1>",
            f'<p style="opacity:.6">Last updated {UPDATED}.</p>',
            "<h2>Contact us</h2>",
            f'<p>Email <a href="mailto:{EMAIL}">{EMAIL}</a>. Include the app name, the app version (Settings → Apps → '
            f"{name}, or the About screen), your iPhone model, the iOS version, and what you did just before the problem. "
            "We answer within two business days.</p>",
            "<h2>Common questions</h2>",
            faq_html(app),
            "<h2>Purchases and restoring</h2>",
            "<p>Purchases are handled by Apple. On a new phone or after reinstalling, open the purchase screen, tap "
            "<em>Restore Purchases</em>, and make sure the device is signed in with the same Apple Account that bought "
            "it. Purchases cannot be moved between Apple Accounts.</p>",
            "<h2>Cancel a subscription</h2>",
            "<p><code>iOS Settings → Apple Account → Subscriptions</code>. Cancelling stops the next renewal and keeps "
            "access until the paid period ends. Deleting the app does not cancel anything.</p>",
            "<h2>Refunds</h2>",
            f'<p>We cannot issue refunds — Apple handles all billing. Request one at '
            f'<a href="{REPORT_PROBLEM}">{REPORT_PROBLEM}</a>.</p>',
            "<h2>Where is my data?</h2>",
            "<p>On your device only. There is no account and no cloud sync, so deleting the app deletes its data. Export "
            "anything you want to keep first.</p>",
            "<h2>Privacy</h2>",
            f'<p>See the <a href="/legal/{slug}/privacy/">privacy policy</a> and the '
            f'<a href="/legal/{slug}/terms/">terms of use</a>.</p>',
            "<h2>Accessibility</h2>",
            "<p>If a screen is hard to use with VoiceOver, large text or a switch control, tell us which screen and "
            "which device — we treat it as a bug.</p>",
            ]
    return head(f"{name} Support") + "\n".join(body) + "\n" + tail()


def apps_table() -> str:
    rows = "\n".join(
        f'<tr><td>{app["name"]}</td>'
        f'<td><a href="/legal/{app["slug"]}/privacy/">Privacy</a> · '
        f'<a href="/legal/{app["slug"]}/terms/">Terms</a> · '
        f'<a href="/legal/{app["slug"]}/support/">Support</a></td></tr>'
        for app in APPS
    )
    return ("<table>\n<thead><tr><th>App</th><th>Pages</th></tr></thead>\n<tbody>\n"
            + rows + "\n</tbody></table>\n")


def obsolete(what: str) -> str:
    """The one-size-fits-all /legal/privacy/ and /legal/support/ URLs: they stayed
    in App Store Connect for months, so they keep resolving, but the per-app pages
    are the real ones."""
    return (
        head(f"Legal — {what}")
        + f'<meta http-equiv="refresh" content="0; url=/legal/">'
        + f'<nav><a href="/legal/">All apps</a></nav>'
        + f"<h1>{what}</h1>"
        + "<p>Each app now has its own pages, because they no longer collect the same things. "
          "Pick the app you are using:</p>"
        + apps_table()
        + f'<p>Contact: <a href="mailto:{EMAIL}">{EMAIL}</a></p>'
        + tail()
    )


def landing(app: dict) -> str:
    """<slug>/ — the marketing URL in App Store Connect."""
    name, slug = app["name"], app["slug"]
    return (
        head(f"{name}")
        + nav(slug, name)
        + f"<h1>{name}</h1>"
        + f"<p>{app['purpose']}</p>"
        + "<h2>Pages</h2>"
        + f'<ul><li><a href="/legal/{slug}/privacy/">Privacy policy</a></li>'
        + f'<li><a href="/legal/{slug}/terms/">Terms of use</a></li>'
        + f'<li><a href="/legal/{slug}/support/">Support</a></li></ul>'
        + tail()
    )


def index() -> str:
    return (
        head("Legal — iOS apps")
        + '<nav><a href="/legal/">All apps</a></nav>'
        + "<h1>Legal</h1>"
        + f'<p style="opacity:.6">Privacy policies, terms of use and support pages for the iOS apps in this account. '
          f"Last updated {UPDATED}.</p>"
        + apps_table()
        + f'<p>Contact: <a href="mailto:{EMAIL}">{EMAIL}</a></p>'
        + tail()
    )


def main() -> None:
    root = Path(__file__).resolve().parent
    slugs = [app["slug"] for app in APPS]
    assert len(slugs) == len(set(slugs)), "duplicate slug"
    for app in APPS:
        # Subscription apps price weekly...lifetime; the games sell five one-off products
        # (Remove Ads, starter, three coin packs) and must not be required to price a plan.
        if app.get("subs", True):
            assert app["prices"]["weekly"] and app["prices"]["lifetime"], app["slug"]
        else:
            assert all(app["prices"].get(k) for k in
                       ("removeads", "starter", "coins_small", "coins_medium", "coins_large")), app["slug"]
        for page, content in (("privacy", privacy), ("terms", terms), ("support", support)):
            target = root / app["slug"] / page / "index.html"
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content(app), encoding="utf-8")
        (root / app["slug"] / "index.html").write_text(landing(app), encoding="utf-8")
    (root / "index.html").write_text(index(), encoding="utf-8")
    (root / "privacy" / "index.html").write_text(obsolete("Privacy policy"), encoding="utf-8")
    (root / "support" / "index.html").write_text(obsolete("Support"), encoding="utf-8")
    print(f"wrote {len(APPS)} apps x 4 pages + index.html + 2 redirect stubs")
    if "--check" in sys.argv:
        for app in APPS:
            for page in ("privacy", "terms", "support"):
                path = root / app["slug"] / page / "index.html"
                assert path.exists(), path
                text = path.read_text(encoding="utf-8")
                assert EMAIL in text, f"{path}: no contact email"
                assert EULA in text or page != "terms", f"{path}: terms without Apple EULA"
            assert (root / app["slug"] / "index.html").exists(), app["slug"]
        print("check: every page exists, has the contact email, terms cite Apple's EULA")


if __name__ == "__main__":
    main()
