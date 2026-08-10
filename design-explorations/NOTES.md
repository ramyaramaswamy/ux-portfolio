# Design explorations

**Current designs: `home-v16.html` and `capacity-v1.html`** — open these two. Everything
else is history.

## Where we got to (9 Aug 2026)

Both pages are design-complete. The home page was finished on 31 Jul; the capacity case
study caught up on 9 Aug and is now mobile-complete, with its figures rebuilt and its
testimonials promoted out of a raster into real markup. What remains on both is content,
not design — see **Still open** below.

The original build order was Capacity first, on the theory that the hardest page should
define the components. That got inverted once home was built, and the two have now met in
the middle: capacity was built by porting home's tokens and shell wholesale, which is the
proof that the token set travels. **The next step is writing the spec**, using both files
as the reference, then extracting `css/style.css` and the real pages.

---

## Still open

**On `capacity-v1.html`:**

- **The cover is still a placeholder** — `.cover-ph`, full bleed at 16:5. Change
  `--cover-ratio` alone and the band, the placeholder and the shipped image all follow.
- **Three figures are still softened** by the upscaling mistake described under *Figures*:
  `product-areas` (1.50×), `prioritization-matrix` (1.62×), `team-archetypes` (1.32×).
  `vteams` was reverted; these three weren't. Re-cutting them at native cropped size keeps
  the size gain and removes the softness — it costs nothing but a re-export.
- **`testimonials.webp` is now unused** (73KB) since the quotes became markup. Delete it
  once you're sure the raster isn't wanted elsewhere.
- **The two short testimonials have no organisation** against the VP's "Meta". Fine if
  that's deliberate; inconsistent if it isn't.

**On `home-v16.html`:**

- ~~Case study covers~~ **done.** Both are in and both placeholders are gone:
  `images/capacity/cover.png` and `images/agentic-ai/cover.png`, each 2400×1800 (2× at the
  desktop column width) on the plum-tinted dot ground that matches the hero. Sources live
  in `Home page/`, which is gitignored — the copies under `images/` are the tracked ones.
  A superseded dark-plum variant sits at `images/capacity/cover-dark.png`; delete it if
  it's not wanted.
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

## The capacity case study — `capacity-v1.html`

Tokens and shell ported from `home-v16.html` unchanged. Two tokens are its own:
`--measure: 660px`, the reading column, deliberately far narrower than home's because this
page carries 2,400 words of running prose and home carries almost none; and `--stack: 56px`,
the prose→figure gap, set at roughly half `--band` so a figure sits closer to the paragraph
it belongs to than two chapters sit to each other.

### Sections

**Intro is plain paper — no dot ground.** It used to carry home's hero grid as a callback.
The cover sits directly above it and has a dot texture of its own, and two patterned bands
stacked read as decoration competing with the title rather than as one image over one page.

**Both pull quotes open on a gold eyebrow.** The slot used to be either/or — a row of gold
dots on the first, a label on the second — and side by side they read as two components
rather than as the same voice twice, which is the one thing that band exists to avoid. The
label also names what the sentence *is*, which a dot can't. The blockquote measure is
**44ch, not 26**: both quotes set their own breaks with `<br>`, and at 26ch the longer one
wrapped again underneath, so one came out as two tidy lines and the other as three ragged
ones. 44ch clears the longest authored line, so every quote breaks where it says it breaks.

**Results is centred**, like the quote bands. It was the one block set left, and against an
888px band that put its left edge 136px outboard of every heading above it — the page's
strongest section read as the one that had slipped. Below 900px the *paragraph* reverts to
left: centred prose has no fixed left edge to return to, which the eye absorbs over the
three or four lines this runs to on desktop and not over the eleven it becomes at 390px.

**Testimonials are HTML, not an image** — the page's second and last quote treatment. The
plum band is the author's voice; a card is other people's, because a card can carry a face
and an attribution. Three equal columns, VP quote in the middle as the original slide had
it, cards stretched to a common height with each attribution pushed down by `margin-top:auto`
so all three faces sit on one line.

**The gold highlight, five times on 2,400 words.** The marker device from the reference,
in this palette's gold. It is **reserved for figures and outcomes** — never a whole
explanatory sentence, because a highlight covering the argument stops pointing at anything
inside it — and it is **paper only**: the wash is mixed for white, and the plum bands
already have gold doing this job in their metric values. Roughly one per act: the two
intro figures, the CEO's 95% mandate, the 90+→six collapse, and the team's turnaround.
The Product section is deliberately unmarked, because the Results band lands directly
after it carrying four gold numbers and two emphases in a row is one too many.

Three details in the rule itself:

- **Colour is set, not inherited.** The wash renders `#F4E4BC`; ink on it clears 12.6:1,
  while the body grey it used to inherit managed 6.0:1. A phrase singled out as important
  shouldn't be the least legible thing in its own paragraph.
- **Weight 500, not 600.** The prose already runs `<strong>` at 700 in several places, so
  a heavier highlight competed with it rather than sitting a step above the body.
