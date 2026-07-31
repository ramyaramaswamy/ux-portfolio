# Design explorations

**Current design: `home-v16.html`** — open this one. Everything else is history.

## Where we got to (31 Jul 2026)

The home page is design-complete. Desktop and mobile both done, tokens reconciled,
keyboard focus built. What remains is content, not design — see **Still open** below.

The original build order was Capacity first, on the theory that the hardest page should
define the components. That's now inverted: home is built, so **the next step is writing
the spec**, using `home-v16.html` as the reference for tokens and components, then
`capacity.html`.

---

## Still open

- **The two case study cover images don't exist.** The files in `Capacity Case Study/` and
  `Agentic AI Case Study/` are full annotated presentation slides — title, browser mock,
  callout cards — not covers. There is no 4:3 crop of those that isn't a mess. v16 ships
  tinted placeholders. This is the only real blocker.
- **Copy lengths are lopsided.** The Agentic description is one line against Capacity's
  three, so the two rows sit at visibly different heights. A copy fix, not a layout one.
- **The two contact buttons are identical white outlines**, so the page's primary action
  has no emphasis over its secondary. Raised as a gold-button fix and declined; the
  hierarchy gap is still there.
- **No skip link.** The standard keyboard affordance for jumping past the nav to `<main>`
  (WCAG 2.4.1, Level A). ~6 lines. Note it needs `position: fixed` on focus, or to sit
  outside `.page` — `.page` has `overflow: hidden` for the image bleed and would clip it.

**Settled, not open:** `$1B+` appearing in both the metrics band and the Capacity row's
metrics is fine and intentional.

---

## The design system

Everything below lives as CSS custom properties on `.d` in `home-v16.html`. That block is
the source for `css/style.css` when the real site gets built.

### Colour

| Token | Value | Notes |
|---|---|---|
| `--plum-900` | `#241d3d` | Dark surfaces **and** heading text |
| `--plum-700` | `#35294f` | Metric cards |
| `--ink-head` | → `var(--plum-900)` | Alias, not its own value — see below |
| `--ink-body` | `#4a5468` | Inherited default |
| `--ink-muted` | `#78818f` | Secondary text |
| `--ink-faint` | `#9aa4b0` | The metric arrow only |
| `--accent` | `#57398a` | Primary buttons, eyebrow, nav hover |
| `--accent-hover` | `#452c6f` | |
| `--gold` | `#d9a521` | |
| `--rule` | `#e2e5ea` | Hairlines |
| `--dot` | `#d3d6dd` | Hero dot grid |

**One dark, not two.** `--ink-head` used to be `#1b2337`, a navy sitting a shade off the
plum used by the dark bands and the outline button — close enough to look accidental,
different enough to see. It's now an alias so heading colour and surface colour cannot
drift apart again.

**The gold is honey `#d9a521`**, hue ~38°, chosen over a lemony `#f0c463` and an antique
brass `#c9a227` because it sits opposite the plum on the wheel rather than beside it.

### Type

Source Serif 4 for headings (600 and 700 only — the italic and 400 axes were being
downloaded unused and have been dropped from the font request). Inter for everything else.

- `--text-body: 1.04rem` — every running paragraph. Was four values between 1.02 and
  1.06rem doing the same job.
- Sentence case throughout. The hero eyebrow is the single deliberate exception and the
  only all-caps left on the page.

### Vertical rhythm

| Token | Desktop | Mobile |
|---|---|---|
| `--band` | 96px | 64px |
| `--band-dark` | 80px | 56px |
| `--band-tight` | 32px | 28px |
| `--hero-top` | 56px | 40px |
| `--row-gap` | 96px | 24px |

Two rules behind these:

**Dark bands run tighter than light ones.** Every section boundary on this page is already
a colour change, so the padding is internal comfort, not separation — and the colour has
already done the separating work.

**`--row-gap` equals `--band` on desktop.** When the gap between the two case studies
exceeded the section's own padding, the rows read as less related to each other than to
the page. On mobile it drops to 24px — the deliberate exception, because the rows become
cards there, and cards in a list sit far closer than full-bleed sections do.

Mobile redeclares all five tokens once, at roughly two-thirds. There are no per-section
mobile values left to keep in sync.

