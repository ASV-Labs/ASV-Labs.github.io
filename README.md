# ASV Labs public work

The source for the ASV Labs GitHub Pages front page at
[asv-labs.github.io](https://asv-labs.github.io/).

The site uses semantic HTML, CSS, and progressive-enhancement JavaScript. The repository list in
`index.html` is curated by hand: add a row there when a repository goes public. In the browser,
the GitHub organization API only refreshes each row's update month and hides rows that are no
longer public. Repository descriptions are never copied from GitHub onto the page.

## Local preview

```bash
python3 -m http.server 4173
```

Then open <http://localhost:4173>.

## Publication

GitHub Pages publishes the root of `main` directly. The branch-source configuration keeps
publication Git-based without requiring a billable Actions runner.