- **Horizontal padding `.12em`, and `box-decoration-break: clone`.** At `.2em` the right
  padding visibly detached a sentence-final period from its own sentence; `clone` gives a
  wrapped highlight its padding and radius on both fragments instead of slicing them.

### Mobile

One extra stop below the 900px block: **480px**, where the intro facts go one-up. Two
columns inside a 390px screen left each value ~110px, turning the longest into six lines —
and since grid rows take their tallest cell, it opened a hole the same six lines deep under
the shortest. One column is no taller in practice, because the hole goes with it.

### Figures

**They shrink. They do not pan.** The first attempt gave every figure `min-width: 720px`
inside an `overflow-x` scroller, with a sticky edge fade to advertise the crop. That was the
wrong trade: it bought label-level legibility for all nine to serve a need only one of them
had. Eight argue in **shapes, densities and rhythms** — thirty boxes collapsing into six,
nine screens sharing one language, a pod above six teams — and those survive being small.
Only the quotes argued in words, and the answer there was to stop shipping words as a
picture, not to make the picture pannable. Panning's cost was paid by every reader on every
figure: a nested scroll region inside a scrolling page, a figure cropped at the right edge
whether or not you chose to explore it, and an affordance needed to explain the crop.

Detail now lives one tap away — **every figure links to its own full-size export**
(`cursor: zoom-in`), which brings the browser's pinch-zoom with it for free and costs no
JavaScript. The link is not mobile-only; a figure that behaves differently by width is
harder to explain than one that always does the same thing. It does add nine tab stops,
unlike home's image links which are deliberately `tabindex="-1"` — correct here, because
the link is the only route to full resolution.

**Trim the dead margin, then leave the crop at native size.** Several exports floated in
whitespace — `product-home` was 34.8% empty across its width. Cropping to the content box
plus ~3% padding makes the content fill the frame, which is worth 1.03×–1.45× of apparent
size for free. Two things learned the hard way:

- **Trimming costs no sharpness.** Cutting empty pixels doesn't touch content pixels, so a
  figure cropped to its native 1390px displays at exactly the density the untrimmed 1700px
  file did — it just fills the frame instead of floating in it.
- **Never resize up after cropping.** Only `product-home` has a true 2× export (4800px);
  `vteams`, `product-areas`, `team-archetypes` and `prioritization-matrix` are ~1700px 1×
  exports. Cropping those and then scaling to a 2080/2360 target invented pixels and
  visibly softened them — worst at 1.68× on `vteams`, which is why that one was reverted to
  its untrimmed original. Check the source resolution before choosing a delivery width.

**Delivery is WebP at q88.** The nine figures went **6.24MB → 1.15MB, an 82% cut**, checked
at 1:1 against the PNGs on the smallest type in the set and indistinguishable. That matters
more now that mobile readers actually look at the figures instead of skipping past a pan,
and it's what makes these assets cheap enough to keep in git at all — 6MB of PNGs would
have bloated the repo permanently on every re-export. `cover.png` stays PNG because
`home-v16.html` references it.

> **Source-of-truth warning.** Every trimmed figure is re-derived from `Capacity Case Study/`,
> which is **gitignored** and exists only on this machine. In the repo the WebPs are the only
> copies — a fresh clone can't rebuild them. Back that folder up somewhere off-machine.

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
- **Never scope a component rule by element.** This has now bitten three times. `nav .links`
  beat the mobile override; `nav a` beat `.btn`; and on the capacity page a bare `footer`
  selector styling the page footer reached inside every testimonial card and put a black
  block behind each attribution. Fixed by giving the page footer `.pagefoot` and scoping all
  six of its rules to that class. A page-level region and a component are different things
  and must not share a selector — the moment a second `<footer>`, `<nav>` or `<header>`
  exists anywhere on the page, an element selector is a bug waiting for a date.
- **Ask what a figure argues before deciding how it must render.** A figure that argues in
  shapes, densities or rhythms survives being small; only one that argues in *words* needs
  its labels legible — and that one usually shouldn't be an image at all. Getting this
  backwards is what produced the panning figures.

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

**On the capacity page:**

- **Horizontally panning figures** (`min-width: 720px` in an `overflow-x` scroller, plus a
  sticky edge fade to advertise the crop). Rejected outright — see *Figures* above. Don't
  retry it with a nicer affordance; the affordance was never the problem, the crop was.
- **Shrinking figures to fit with nothing else.** The other half of that false choice. A
  22%-scale slide with 3px type doesn't read as "detail available elsewhere," it reads as a
  blurry image, which on a design portfolio costs more than the missing detail does. The
  answer was shrink *plus* a tap to the full-size export.
- **Two columns for the testimonials**, long quote spanning two rows with the short pair
  stacked beside it, on the theory the pair would come out level with the tall one.
  Measured: 329px against 528px, leaving 200px of dead space. Equal columns absorb the
  difference inside the cards instead.
- **A gold eyebrow on the testimonials block.** Gold is never text on paper — same rule as
  everywhere else. The section carries a visually-hidden heading instead, matching home's
  decision to skip section tags entirely.

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
