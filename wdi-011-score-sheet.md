# WDI-011 Score Sheet: ASV Labs Public Work

## Page: `index.html`

A1 Viewport dominance:      4/5  
A2 Section rhythm:          4/5  
A3 Card justification:      5/5  
A4 Type:                    5/5  
A5 Color:                   5/5  
A6 Motion:                  4/5  
A7 Mobile composition:      4/5  
Weighted overall:           4.40/5.0  
Hard-fails triggered:       none  
Verdict:                    PASS

Evidence (re-scored 2026-11-18):

- Each major viewport has one clear content-led focus: the type-led opening, the featured
  project's facts, the repository ledger, and the closing actions. The featured tier is now
  text-only (WDI-014), which leaves more open field on desktop, so A1 drops to 4.
- Section treatments vary by height, density, field color, and information shape.
- The repository ledger is the one sanctioned comparable collection, shown as full-width rows
  with real metadata, not equal cards.
- The two-color chrome and one signal accent remain consistent; contrast is legible throughout.
- Motion is limited to pointer orientation and action/row state, with coarse-pointer and
  reduced-motion removal.
- CDP renders at 1440x1000, 834x1112, and 390x844 report exact viewport widths, zero
  horizontal overflow, and zero page exceptions.
- Mobile changes section order, hides desktop pointer behavior, compresses the masthead, and
  changes the repository metadata layout.
- HF-1: no identical card siblings above the fold.
- HF-2: no gradient/blob hero.
- HF-3: no product still in visitor-facing content; the pinned ASV Agent Desk image is used
  only as the Open Graph card.
- HF-4: no KPI/stat strip; the repository count is labeled and linked to its GitHub source.
- HF-5 through HF-8: no zig-zag series, budget overrun, icon grid, or testimonial row.
- HF-9: one primary page; the 404 utility uses a distinct, single-action editorial
  construction.

## Page: `404.html`

A1 Viewport dominance:      5/5  
A2 Section rhythm:          4/5  
A3 Card justification:      5/5  
A4 Type:                    5/5  
A5 Color:                   5/5  
A6 Motion:                  5/5  
A7 Mobile composition:      5/5  
Weighted overall:           4.85/5.0  
Hard-fails triggered:       none  
Verdict:                    PASS

Evidence:

- One error statement is the unambiguous focal point and one 48px recovery action completes the
  page.
- No card, fake UI, metric, decorative icon, gradient, testimonial, or motion is present.
- The page is complete without JavaScript, preserves exact-width renders at all required
  viewports, and produces no horizontal overflow or page exceptions.
- The utility construction is intentionally distinct from the catalog page: one bounded
  editorial measure, no navigation shell, no repository data, and no product media.