### Buttons — three roles, not three backgrounds

| Role | Style | Where |
|---|---|---|
| Primary | Filled `--accent` | Light backgrounds |
| Secondary | 1.5px ink outline, fills solid on hover | Light **or** gold backgrounds |
| On dark | 1.5px white outline | Dark backgrounds |

Framed as roles rather than backgrounds so the set stops at three. All three measure
13px / 26px edge to text — the outline buttons carry 11.5px / 24.5px padding to
compensate for their border.

The on-dark button is an **outline**. The original note said "white button with white
text," which would be invisible; this resolves it.

### Keyboard focus

`:focus-visible`, not `:focus`, so the ring shows for Tab and stays away on click. 2px
outline at 3px offset — the offset clears the pill radius and makes the ring's adjacent
colour the background rather than the button. Measured:

| | |
|---|---|
| Ink ring on paper | 15.93:1 |
| Ink ring on the gold block | 7.10:1 |
| Ink ring on the darkest point of the pool (`#a3a0ae`) | 6.22:1 |
| White ring on contact / footer | 15.93:1 / 18.49:1 |
| *Gold ring on paper — rejected* | *2.24:1* |
| *White ring on the gold block — rejected* | *2.24:1* |

The white flip is scoped to `.contact` and `footer`, deliberately **not** `.metrics`: the
one focusable thing in the metrics band is the button on the gold block, where a white
ring would fail.

Transitions name their properties. The bare `transition: .16s` shorthand meant `all`,
which animated the focus ring in rather than snapping it on.

---

## Components

### Hero

Portrait left, text right. Behind it: v11's dot grid across the whole hero, over a soft
light pool — `rgba(36,29,61,.42)`, `58% × 30%`, centred at `30% 100%`.

**The 30% matters.** A pool centred at page middle sits beside her, not behind her. It was
invisible at first partly because of that, not only because of opacity.

Portrait zoom is a transform anchored bottom-centre (`--portrait-zoom: 1.16`), so her feet
stay on the card line and only her head rises. Ceiling is ~1.24 before she reaches the nav;
past that the hero needs to get taller instead.

`--hero-gap: 64px` is the clear space between the hero button and the card tops. The metric
cards rise `--bleed` (96px) into the hero, so the visible gap is the padding *minus* the
bleed — which is why `.herotext` adds the two rather than setting one.

### Metrics band

Three cards bleeding up into the hero, then the gold philosophy block — full honey fill
with an ink-outline button on it. The cards keep their short white rule.

The block's hover was **removed**: it lightened on hover while only the button inside it
was ever a link, so it promised something it couldn't do.

### Case study rows

Title → description → metrics → button. No logo, no eyebrow, no index numeral.

Rows alternate, image left then image right, with the image bleeding off the outer page
edge and rounded only on its inner corners — reusing the metrics band's bleed motif.

Three links per row, but only two in the tab order: the title, and the button. The image
link carries `tabindex="-1"` and `aria-hidden="true"` so it's mouse-clickable without
making a screen reader announce the same destination three times.

**Metrics.** A metric is either a single value or a `before → after`. Both figures carry
full ink; only the connecting arrow is lighter, so it separates without demoting a number.
Labels sentence case, non-bold. Values are ink, never gold. Separated by faint `--rule`
hairlines, with column gap 0 and padding either side so the line sits centred in the
gutter. Built with `grid-auto-flow: column`, so two metrics give two columns rather than
three with a hole.

### Mobile

- **Portrait becomes a filled circle, face only** — `min(126px, 34vw)`, left-aligned.
  The crop is the 660px square `538,70 → 1198,730` on the source, centred on the head
  (measured: it runs y118–700 at x664–1074 before widening into shoulders). The CSS
  figures are that box over 660, so they're percentages and hold at any circle size.
  The circle **must be filled** — the portrait is a transparent cut-out, so without a
  fill there's no circle, just a floating head. It carries an 8% plum tint.
- **The light pool comes off**; that circle tint takes over the grounding job. Dots only.
- **Each case study becomes a card.** The `.csrow` itself is the card — image flush to the
  top edge, text below, both clipped by the card radius, `gap: 0` so the halves meet.
