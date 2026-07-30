const ORG = "ASV-Labs";
const EXCLUDED_REPOSITORIES = new Set([".github", "ASV-Labs.github.io"]);
const FEATURED_REPOSITORY = "asv-agent-desk";
const API_URL = `https://api.github.com/orgs/${ORG}/repos?type=public&sort=updated&per_page=100`;

const languageClass = (language = "") =>
  `meta-dot--${language.toLowerCase().replace(/[^a-z0-9]+/g, "-")}`;

const monthYear = (dateString) =>
  new Intl.DateTimeFormat("en-US", {
    month: "long",
    year: "numeric",
    timeZone: "UTC",
  }).format(new Date(dateString));

const safeText = (value, fallback) =>
  typeof value === "string" && value.trim() ? value.trim() : fallback;

function repoRow(repository, index) {
  const item = document.createElement("li");
  item.className = "repo-row";
  item.dataset.repo = repository.name;

  const numericIndex = String(index + 1).padStart(2, "0");
  const language = safeText(repository.language, "Mixed");
  const description = safeText(repository.description, "Public ASV Labs repository.");
  const license = safeText(repository.license?.spdx_id, "Not declared");
  const updated = monthYear(repository.pushed_at || repository.updated_at);

  item.innerHTML = `
    <span class="repo-row__index">${numericIndex}</span>
    <div class="repo-row__identity">
      <h3><a href="${repository.html_url}">${repository.name}</a></h3>
      <p></p>
    </div>
    <dl class="repo-row__meta">
      <div>
        <dt>Language</dt>
        <dd><span class="meta-dot ${languageClass(language)}"></span></dd>
      </div>
      <div><dt>License</dt><dd></dd></div>
      <div><dt>Updated</dt><dd></dd></div>
    </dl>
    <a class="repo-row__open" href="${repository.html_url}" aria-label="Open ${repository.name} on GitHub">
      <span aria-hidden="true">↗</span>
    </a>
  `;

  item.querySelector(".repo-row__identity p").textContent = description;
  const metadataValues = item.querySelectorAll(".repo-row__meta dd");
  metadataValues[0].append(language);
  metadataValues[1].textContent = license;
  metadataValues[2].textContent = updated;

  return item;
}

async function refreshRepositoryLedger() {
  const list = document.querySelector("#repo-list");
  const status = document.querySelector("#sync-status");
  const count = document.querySelector("#repo-count");
  const summary = document.querySelector("#catalog-summary");

  if (!list || !status || !count || !summary) return;

  const controller = new AbortController();
  const timeout = window.setTimeout(() => controller.abort(), 6000);

  try {
    const response = await fetch(API_URL, {
      headers: { Accept: "application/vnd.github+json" },
      signal: controller.signal,
    });

    if (!response.ok) throw new Error(`GitHub returned ${response.status}`);

    const repositories = (await response.json())
      .filter(
        (repository) =>
          !repository.archived &&
          !repository.fork &&
          !EXCLUDED_REPOSITORIES.has(repository.name),
      )
      .sort((left, right) => {
        if (left.name === FEATURED_REPOSITORY) return -1;
        if (right.name === FEATURED_REPOSITORY) return 1;
        return new Date(right.pushed_at) - new Date(left.pushed_at);
      });

    if (!repositories.length) throw new Error("GitHub returned an empty public catalog");

    list.replaceChildren(...repositories.map(repoRow));
    const formattedCount = String(repositories.length).padStart(2, "0");
    count.textContent = `${formattedCount} ${repositories.length === 1 ? "entry" : "entries"}`;
    summary.textContent = `${repositories.length} public project ${
      repositories.length === 1 ? "repository" : "repositories"
    }`;
    status.textContent = "Live GitHub catalog loaded.";
  } catch (error) {
    status.textContent = "Live refresh unavailable; showing the bundled verified catalog.";
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
