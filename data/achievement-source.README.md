# Achievement source snapshot

`achievement-source.json` holds 641 rows extracted from the rendered [Achievements page](https://bindingofisaacrebirth.wiki.gg/wiki/Achievements), revision 269014, fetched 2026-10-05. Each record preserves the game Secrets ID, original English name, condition (including inline DLC qualifications), reward message, linked condition pages, and reward source URL. IDs 1–637 apply to Repentance; 638–641 were added in Repentance+.

Source attribution: contributors to The Binding of Isaac: Rebirth Wiki on wiki.gg; older pages may derive from the Fandom wiki. Source material and the derived condition translations, achievement catalog, and numbered guide pages are distributed under **[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)**, an exception to the site's default CC BY-NC-SA notice. No source images are copied.

Run `python scripts/generate-achievements.py` at the repository root to regenerate the seven numbered Markdown guides and UI data. The generator does not use network access. It refuses missing/duplicate IDs or conditions without a reviewed translation. Update the snapshot and review translations together, especially DLC-qualified conditions; do not strip version annotations before review. The generator's advice is editorial guidance, not evidence of game execution.