- Metrics stay three across with their dividers rather than wrapping; gutters and value
  size come down to fit roughly 300px of card.
- **Nav collapses to a hamburger.** Only Work and Philosophy go in the panel — "Get in
  touch" stays visible in the bar, since the primary action shouldn't cost two taps. The
  panel is in normal flow at `flex-basis: 100%`, so it wraps to a second line inside the
  nav and **pushes the page down** rather than overlaying it. Separators run between items
  only, edge to edge (negative side margins cancel the nav's padding). Bars morph to an X.

### The one piece of JavaScript

The hamburger is the only script on the site — ~20 lines, inline, no build step. It was a
deliberate choice over the CSS-only alternatives: a hidden checkbox can't update
`aria-expanded`, so assistive tech misreads it, and `<details>` announces as a disclosure
with no Escape-to-close.

`aria-expanded` is the single source of truth. The CSS selects on it —
`nav:has(.navtoggle[aria-expanded="true"]) .links` — rather than on a class, so the visual
state and the announced state cannot drift apart.

**Nav DOM order is load-bearing: wordmark → toggle → links → CTA.** It's the only order
that tabs correctly in both layouts. On desktop the toggle is hidden, giving
Work → Philosophy → CTA; on mobile the panel comes immediately after the button that opens
it, so Tab moves into the menu you just opened. `order` does the visual arrangement in
each layout, and the two disagree — which is exactly why the DOM can't be reordered to
match what you see.

Escape closes and returns focus to the button, rather than stranding it inside a panel
that has just been hidden.

**The open/close animation.** `display: none` can't be transitioned, so the panel is a
one-row grid whose track animates `0fr → 1fr`. That tweens real height without anything
having to measure it, which is what keeps the page-push smooth. It needs the extra
`.links-inner` wrapper (`min-height: 0` plus `overflow: hidden` on both) — that's the only
reason that element exists.

`visibility` carries the accessibility half: `hidden` keeps the links out of the tab order
while collapsed, and its transition is delayed by the full duration so it only flips back
after the collapse finishes. The 14px of breathing room is padding on the *inner* element,
not margin on the outer, so it collapses with everything else.

Panel links use `outline-offset: -3px` — the panel's `overflow: hidden` would clip a
normal outset focus ring at the left and right edges.

**Specificity trap — this one bit twice.** Element-scoped nav rules quietly outrank
class-only ones, and it caused two separate bugs:

1. `nav .links` (0,1,1) beat the mobile override `.links` (0,1,0), so the panel was
   permanently open. Fix: every mobile nav rule keeps the `nav` prefix.
2. `nav a` (0,1,1) beat `.btn` (0,1,0), so the "Get in touch" button never got its own
   white text — it rendered `--ink-muted` on purple at **2.26:1**, and on hover turned
   `--accent` on `--accent-hover` at **1.28:1**, nearly invisible. Fix: `nav a:not(.btn)`
   on both the base and hover rules, so the button keeps its own colour and darkens on
   hover like every other primary button. Now 8.91:1 and 11.40:1.

**Carry this into `css/style.css`:** don't scope component rules by element. A `.btn`
should not be overridable by a `nav a` sitting elsewhere in the file.

---

## Rules that emerged

- **Gold is never text on paper.** `#d9a521` on white is 2.24:1. It works on the plum
  (~7:1) and as decoration, never as a word that has to be read on the light half of the
  page. This is why case study metric values are ink and why the focus ring isn't gold.
- **Marks, not lines — for gold, at section boundaries.** Gold accents are marks, never
  dividers. Mitch's gold section rules are the one thing from that reference deliberately
  not copied. The rule is about *gold* and about *section boundaries*: neutral hairlines
  inside a component are fine, which is why the metric cards keep their rule and the case
  study metrics gained dividers.
- **Behind the portrait, use tone with no edge.** No lines, no shapes, nothing with a
  boundary. This came out of three failed attempts — see below.

---

## Rejected, and why — so they don't get retried

**Backdrop, three attempts before the fourth worked:**

1. **SVG topographic contours** (v12). Lines behind a face compete with it; the eye keeps
   trying to resolve them. Density wasn't the issue — the medium was.
2. **Tonal panel + grounding shadow** (v13). Boxy. A vertical edge beside a grid of cards
   reads as another card.
3. **Full-width washes and a horizon line** (v14 options). Too faint to register, or
   another horizontal edge.
4. **Dots over a soft light pool.** Kept.

**Also tried and cut:**

- **Gold index numerals (01 / 02)** above the case study titles. A numeral as large as the
  headline it introduces reads top-heavy. The work section carries no gold as a result.
- **Section tags / pills** ("Selected work", "By the numbers"). Skipped entirely, which
  leaves the drawn underline as the page's single playful device — that was the goal. The
  sections now carry visually-hidden headings instead, purely for document structure.
- **Gold focus rings and gold hover states.** Declined; would have failed contrast on paper
  anyway.
- **A logo above each case study title.** Skipped — no assets exist, and it would have put
  two competing brand marks next to the wordmark in the nav.

---

## Redoing the portrait cutout

Script: `tools/portrait-cutout.py`. Source is `Home page/1_Ramya_Portrait.png`; output is
`1_Ramya_Portrait_cutout.png`. The original is kept alongside.

Luminance **cannot** separate her from that studio backdrop — lit skin reaches 255, the
background bottoms out at 214, so the ranges fully overlap. A threshold cut at 200 leaked
through a forehead highlight and removed half her face.

What works is a border-seeded flood fill, so light things *enclosed* by the subject — teeth,
the pearl bracelet, the watch — survive instead of becoming holes. The barrier sits at
**T=215**. Measured sweep:

| T | Result |
|---|---|
| 200 | 23.5% of the face lost |
| 210–215 | clean both ways |
| 220 | 0.4% of background survives |
| 232 | 23.9% of background survives |

**Verify against magenta, never white.** A white preview makes transparent and light-grey
look identical — the first bad cut looked perfect until it was composited on colour.

This is an automatic cut, not a hand mask. It's clean at the sizes used here (430px
displayed from a 1792px source), but fine flyaway hair is cut hard rather than feathered.
If the portrait is ever used large, a proper mask from Photoshop or Figma would earn its
keep.

