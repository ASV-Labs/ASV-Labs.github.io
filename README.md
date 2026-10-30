# ASV Labs — Public Work

The source for the ASV Labs GitHub Pages front page at
[asv-labs.github.io](https://asv-labs.github.io/).

The site uses semantic HTML, CSS, and progressive-enhancement JavaScript. Its repository ledger
loads current public repositories from the GitHub organization API while retaining a verified
static fallback for no-JavaScript and API-failure states.

`/design-tools/` is a curated Design Engineer Tools index. The catalog lives in
`design-tools/tools.json`; regenerate the static page with
`python3 scripts/build-design-tools.py`.

## Local preview

```bash
python3 -m http.server 4173
```

Then open <http://localhost:4173>.

## Publication

GitHub Pages publishes the root of `main` directly. The branch-source configuration keeps
publication Git-based without requiring a billable Actions runner.
