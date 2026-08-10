# Capacity case study cover image — design

**Date:** 31 Jul 2026
**Status:** approved, ready to plan
**Blocks:** the home page. `NOTES.md` lists the missing covers as the only thing left.

## Goal

Produce `images/capacity/cover.png` — the cover for the "Transforming Meta's Global Capacity
Infra" row on the home page. It fills `.csimg`, a 4:3 box that occupies the outer half of the
first case study row.

## Scope

**In:** the Capacity cover, and the one page-level CSS change it depends on.

**Out:** the Agentic AI cover. It needs the same treatment and should read as a sibling, but its
source is unresolved — the Figma file
(`gUL6zuxqwgQm0GRDtSof1f`) contains a single page, Capacity Case Study, and the best agentic
artifact found so far (the CapacityMate panel in `Agentic AI Case Study/7 - Noisy Alert.png`) is
1246×688, too small to crop. That is a separate spec once a source exists.

## Decisions and why

| Decision | Choice | Why |
|---|---|---|
| Composition | **Hybrid** — real product artifact on a plum ground | Abstract graphics wouldn't prove anything; a bare screenshot has no relationship to the site |
| Crop | **Signature moment, tight** | The cover renders at ~590 CSS px. A whole 1700px dashboard scaled into that is texture, not information |
| Colour | **Authentic** — product keeps its blue/teal/purple | A data product's colour *is* its information. The plum ground does the unifying, not recolouring |
| Geometry | **B · Run-off** | Plum frames left/top/bottom, slice exits the rounded inner edge — a fragment of something larger, pointing into the page |
| Ground | **Quiet** — flat plum, faint dots, no pool | Maximum separation between the white product cards and the ground |

### Two things the mockup disproved

Recorded because both are easy to re-propose:

1. **The run-off cannot go left.** `$XX B` and every card title sit hard against the slice's left
   edge. A left bleed rendered the numeral as "B" and the timeline title as "…ty Planning
   Timeline". It destroyed the exact anchor the crop was chosen for. Run-off goes **right**.
2. **Plum must survive on three sides.** Variant C inset only the top-left and let the slice exit
   right *and* bottom. The remaining plum read as misalignment rather than as a designed ground.

## Source

- **Figma file:** `gUL6zuxqwgQm0GRDtSof1f` — Infra Cloud – MCP Unified Tooling Dashboard
- **Artboard:** `397:2` "Landing Page", 1408×1560 native — the product artboard, **not** the
  annotated slide export in `Capacity Case Study/7 - Home Page.png`
- **Crop:** full width, `y 642 → 1560` → **1408×918**, ratio 1.534
- **Working copy:** `design-explorations/assets/capacity-slice.png`

`y 642` is the exact top edge of the Meta Capacity Planning Timeline card, so the slice opens on a
clean card edge rather than through a title. The crop contains three cards — timeline (time),
Meta Fleet Trends & Insights (money), Top Budget Nodes / Top Platforms (priority). The Fleet
Trends card's top edge lands at **34.9%** down the crop, effectively on the upper-third line
without needing to be nudged.

The slice being 1.534 — wider than the 4:3 frame — is what makes a run-off possible at all. A 4:3
slice could only sit inset or fill completely.

## Composition

Geometry in percentages of the cover frame, so it is resolution-independent:

| Property | Value | At 1200×900 |
|---|---|---|
| slice `left` | 6.78% | 81.4px |
| slice `top` | 5.66% | 50.9px |
| slice `width` | 101.9% | 1222.8px |
| slice `height` | derived from 1.534 | 797px |
| slice `border-radius` | 10px at 590 reference | 20px |
| slice `box-shadow` | `0 2px 5px rgba(0,0,0,.20), 0 22px 50px rgba(0,0,0,.36)` | scaled 2.03× |

The slice overflows the right edge by ~51px at the 590 reference and is clipped by the frame.
Plum remains visible on the left, top and bottom.

## Ground

```css
background-color: #241d3d;                                    /* --plum-900 */
background-image: radial-gradient(circle, rgba(255,255,255,.05) 1px, transparent 1px);
background-size: 44.75px 44.75px;                             /* see note */
```

No pool, no gold. Gold is excluded deliberately: by the project's own rule it cannot be text
here, and as a mark it competes with the product's blue.

**Dot pitch note.** The hero's dot grid is 22px in CSS pixels. Because the cover is authored at
1200px wide and displayed at 590 at the reference viewport, the authored pitch must be
`22 × (1200/590) = 44.75px` to read as 22px on screen. This matches only at the reference width —
on a 1728px viewport the cover is 864 wide and the baked dots read at ~32px while the hero's stay
at 22px. That drift is unavoidable with a raster asset and is accepted; at .05 alpha it is not
perceptible as a mismatch.

