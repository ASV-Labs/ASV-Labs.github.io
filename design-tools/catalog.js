async function hydrateCatalog() {
  const root = document.querySelector("#index");
  if (!root) return;

  try {
    const response = await fetch("tools.json", { headers: { Accept: "application/json" } });
    if (!response.ok) return;
    const catalog = await response.json();
    const toolCount = catalog.sections.reduce((sum, section) => sum + section.tools.length, 0);
    const summary = document.querySelector("#catalog-summary");
    const count = document.querySelector("#tool-count");
    if (summary) {
      summary.textContent = `${toolCount} public tools / ${catalog.sections.length} sections`;
    }
    if (count) {
      count.textContent = `${String(toolCount).padStart(2, "0")} entries`;
    }
  } catch {
    // Static HTML already contains the bundled catalog.
  }
}

hydrateCatalog();