---

## Foundational decisions (unchanged)

- Plain HTML + CSS, no build step. One `css/style.css` of custom properties; pages carry
  no styling of their own.
- v1 pages: `index.html`, `capacity.html`, `agentic-ai.html`, `philosophy.html`.
- Source Serif 4 headlines, Inter body.
- Palette sampled from Ramya's own slide decks, not from the reference site.
- Two quote treatments only.
- No contact form — a static site can't process one. Email and LinkedIn links instead.

---

## Version history

| File | What it explored |
|---|---|
| `design-directions.html` | Three type/colour directions: Faithful, Editorial, Technical |
| `design-direction-v2.html` | Editorial type + Technical palette, three teal depths |
| `design-direction-v3.html` | Purple/indigo palette sampled from Ramya's decks; quote treatments |
| `design-direction-v4.html` | Amber demoted to accent; three philosophy block options |
| `home-v5.html` | Home restructured: portrait hero, metric cards, case study rows |
| `home-v6.html` | Metrics moved onto a dark band, rounder cards |
| `home-v7.html` | First attempt at the metric card bleed |
| `metrics-bleed-options.html` | Four readings of "cards bleed into the image above" |
| `home-v8.html` | Cards over the portrait, text column kept clear of collision |
| `home-v9.html` | Real portrait, margin-collapse bug fixed, two button styles |
| `home-v10.html` | Full amber on the "Strong teams" card |
| `home-v11.html` | Pale amber on that card |
| `v12-options.html` | 3 golds × 2 block treatments, 3 contour densities, 4 scribbles, 4 tag styles |
| `home-v12.html` | Honey gold, drawn underline, alternating bleed — with the rejected contours |
| `v13-backdrop-options.html` | Six quieter backdrops after the contours were rejected |
| `home-v13.html` | Tonal panel + grounding shadow — rejected as boxy |
| `v14-ground-options.html` | Four full-width, edgeless grounds, shown against the metric cards |
| `home-v14.html` | Dots over a light pool |
| `home-v15.html` | Case study rows restructured, cut-out B&W portrait, focus states |
| **`home-v16.html`** | **Consistency pass, rhythm tokens, mobile circle + cards — current** |
