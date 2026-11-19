const ORG = "ASV-Labs";
const API_URL = `https://api.github.com/orgs/${ORG}/repos?type=public&per_page=100`;

const monthYear = (dateString) =>
  new Intl.DateTimeFormat("en-US", {
    month: "long",
    year: "numeric",
    timeZone: "UTC",
  }).format(new Date(dateString));

// The ledger in index.html is the curated catalog. The live GitHub response only
// refreshes each row's update month and hides rows that are no longer public.
// Repository descriptions are never copied from GitHub onto the page.
async function refreshRepositoryLedger() {
  const list = document.querySelector("#repo-list");
  const count = document.querySelector("#repo-count");
  const summary = document.querySelector("#catalog-summary");

  if (!list || !count || !summary) return;

  const controller = new AbortController();
  const timeout = window.setTimeout(() => controller.abort(), 6000);

  try {
    const response = await fetch(API_URL, {
      headers: { Accept: "application/vnd.github+json" },
      signal: controller.signal,
    });

    if (!response.ok) throw new Error(`GitHub returned ${response.status}`);

    const live = new Map(
      (await response.json())
        .filter((repository) => !repository.archived && !repository.private)
        .map((repository) => [repository.name, repository]),
    );
    if (!live.size) throw new Error("GitHub returned an empty public catalog");

    const rows = [...list.querySelectorAll(".repo-row")];
    const visible = rows.filter((row) => live.has(row.dataset.repo));
    if (!visible.length) return;

    rows.forEach((row) => {
      if (!live.has(row.dataset.repo)) row.remove();
    });

    visible.forEach((row, index) => {
      const repository = live.get(row.dataset.repo);
      const updated = row.querySelector("[data-updated]");
      const stamp = repository.pushed_at || repository.updated_at;
      if (updated && stamp) updated.textContent = monthYear(stamp);
      const number = row.querySelector(".repo-row__index");
      if (number) number.textContent = String(index + 1).padStart(2, "0");
    });

    const total = visible.length;
    count.textContent = `${String(total).padStart(2, "0")} ${total === 1 ? "entry" : "entries"}`;
    summary.textContent = `${total} public ${total === 1 ? "repository" : "repositories"}`;
  } catch (error) {
    // Keep the bundled catalog as published.
  } finally {
    window.clearTimeout(timeout);
  }
}

function initializePointerField() {
  const pointerField = document.querySelector(".pointer-field");
  if (!pointerField || window.matchMedia("(pointer: coarse)").matches) return;

  window.addEventListener(
    "pointermove",
    (event) => {
      document.documentElement.style.setProperty("--pointer-x", `${event.clientX}px`);
      document.documentElement.style.setProperty("--pointer-y", `${event.clientY}px`);
      pointerField.classList.add("is-active");
    },
    { passive: true },
  );
}

document.querySelector("#year").textContent = String(new Date().getFullYear());
initializePointerField();
refreshRepositoryLedger();