## Output

- **Path:** `images/capacity/cover.png`
- **Size:** **2400×1800**

Not 1200×900. The cover box grows with the viewport — 590 wide at 1180, 720 at 1440, 864 at 1728,
960 at 1920 — so 1200×900 would fall to 1.25× density on a large screen. 2400×1800 holds 2× up to
a 1200px box. The 1408px slice downscales into it; nothing is upscaled.

## Production

**Built in Figma**, via the Plugin API, and exported at 2×.

The decisive fact is that `397:2` is a **COMPONENT**, not a flattened export. So the cover holds a
live instance of the real Landing Page rather than a raster of it. Nothing is pixel-baked: the
crop is a clipping frame, the type stays as type, and re-exporting at any scale stays crisp. If
the product design changes, the instance updates and the cover is re-exported — no re-cropping.

This replaced an earlier plan to compose in HTML and screenshot with headless Chrome. That route
would have baked a raster and put the cover's source of truth outside the design file.

### What was built

| Node | Id | Notes |
|---|---|---|
| `Capacity Cover — 4:3` | `698:494` | 1200×900 at canvas (1554, 10088), `clipsContent`, plum fill |
| `Dot grid — 44.75px pitch` | `698:743` | 27×21 = 567 dots, white, frame opacity `.05` — the one tuning point |
| `Slice — Landing Page y642-1560` | `698:495` | clip frame, `rescale(1222.8/1408)`, radius 20, two drop shadows |
| instance of `397:2` | `698:496` | offset `y = -642` inside the clip |

The empty 1200×900 `Frame 1` (`695:494`) was left untouched — the cover is a new frame beside it.

Export: `download_assets` on `698:494` at `defaultScale: 2` → `images/capacity/cover.png`,
2400×1800, 426 KB.

Radius and shadows must be applied **after** `rescale()`, or they get scaled down with everything
else.

## Required page change

The cover's geometry assumes the desktop run-off works. **It currently does not.** `.worklist` is
a plain centred `max-width: 1180px` with no negative margin, so at 1728px the image stops 274px
short of the edge with a squared outer corner floating in white. It looks correct in `home-v15.html`
only because that file's mock `.page` frame is itself exactly 1180 wide.

```css
@media (min-width: 901px) {
  /* 1180px is .worklist's own width, stated literally. A percentage would resolve
     against the 590px grid AREA, not the container, and overshoot by ~295px. */
  .csrow:nth-child(odd)  .csimg { margin-left:  min(0px, calc((1180px - 100vw) / 2)); }
  .csrow:nth-child(even) .csimg { margin-right: min(0px, calc((1180px - 100vw) / 2)); }
}
```

The wrapper needs `overflow-x: clip`, because `100vw` includes the scrollbar width.

Mobile needs no change — `@media (max-width: 900px)` already gives `.csimg` full rounding and
`margin: 0 22px`, which is the intended contained behaviour.

## Verification

1. Render the finished `cover.png` into a scratch copy of `home-v15.html` — with the run-off CSS
   applied and the `.csimg` placeholder replaced — at **1728**, **1440** and **390** px. The
   scratch copy is a test fixture and is not committed.
2. Confirm at every width: `$XX B` is uncut, all three card titles are uncut, plum is visible on
   left/top/bottom, and the slice is clipped only on the right.
3. Confirm the box stays 4:3 at every width, so the PNG scales rather than re-crops.
4. Confirm no horizontal overflow is introduced by the run-off CSS.

**Result — passed, 31 Jul 2026.** At 1728 the cover runs to the left viewport edge with `$XX B`,
all three card titles and the chart intact, plum on left/top/bottom, clipped only on the right.
At 390 it is contained with 22px gutters and full rounding, and `$XX B` still reads. The
pre-existing 390px page overflow (below) is visible in the fixture but is not caused by the cover.

## Deferred

- **Agentic AI cover** — blocked on source. See Scope.
- **Mobile detail.** At 390px the box is 346×260. `$XX B` still reads; card titles and table rows
  become texture. Acceptable for a thumbnail. If it should still *say* something at that size the
  answer is a tighter second crop served via `srcset` — decide alongside the Agentic cover so both
  are treated the same way.
- **`NOTES.md` update** — record the two disproved options and close the "cover images need
  making" open item once the Capacity cover ships.

## Pre-existing bug found, not in scope

At 390px the **unmodified** `home-v15.html` overflows horizontally — the metric cards and the gold
philosophy block run past the right edge. Verified against the original file, so it is not caused
by this work. It matches the existing open item in `NOTES.md` about mobile not having been
reviewed since the bleed and pool went in. Worth its own fix.
