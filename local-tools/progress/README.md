# Local read-only progress viewer

Download `docs/public/downloads/isaac-progress.html`, then open it in a browser. The single file embeds its application and offline lookup data. File contents stay in memory; there are no fetch calls, game-save writers, Steam API keys, dependencies to install or runtime CDN requests. CSP denies outgoing connections. Chrome/Edge's read-only file handle can reopen the selected file; ordinary file inputs and drag/drop explicitly require selecting a fresh file again.

## Supported layout

- Header `ISAACNGSAVE09R  `; 16-byte header, 4-byte prefix field, 11 typed blocks, 8-byte tail.
- Block header: little-endian uint32 type, byte-size field and count field. Known block-specific payload lengths follow the cited layout, not a guessed fixed offset.
- Read achievements (1), event counters (2), collectible records (4), challenges (7). Skip other recognized block bodies and parse the four length-prefixed bestiary subblocks (11) to validate framing.
- Verify the trailing custom-seeded CRC-32 over bytes 16 through length minus four. Validate required array lengths, duplicate/unknown block IDs, bounds and Boolean flags. Unsupported formats fail closed; absent record IDs stay unknown.
- Repentance / Repentance+ share the format header. Array length and the chosen filename identify the applicable achievement list; missing newer IDs are never inferred as locked.
- “Collected” is separate from “unlocked”. Trinket/card/pill acquisition history is not inferred from the collectible array. Hidden item forms are described as special forms.

Format facts were cross-checked against:

- [frto027/IsaacPorter](https://github.com/frto027/IsaacPorter/blob/608ce768e2bcbf9dbcf965f517c19a1f57f4d0d7/IsaacSave.h), commit `608ce768e2bcbf9dbcf965f517c19a1f57f4d0d7` (documents 1.7.9b and 1.9.7.11+).
- [jamesthejellyfish/isaac-save-edit-script](https://github.com/jamesthejellyfish/isaac-save-edit-script/blob/516fe1c8d3245677313c159bd1debde37f80fbd0/script.py), commit `516fe1c8d3245677313c159bd1debde37f80fbd0` for checksum and arrays. Do not use its unverified hard-coded donation offsets.
- [IsaacScript / REPENTOGON enums](https://github.com/IsaacScript/isaacscript/tree/428232c3d2cae4c422bb4c360b96b15fde37b79c/packages/isaac-typescript-definitions-repentogon/src/enums), commit `428232c3d2cae4c422bb4c360b96b15fde37b79c` for event and achievement **numeric facts**. No upstream runtime code is bundled. Donation counters are 20 and 115, not another character's completion counter. Forgotten, Bethany and tainted characters have their own explicit IDs.
- Guide and item lookups use the reviewed site snapshots. wiki.gg-derived translations and tutorials retain **CC BY-SA 4.0**, attribution and original source links via the site achievement tutorials and `data/achievement-source.README.md`.

No end-user save or game installation is present in the development environment. Automated tests use independently generated binary fixtures, malformed files and headless Chromium. Support for a particular user's save should be confirmed against their in-game Stats screens; do not claim real-game validation from fixtures alone.

The managed cloud browser blocks `file://` navigation. Offline browser tests load the complete generated HTML into a disconnected page and verify zero network requests, read-only file inputs, exports and fresh-file handle reads; they do not establish file-origin behavior on the user's Windows installation.

## Update

```sh
python3 scripts/generate-save-progress-data.py <IsaacScript checkout>
node scripts/build-local-progress.mjs
npm test
BASE=/Isaac-Wiki/ npm run build
python3 scripts/check-built-links.py
```

Regenerate lookup data after updating item/achievement/character/challenge guides. For challenge strategy changes, first run `python3 scripts/generate-challenge-pages.py`; the local lookup includes all 45 strategies and links each challenge to its own page. Commit the lookup snapshot and generated single-file download together. Normal website builds rebuild the offline file using the checked-in lookup snapshot.
