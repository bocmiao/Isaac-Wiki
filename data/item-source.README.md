# Item and entry-guide snapshots

The four catalogs contain 34 character guides, 35 room/region guides, 35 floor/mode guides, and 1057 unique item-kind/ID records: 721 collectibles (including named special forms), 188 trinkets, 97 cards/runes/soul stones, and 51 pill entries (including the special golden-pill lookup record).

## Sources

- EID names and factual effect descriptions: https://github.com/wofsauge/External-Item-Descriptions/tree/4a55dc567e701c3afe15acaf57da17841703da3a/descriptions
  - Merge `ab+/zh_cn.lua`, `rep/zh_cn.lua`, and `rep+/zh_cn.lua` in that order.
  - Preserve Repentance and Repentance+ variants, and both horse-pill variants.
  - Read names by `(kind, ID)` so duplicate English names do not overwrite entries.
- Type, charge and unlock-ID attributes, and **Repentance pool snapshot**, from https://github.com/wofsauge/IsaacDocs/tree/e05b1fd90e33608a7a7a8dcb70a89cef908cc41a/scripts/data
  - The XML snapshot contains legacy Repentance values (e.g. Revelation's soul hearts). Do not use those attributes to replace Repentance+ effect descriptions or silently relabel pools as verified Repentance+ data.
  - Only positive-weight pool memberships are listed; membership is not a drop guarantee.
- Unlock translations and guide references: `achievement-source.json` and the existing reviewed achievement catalog. These condition translations derive from wiki.gg material under **CC BY-SA 4.0**; generated pages using them preserve attribution and that license exception. Original revision and attribution are in `achievement-source.README.md`.
- Character, room and floor content: previously reviewed site guides archived in `data/entry-guides/`. Edit those source articles, then regenerate, rather than editing generated detail pages alone.

The importer parses declarations; it does **not execute upstream Lua** or copy game images, fonts or upstream runtime code. Source links and pinned commits are included on detail pages. Effect data describes the base item; runtime conditional modifiers, gold-trinket/Mom's Box variants, character modifiers and mods are not a universal multiplication of that description.

## Reviewed exceptions

- Collectible 59 is Judas' Birthright **passive Book of Belial**. Its hand-written fallback repeats the active book description, so the generator uses the reviewed Birthright mechanism and does not describe it as another active item.
- Collectibles 551 and 656 are the second Broken Shovel piece and active Damocles' hanging-sword state. They have distinct pages and acquisition notes.
- `rep+/item_data.lua` changes collectible 120 from `Tears` to `FireRate`; its +1.7 is a flat fire-rate increase in the Repentance+ description.
- Pill record 9999 is EID's **golden-pill lookup sentinel**, not the engine's ordinary PillEffect ID. It has no `gameId` in catalog data and is not presented as effect ID 9999.
- Preserve `?` when matching reversed cards. Ordinary tarot cards must not inherit their reversed counterpart's unlock. Reversed Sun and Moon share achievement 542; golden pills use 603.
- Rune names are matched to the corresponding `Rune of ...` achievement, not to a same-name trinket or a generic rune-page fragment. Card Ace of Spades uses achievement 327, not the trinket.

## Rebuild

```sh
python3 scripts/import-item-source.py <EID-checkout> <IsaacDocs-checkout>  # only when updating the snapshot
python3 scripts/generate-entry-pages.py
npm test
BASE=/Isaac-Wiki/ npm run build
```

The generator refuses unresolved effect tags, missing descriptions and unknown unlock IDs. Commit source data, reviewed exceptions, generated Markdown, catalog JSON and manifest together. Former article URLs remain catalog pages; their entry/build/combat anchors route to corresponding detail pages.
