# ASV Labs GitHub Portfolio — Design Note

## Page: `index.html`

Project/topic: ASV Labs public GitHub portfolio  
Page or site type: Directory  
Primary audience: Prospective users, collaborators, and technical evaluators  
Primary user action: Open a public ASV Labs repository or its live product surface  
Secondary user action: Visit the ASV Labs GitHub organization  
Emotional tone: Precise, trustworthy, quietly ambitious  
Content density: Medium  
Device priority: Desktop and mobile equally; tablet supported as a distinct composition  
Interaction level: Low-to-medium; live repository filtering and direct outbound links  
Motion level: Low; one restrained reveal/hover system with a reduced-motion path  
Trust requirement: High; all project facts come from GitHub or the project repository  
Conversion pressure: Low; this is a transparent public-work index, not a funnel  
Implementation stack: Semantic HTML, CSS, and progressive-enhancement JavaScript on GitHub Pages

Site type: Directory  
Audience: Prospective users, collaborators, and technical evaluators  
Primary action: Open a public ASV Labs repository or live project surface  
Tone: Organized, precise, trustworthy  
Selected composition: Curated index with a featured-work tier and a live repository ledger  
Why this composition fits: ASV Labs currently has a small public catalog. One flagship project can carry real product media and fuller context, while every public repository remains visible as a GitHub-sourced ledger. The structure scales without turning into a marketing card wall.  
Style atlas match: SaaS or Technical Product, adapted to the directory gate’s restrained, editorial index  
Reference/pattern moves borrowed (max 3): Semantic badge taxonomy for language/license metadata; subject-shaped IA organized as Field / Public Work / Repository Ledger; fixed media geometry for the single captured product image  
Card budget for this site type / cards used / justification if > 0: Budget 1 / used 0 equal-card sections. Repository entries are full-width ledger rows with distinct content density, not equal cards.  
Forbidden defaults rejected (from the list of 8): Equal-height card wall is replaced by a tiered feature-plus-ledger index; three columns under a centered hero are replaced by an asymmetric editorial opening; fake dashboard screenshot is rejected in favor of a real captured ASV Agent Desk product image; pointless KPI strip is rejected and any counts are labeled as live GitHub metadata; stock-icon feature grid is not used; repeated two-column zig-zag sections are not used; unearned gradient blob background is rejected for a two-color field with one signal accent; giant testimonial card row is not used.  
Product imagery provenance: captured-from-product @ `ASV-Labs/asv-agent-desk` current public `main`, `docs/assets/product-overview.jpg` (pinned commit URL in HTML)  
Motion behavior: A restrained cursor-follow field and row/media transitions communicate navigation and active focus; no scroll-jacking or looping decoration.  
Responsive behavior (mobile composed, not squeezed): Desktop uses an asymmetric hero and wide ledger; tablet reduces the field and keeps horizontal metadata bands; mobile removes cursor effects, turns the opening into a compact masthead, promotes the repository name/action, and demotes secondary metadata into readable stacked lines.  
Accessibility fallback (reduced-motion, keyboard, no-JS): Semantic landmarks, visible focus, 44px targets, `prefers-reduced-motion`, a static fallback repository catalog in initial HTML, and status messaging with `aria-live`.  
Performance risk: Low. No framework or webfont payload; one pinned external product image is lazy-loaded; GitHub API enhancement is deferred and timeout-safe.

### Structural signature conformance

- Must: the index is tiered. The first public product has a full-width featured treatment with real media; all public repositories follow in a metadata-rich ledger.
- Must: entries carry number, category, language, license, update time, and links when GitHub supplies them.
- Must not: the page never becomes one equal grid, and the opening is not an equal-card hero.
- Cross-type `subject-shaped-ia`: section names follow the work itself—Field, Public Work, Repository Ledger—rather than a transplanted About/Services/Contact template.

## Page: `404.html`

Project/topic: ASV Labs not-found recovery  
Page or site type: Directory utility page  
Primary audience: Visitors who followed an outdated or mistyped URL  
Primary user action: Return to the ASV Labs public-work index  
Secondary user action: None  
Emotional tone: Calm, direct, consistent with the main site  
Content density: Minimal  
Device priority: Mobile first  
Interaction level: Low  
Motion level: None  
Trust requirement: Medium  
Conversion pressure: None  
Implementation stack: Standalone semantic HTML with critical inline CSS

Site type: Directory utility page  
Audience: Visitors at an unknown URL  
Primary action: Return to the ASV Labs public-work index  
Tone: Precise, calm, trustworthy  
Selected composition: Restrained editorial recovery  
Why this composition fits: A single error statement and one unambiguous recovery action are the complete job; catalog UI would create false choices.  
Style atlas match: Technical-product restraint  
Reference/pattern moves borrowed (max 3): Type-led composition; one-question/one-action service-flow restraint  
Card budget for this site type / cards used / justification if > 0: Budget 1 / used 0  
Forbidden defaults rejected (from the list of 8): No card wall, centered vague hero, fake UI, KPI strip, stock icons, zig-zag, gradient blob, or testimonial row.  
Product imagery provenance: none  
Motion behavior: None  
Responsive behavior (mobile composed, not squeezed): One bounded text measure, fluid type, and one full-size recovery target across all viewports.  
Accessibility fallback (reduced-motion, keyboard, no-JS): The page is complete without JavaScript; focus is visible and the only action exceeds 44px.  
Performance risk: None beyond the HTML document itself.
