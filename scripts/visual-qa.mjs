import { spawn } from "node:child_process";
import { mkdtempSync, mkdirSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";
import { setTimeout as delay } from "node:timers/promises";

const chromePath =
  process.env.CHROME_PATH ??
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const baseUrl = process.argv[2] ?? "http://127.0.0.1:4173/";
const outputDirectory =
  process.argv[3] ?? path.resolve("visual-qa");
const debuggingPort = 9333;
const profileDirectory = mkdtempSync(path.join(tmpdir(), "asv-labs-visual-qa-"));

mkdirSync(outputDirectory, { recursive: true });

const chrome = spawn(
  chromePath,
  [
    "--headless=new",
    "--disable-gpu",
    "--hide-scrollbars",
    "--no-first-run",
    `--remote-debugging-port=${debuggingPort}`,
    `--user-data-dir=${profileDirectory}`,
    "about:blank",
  ],
  { stdio: "ignore" },
);

async function waitForDebugger() {
  for (let attempt = 0; attempt < 50; attempt += 1) {
    try {
      const response = await fetch(`http://127.0.0.1:${debuggingPort}/json/version`);
      if (response.ok) return;
    } catch {
      // Chrome has not opened its debugging socket yet.
    }
    await delay(100);
  }
  throw new Error("Chrome debugging endpoint did not become available");
}

await waitForDebugger();
const targetResponse = await fetch(
  `http://127.0.0.1:${debuggingPort}/json/new?${encodeURIComponent(baseUrl)}`,
  { method: "PUT" },
);
const target = await targetResponse.json();
const socket = new WebSocket(target.webSocketDebuggerUrl);

await new Promise((resolve, reject) => {
  socket.addEventListener("open", resolve, { once: true });
  socket.addEventListener("error", reject, { once: true });
});

let requestId = 0;
const pending = new Map();
const events = new Map();
const pageErrors = [];

socket.addEventListener("message", ({ data }) => {
  const message = JSON.parse(data);
  if (message.id && pending.has(message.id)) {
    const { resolve, reject } = pending.get(message.id);
    pending.delete(message.id);
    if (message.error) reject(new Error(message.error.message));
    else resolve(message.result);
    return;
  }

  if (message.method === "Runtime.exceptionThrown") {
    pageErrors.push(message.params.exceptionDetails.text);
  }

  const listeners = events.get(message.method) ?? [];
  for (const listener of listeners.splice(0)) listener(message.params);
});

function command(method, params = {}) {
  requestId += 1;
  socket.send(JSON.stringify({ id: requestId, method, params }));
  return new Promise((resolve, reject) => {
    pending.set(requestId, { resolve, reject });
  });
}

function once(method) {
  return new Promise((resolve) => {
    const listeners = events.get(method) ?? [];
    listeners.push(resolve);
    events.set(method, listeners);
  });
}

await command("Page.enable");
await command("Runtime.enable");

const cases = [
  { name: "desktop", width: 1440, height: 1000, mobile: false },
  { name: "tablet", width: 834, height: 1112, mobile: false },
  { name: "mobile", width: 390, height: 844, mobile: true },
];

const results = [];

for (const testCase of cases) {
  await command("Emulation.setDeviceMetricsOverride", {
    width: testCase.width,
    height: testCase.height,
    deviceScaleFactor: 1,
    mobile: testCase.mobile,
    screenWidth: testCase.width,
    screenHeight: testCase.height,
  });
  await command("Emulation.setTouchEmulationEnabled", {
    enabled: testCase.mobile,
    maxTouchPoints: testCase.mobile ? 5 : 1,
  });

  const loaded = once("Page.loadEventFired");
  await command("Page.navigate", {
    url: `${baseUrl}${baseUrl.includes("?") ? "&" : "?"}qa=${testCase.name}`,
  });
  await loaded;
  await delay(1800);

  const dimensions = await command("Runtime.evaluate", {
    expression: `({
      innerWidth: window.innerWidth,
      innerHeight: window.innerHeight,
      scrollWidth: document.documentElement.scrollWidth,
      scrollHeight: document.documentElement.scrollHeight,
      liveStatus: document.querySelector("#sync-status")?.textContent?.trim(),
      wordmark: (() => {
        const element = document.querySelector(".site-header .wordmark");
        const rect = element?.getBoundingClientRect();
        const style = element ? getComputedStyle(element) : null;
        return rect && style ? {
          x: rect.x, y: rect.y, width: rect.width, height: rect.height,
          display: style.display, visibility: style.visibility, opacity: style.opacity
        } : null;
      })(),
      eyebrowStart: (() => {
        const element = document.querySelector(".hero .eyebrow span");
        const rect = element?.getBoundingClientRect();
        const style = element ? getComputedStyle(element) : null;
        return rect && style ? {
          x: rect.x, y: rect.y, width: rect.width, height: rect.height,
          display: style.display, visibility: style.visibility, opacity: style.opacity
        } : null;
      })()
    })`,
    returnByValue: true,
  });

  const screenshot = await command("Page.captureScreenshot", {
    format: "png",
    fromSurface: true,
    captureBeyondViewport: false,
  });
  writeFileSync(
    path.join(outputDirectory, `${testCase.name}.png`),
    screenshot.data,
    "base64",
  );

  for (const sectionId of ["public-work", "repository-ledger"]) {
    const sectionExists = await command("Runtime.evaluate", {
      expression: `Boolean(document.querySelector("#${sectionId}"))`,
      returnByValue: true,
    });
    if (!sectionExists.result.value) continue;

    await command("Runtime.evaluate", {
      expression: `document.querySelector("#${sectionId}").scrollIntoView({ block: "start" })`,
    });
    await delay(250);
    const sectionScreenshot = await command("Page.captureScreenshot", {
      format: "png",
      fromSurface: true,
      captureBeyondViewport: false,
    });
    writeFileSync(
      path.join(outputDirectory, `${testCase.name}-${sectionId}.png`),
      sectionScreenshot.data,
      "base64",
    );
  }

  results.push({
    ...testCase,
    ...dimensions.result.value,
    horizontalOverflow:
      dimensions.result.value.scrollWidth > dimensions.result.value.innerWidth,
  });
}

writeFileSync(
  path.join(outputDirectory, "results.json"),
  `${JSON.stringify({ results, pageErrors }, null, 2)}\n`,
);

socket.close();
chrome.kill("SIGTERM");

console.log(JSON.stringify({ results, pageErrors }, null, 2));

if (results.some((result) => result.horizontalOverflow) || pageErrors.length) {
  process.exitCode = 1;
}
