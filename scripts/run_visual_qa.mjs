import crypto from "node:crypto";
import fs from "node:fs/promises";
import path from "node:path";
import process from "node:process";
import { chromium, firefox, request, webkit } from "playwright";

const ROOT = process.cwd();
const REPORT_ROOT = path.join(ROOT, "release-report", "visual-qa");
const ROUTES = ["/", "/library", "/articles", "/groups", "/variants", "/feedback", "/comments", "/account", "/admin"];
const VIEWPORTS = [
  { label: "1920x1080", width: 1920, height: 1080, mobile: false },
  { label: "1440x900", width: 1440, height: 900, mobile: false },
  { label: "1280x720", width: 1280, height: 720, mobile: false },
  { label: "1024x768", width: 1024, height: 768, mobile: false },
  { label: "390x844", width: 390, height: 844, mobile: true },
  { label: "360x800", width: 360, height: 800, mobile: true },
];
const CROSS_BROWSER_VIEWPORTS = [VIEWPORTS[0], VIEWPORTS[3], VIEWPORTS[4]];
const SAFE_GENIE_QUESTION = "How far below its baseline is Capital Available in CASE_0042?";
const AUTH_STORAGE_STATE = process.env.DATABRICKS_STORAGE_STATE || undefined;
const APP_TOKEN = process.env.DATABRICKS_APP_TOKEN || undefined;

function browserContextOptions(options) {
  return {
    ...options,
    ...(AUTH_STORAGE_STATE ? { storageState: AUTH_STORAGE_STATE } : {}),
    ...(APP_TOKEN ? { extraHTTPHeaders: { Authorization: `Bearer ${APP_TOKEN}` } } : {}),
  };
}

function formatDateParts(date = new Date()) {
  const pad = (value) => String(value).padStart(2, "0");
  return {
    iso: date.toISOString(),
    day: `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())}`,
    minute: `${pad(date.getHours())}-${pad(date.getMinutes())}`,
  };
}

function slugifyRoute(route) {
  return route === "/" ? "root" : route.replace(/^\//, "").replace(/[^a-z0-9]+/gi, "-");
}

function screenshotName(route, viewport) {
  return `${slugifyRoute(route)}__${viewport.label}`;
}

function sanitizeText(value, limit = 500) {
  return String(value || "")
    .replace(/https?:\/\/\S+/gi, "[url]")
    .replace(/\s+/g, " ")
    .replace(/[A-Fa-f0-9]{24,}/g, "[redacted-id]")
    .replace(/\b\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z\b/g, "[timestamp]")
    .trim()
    .slice(0, limit);
}

function sanitizeUrl(value) {
  try {
    const url = new URL(String(value));
    const sanitizedPath = url.pathname
      .replace(/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}/gi, "[id]")
      .replace(/[A-Fa-f0-9]{24,}/g, "[id]");
    return `${url.origin}${sanitizedPath}${url.search ? "?redacted" : ""}${url.hash ? "#redacted" : ""}`;
  } catch {
    return sanitizeText(value, 240);
  }
}

function classifyAxeImpact(violations) {
  const counts = { critical: 0, serious: 0, moderate: 0, minor: 0 };
  for (const item of violations) {
    if (item.impact && counts[item.impact] !== undefined) {
      counts[item.impact] += 1;
    }
  }
  return counts;
}

function isAppUnavailableSurface(title, bodyPreview, responses) {
  if (/app not available/i.test(title) || /app not available/i.test(bodyPreview)) {
    return true;
  }
  return responses.some((entry) => entry.resourceType === "document" && entry.status === 503);
}

function summarizeFindings(result) {
  const findings = [];
  if (result.appUnavailable) {
    findings.push({
      severity: "P0",
      title: "Deployment returned Databricks App Not Available",
      route: result.route,
      viewport: result.viewport.label,
      expected: "The deployed route should load the MAD DATA LAB application shell or the expected authenticated redirect.",
      actual: `Navigation ended on "${result.title || "Unknown page"}" at ${result.finalUrl}.`,
      impact: "The live deployment is unavailable for this route and viewport, blocking product QA and the primary journey.",
      steps: [`Open ${result.requestedUrl} in a clean Chromium context.`],
      screenshot: result.screenshotPath,
      trace: result.tracePath,
      suggestedFix: "Restore the Databricks app service or deployment health before the next QA run.",
    });
  }
  if (result.authWall) {
    findings.push({
      severity: "BLOCKED_AUTHENTICATION",
      title: "Authenticated application surface is not reachable in this run",
      route: result.route,
      viewport: result.viewport.label,
      expected: "Requested MAD DATA LAB route should render the product surface when valid secure auth is available.",
      actual: `Navigation ended on "${result.title || "Unknown page"}" at ${result.finalUrl}.`,
      impact: "Primary in-app QA and the Case #042 journey are blocked for this route and viewport.",
      steps: [`Open ${result.requestedUrl} in a clean Chromium context.`],
      screenshot: result.screenshotPath,
      trace: result.tracePath,
      suggestedFix: "Provide secure automation auth or expose a non-interactive test path for the deployed review environment.",
    });
  }
  if (result.navigationError) {
    findings.push({
      severity: "P1",
      title: "Route navigation failed",
      route: result.route,
      viewport: result.viewport.label,
      expected: "The route should complete navigation and render a stable page.",
      actual: sanitizeText(result.navigationError, 300),
      impact: "This route could not be audited normally.",
      steps: [`Open ${result.requestedUrl} in a clean Chromium context.`],
      screenshot: result.screenshotPath,
      trace: result.tracePath,
      suggestedFix: "Stabilize the route response and client boot path before the next visual QA run.",
    });
  }
  if (result.overflow) {
    findings.push({
      severity: "P2",
      title: "Horizontal overflow detected",
      route: result.route,
      viewport: result.viewport.label,
      expected: "The page should fit within the viewport width without horizontal scrolling.",
      actual: `scrollWidth ${result.metrics.scrollWidth}px exceeds innerWidth ${result.metrics.innerWidth}px.`,
      impact: "Small-screen layout quality is degraded.",
      steps: [`Open ${result.requestedUrl} at ${result.viewport.label}.`],
      screenshot: result.screenshotPath,
      trace: result.tracePath,
      suggestedFix: "Constrain wide containers and media at the affected breakpoint.",
    });
  }
  if (result.axe?.summary.critical || result.axe?.summary.serious) {
    findings.push({
      severity: "P2",
      title: "Serious accessibility violations detected",
      route: result.route,
      viewport: result.viewport.label,
      expected: "No serious or critical WCAG A/AA issues should be present.",
      actual: JSON.stringify(result.axe.summary),
      impact: "Keyboard and assistive-technology usage may be materially affected.",
      steps: [`Open ${result.requestedUrl} and run axe on the settled page.`],
      screenshot: result.screenshotPath,
      trace: result.tracePath,
      suggestedFix: "Address the reported axe violations before release signoff.",
    });
  }
  return findings;
}

async function ensureDir(target) {
  await fs.mkdir(target, { recursive: true });
}

async function createArtifactDirs(root) {
  const dirs = {
    root,
    screenshots: path.join(root, "screenshots"),
    traces: path.join(root, "traces"),
    videos: path.join(root, "videos"),
    logs: path.join(root, "logs"),
  };
  await ensureDir(dirs.screenshots);
  await ensureDir(dirs.traces);
  await ensureDir(dirs.videos);
  await ensureDir(dirs.logs);
  return dirs;
}

async function writeJson(target, value) {
  await fs.writeFile(target, `${JSON.stringify(value, null, 2)}\n`, "utf8");
}

async function finalizeVideo(video, targetPath) {
  if (!video) {
    return null;
  }
  try {
    const originalPath = await video.path();
    if (path.resolve(originalPath) === path.resolve(targetPath)) {
      return originalPath;
    }
    await fs.copyFile(originalPath, targetPath);
    await fs.unlink(originalPath).catch(() => {});
    return targetPath;
  } catch {
    return null;
  }
}

async function listPreviousRuns(reportRoot, currentDir) {
  try {
    const days = await fs.readdir(reportRoot, { withFileTypes: true });
    const runs = [];
    for (const day of days.filter((entry) => entry.isDirectory())) {
      const dayDir = path.join(reportRoot, day.name);
      const minutes = await fs.readdir(dayDir, { withFileTypes: true });
      for (const minute of minutes.filter((entry) => entry.isDirectory())) {
        const runDir = path.join(dayDir, minute.name);
        if (path.resolve(runDir) === path.resolve(currentDir)) {
          continue;
        }
        const summaryPath = path.join(runDir, "summary.json");
        try {
          const payload = JSON.parse(await fs.readFile(summaryPath, "utf8"));
          runs.push({ runDir, summaryPath, payload });
        } catch {
          continue;
        }
      }
    }
    runs.sort((left, right) => String(left.payload.startedAt || "").localeCompare(String(right.payload.startedAt || "")));
    return runs;
  } catch {
    return [];
  }
}

async function runApiProbes(baseUrl) {
  const probeContext = await request.newContext({
    baseURL: baseUrl,
    ignoreHTTPSErrors: false,
  });
  const endpoints = ["/api/health", "/api/cases"];
  const results = [];
  for (const endpoint of endpoints) {
    try {
      const response = await probeContext.get(endpoint, { timeout: 30000 });
      const text = await response.text();
      results.push({
        endpoint,
        status: response.status(),
        ok: response.ok(),
        bodyPreview: sanitizeText(text, 240),
      });
    } catch (error) {
      results.push({
        endpoint,
        status: null,
        ok: false,
        error: sanitizeText(error?.message || error, 240),
      });
    }
  }
  await probeContext.dispose();
  return results;
}

async function captureAxe(page, axeSource) {
  try {
    await page.addScriptTag({ content: axeSource });
    const result = await page.evaluate(async () =>
      await window.axe.run(document, {
        runOnly: { type: "tag", values: ["wcag2a", "wcag2aa"] },
      }),
    );
    return {
      ok: true,
      summary: classifyAxeImpact(result.violations),
      violations: result.violations.map((item) => ({
        id: item.id,
        impact: item.impact,
        help: item.help,
        nodes: item.nodes.length,
      })),
    };
  } catch (error) {
    return {
      ok: false,
      error: sanitizeText(error?.message || error, 300),
      summary: { critical: 0, serious: 0, moderate: 0, minor: 0 },
      violations: [],
    };
  }
}

async function captureMetrics(page) {
  return page.evaluate(() => {
    const nav = performance.getEntriesByType("navigation")[0];
    const headings = [...document.querySelectorAll("h1, h2")]
      .map((node) => node.textContent?.trim())
      .filter(Boolean)
      .slice(0, 6);
    const focusable = [...document.querySelectorAll("a, button, input, select, textarea, [tabindex]:not([tabindex='-1'])")]
      .filter((node) => {
        const element = node;
        const style = window.getComputedStyle(element);
        return !element.hasAttribute("disabled") && style.visibility !== "hidden" && style.display !== "none";
      })
      .slice(0, 8)
      .map((node) => {
        const element = node;
        return {
          tag: element.tagName.toLowerCase(),
          text: (element.innerText || element.getAttribute("aria-label") || element.getAttribute("name") || "").trim().slice(0, 80),
        };
      });
    return {
      title: document.title,
      language: document.documentElement.lang || null,
      bodyPreview: (document.body?.innerText || "").replace(/\s+/g, " ").trim().slice(0, 500),
      headings,
      rootVisible: Boolean(document.querySelector("#root")),
      mainCount: document.querySelectorAll("main").length,
      dialogCount: document.querySelectorAll("[role='dialog'], dialog").length,
      formCount: document.querySelectorAll("form").length,
      buttonCount: document.querySelectorAll("button").length,
      imageCount: document.querySelectorAll("img").length,
      audioCount: document.querySelectorAll("audio").length,
      focusable,
      scrollWidth: document.documentElement.scrollWidth,
      innerWidth: window.innerWidth,
      innerHeight: window.innerHeight,
      overflow: document.documentElement.scrollWidth > window.innerWidth + 1,
      navigation: nav
        ? {
            type: nav.type,
            domContentLoadedMs: Math.round(nav.domContentLoadedEventEnd),
            loadMs: Math.round(nav.loadEventEnd),
            responseEndMs: Math.round(nav.responseEnd),
            transferSize: nav.transferSize,
            encodedBodySize: nav.encodedBodySize,
            decodedBodySize: nav.decodedBodySize,
          }
        : null,
    };
  });
}

async function auditRoute(browser, baseUrl, route, viewport, dirs, axeSource) {
  const baseName = screenshotName(route, viewport);
  const requestedUrl = sanitizeUrl(new URL(route, baseUrl).toString());
  const tracePath = path.join(dirs.traces, `${baseName}.zip`);
  const screenshotPath = path.join(dirs.screenshots, `${baseName}.png`);
  const logPath = path.join(dirs.logs, `${baseName}.json`);
  const context = await browser.newContext(browserContextOptions({
    viewport: { width: viewport.width, height: viewport.height },
    isMobile: viewport.mobile,
    hasTouch: viewport.mobile,
    locale: "en-US",
    colorScheme: "light",
    bypassCSP: true,
    recordVideo: { dir: dirs.videos, size: { width: viewport.width, height: viewport.height } },
  }));
  const page = await context.newPage();
  const video = page.video();
  const consoleMessages = [];
  const pageErrors = [];
  const requestFailures = [];
  const responses = [];
  page.on("console", (message) => {
    consoleMessages.push({ type: message.type(), text: sanitizeText(message.text(), 240) });
  });
  page.on("pageerror", (error) => {
    pageErrors.push({ text: sanitizeText(error?.message || error, 300) });
  });
  page.on("requestfailed", (requestItem) => {
    requestFailures.push({
      url: sanitizeUrl(requestItem.url()),
      method: requestItem.method(),
      resourceType: requestItem.resourceType(),
      failure: sanitizeText(requestItem.failure()?.errorText || "unknown failure", 240),
    });
  });
  page.on("response", async (response) => {
    const status = response.status();
    if (status >= 400 || response.request().resourceType() === "document") {
      responses.push({
        url: sanitizeUrl(response.url()),
        method: response.request().method(),
        status,
        resourceType: response.request().resourceType(),
      });
    }
  });

  let navigationError = null;
  await context.tracing.start({ screenshots: true, snapshots: true, sources: true });
  try {
    await page.goto(requestedUrl, { waitUntil: "domcontentloaded", timeout: 60000 });
    await page.waitForLoadState("networkidle", { timeout: 10000 }).catch(() => {});
  } catch (error) {
    navigationError = sanitizeText(error?.message || error, 300);
  }

  await page.screenshot({ path: screenshotPath, fullPage: true }).catch(() => {});
  await page.keyboard.press("Tab").catch(() => {});
  let metrics;
  try {
    metrics = await captureMetrics(page);
  } catch {
    metrics = {
      title: await page.title().catch(() => ""),
      language: null,
      bodyPreview: "",
      headings: [],
      rootVisible: false,
      mainCount: 0,
      dialogCount: 0,
      formCount: 0,
      buttonCount: 0,
      imageCount: 0,
      audioCount: 0,
      focusable: [],
      scrollWidth: viewport.width,
      innerWidth: viewport.width,
      innerHeight: viewport.height,
      overflow: false,
      navigation: null,
    };
  }
  const axe = await captureAxe(page, axeSource);
  const finalUrl = sanitizeUrl(page.url());
  const title = sanitizeText(await page.title().catch(() => ""), 160);
  const appUnavailable = isAppUnavailableSurface(title, metrics.bodyPreview, responses);
  const authWall =
    !appUnavailable && (
    /sign in|log in/i.test(title) ||
    /\/login\b/i.test(finalUrl) ||
    /sign in|log in/i.test(metrics.bodyPreview) ||
    (!metrics.rootVisible && Array.isArray(metrics.headings) && metrics.headings.some((item) => /sign in|log in/i.test(item))));

  await context.tracing.stop({ path: tracePath }).catch(() => {});
  await context.close();
  const videoPath = await finalizeVideo(video, path.join(dirs.videos, `${baseName}.webm`));

  const result = {
    route,
    viewport,
    requestedUrl,
    finalUrl,
    title,
    appUnavailable,
    authWall,
    navigationError,
    metrics: {
      ...metrics,
      bodyPreview: sanitizeText(metrics.bodyPreview, 500),
      title: sanitizeText(metrics.title, 160),
    },
    overflow: Boolean(metrics.overflow),
    axe,
    consoleMessages,
    pageErrors,
    requestFailures,
    responses,
    screenshotPath,
    tracePath,
    videoPath,
  };
  result.findings = summarizeFindings(result);
  await writeJson(logPath, result);
  return result;
}

async function maybeRunCaseJourney(browser, baseUrl, dirs) {
  const context = await browser.newContext(browserContextOptions({
    viewport: { width: 1920, height: 1080 },
    locale: "en-US",
    colorScheme: "light",
    bypassCSP: true,
    recordVideo: { dir: dirs.videos, size: { width: 1920, height: 1080 } },
  }));
  const page = await context.newPage();
  const video = page.video();
  const tracePath = path.join(dirs.traces, "case-042-journey.zip");
  const transitions = [];
  const experimentResults = [];
  let status = "NOT_TESTED";
  let authState = "UNKNOWN";
  let error = null;

  await context.tracing.start({ screenshots: true, snapshots: true, sources: true });
  try {
    await page.goto(baseUrl, { waitUntil: "domcontentloaded", timeout: 60000 });
    await page.waitForLoadState("networkidle", { timeout: 10000 }).catch(() => {});
    const title = await page.title();
    const bodyPreview = await page.locator("body").innerText().catch(() => "");
    const appUnavailable = isAppUnavailableSurface(title, bodyPreview, [
      {
        resourceType: "document",
        status: await page.locator("body").count().then(() => 200).catch(() => 200),
      },
    ]);
    if (appUnavailable) {
      authState = "UNAVAILABLE";
      status = "FAIL";
      const unavailablePath = path.join(dirs.screenshots, "case-042-app-unavailable.png");
      await page.screenshot({ path: unavailablePath, fullPage: true });
      transitions.push({ name: "app-unavailable", screenshotPath: unavailablePath, note: "Landing page rendered Databricks App Not Available." });
    } else if (
      /sign in|log in/i.test(title) ||
      /\/login\b/i.test(sanitizeUrl(page.url())) ||
      /sign in|log in/i.test(bodyPreview)
    ) {
      authState = "BLOCKED_AUTHENTICATION";
      status = "BLOCKED_AUTHENTICATION";
      const blockedPath = path.join(dirs.screenshots, "case-042-auth-blocked.png");
      await page.screenshot({ path: blockedPath, fullPage: true });
      transitions.push({ name: "auth-blocked", screenshotPath: blockedPath, note: "Landing page redirected to sign-in." });
    } else {
      authState = "AUTHENTICATED";
      const capture = async (name) => {
        const screenshotPath = path.join(dirs.screenshots, `${name}.png`);
        await page.screenshot({ path: screenshotPath, fullPage: true });
        transitions.push({ name, screenshotPath, url: page.url(), title: await page.title() });
      };
      await capture("case-042-landing");
      await page.getByRole("button", { name: "OPEN CASE BOARD" }).click();
      await capture("case-042-board");
      const startButton = page.getByRole("button", { name: /START INVESTIGATION/ });
      if (await startButton.count() === 0) {
        await page.getByRole("button", { name: "OPEN CASE" }).first().click();
      }
      await page.getByRole("button", { name: /START INVESTIGATION/ }).click();
      await capture("case-042-briefing");
      await page.getByLabel("Your prediction").selectOption("PRED_SOURCE_VALUES_CHANGED");
      await capture("case-042-prediction");
      for (let index = 0; index < 5; index += 1) {
        const buttonName = index === 0 ? /RUN GENIE’S FIRST EXPERIMENT/ : "RUN NEXT EXPERIMENT";
        const responsePromise = page.waitForResponse(
          (response) => response.url().includes("/next") && response.request().method() === "POST",
          { timeout: 120000 },
        );
        await page.getByRole("button", { name: buttonName }).click();
        const response = await responsePromise;
        const payload = await response.json().catch(() => ({}));
        experimentResults.push({
          experimentIndex: index + 1,
          experimentId: payload.experiment_id || null,
          experimentNumber: payload.experiment_number || null,
          readyForFinalPrediction: Boolean(payload.ready_for_final_prediction),
        });
        await page.waitForLoadState("networkidle", { timeout: 10000 }).catch(() => {});
        await capture(`case-042-experiment-${index + 1}`);
      }
      await page.getByRole("button", { name: "CONTINUE TO FINAL PREDICTION" }).click().catch(() => {});
      await capture("case-042-final-stage");
      if (await page.getByRole("button", { name: /INSPECT TX-004291/ }).count()) {
        await page.getByRole("button", { name: /INSPECT TX-004291/ }).click();
      }
      if (await page.getByRole("button", { name: /OPEN V2 LINEAGE/ }).count()) {
        await page.getByRole("button", { name: /OPEN V2 LINEAGE/ }).click();
      }
      if (await page.getByRole("button", { name: /INSPECT DQ MATERIALITY/ }).count()) {
        await page.getByRole("button", { name: /INSPECT DQ MATERIALITY/ }).click();
      }
      if (await page.getByRole("button", { name: /ASK DR\. GENIE/ }).count()) {
        await page.getByRole("button", { name: /ASK DR\. GENIE/ }).click();
        if (await page.locator("#genie-question").count()) {
          await page.locator("#genie-question").fill(SAFE_GENIE_QUESTION);
          await page.getByRole("button", { name: /SEND QUESTION/ }).click();
          await page.waitForTimeout(3000);
          await capture("case-042-genie-question");
        }
      }
      await page.getByLabel("FINAL PREDICTION").selectOption("FINAL_CHANGED_V2_SOURCE_RECORDS");
      const concludePromise = page.waitForResponse(
        (response) => response.url().includes("/conclude") && response.request().method() === "POST",
        { timeout: 120000 },
      );
      await page.getByRole("button", { name: /ACCEPT SCIENTIFIC VERDICT/ }).click();
      await concludePromise.catch(() => null);
      await capture("case-042-verdict");
      await page.getByRole("button", { name: /OPEN DEBRIEF/ }).click();
      await page.waitForLoadState("networkidle", { timeout: 10000 }).catch(() => {});
      await capture("case-042-debrief");
      status = "PASS";
    }
  } catch (journeyError) {
    status = status === "BLOCKED_AUTHENTICATION" ? status : "FAIL";
    error = sanitizeText(journeyError?.message || journeyError, 400);
    const failurePath = path.join(dirs.screenshots, "case-042-failure.png");
    await page.screenshot({ path: failurePath, fullPage: true }).catch(() => {});
    transitions.push({ name: "journey-failure", screenshotPath: failurePath, note: error });
  }

  await context.tracing.stop({ path: tracePath }).catch(() => {});
  await context.close();
  const videoPath = await finalizeVideo(video, path.join(dirs.videos, "case-042-journey.webm"));

  return {
    status,
    authState,
    error,
    tracePath,
    videoPath,
    transitions,
    experiments: experimentResults,
    safeQuestion: authState === "AUTHENTICATED" ? SAFE_GENIE_QUESTION : null,
  };
}

async function runCrossBrowserComparison(baseUrl, dirs, axeSource) {
  const attempts = [
    { name: "Firefox", launcher: firefox },
    { name: "WebKit", launcher: webkit },
  ];
  const unavailable = [];
  for (const attempt of attempts) {
    let browser;
    try {
      browser = await attempt.launcher.launch({ headless: true });
      const browserDirs = await createArtifactDirs(path.join(dirs.root, "cross-browser", attempt.name.toLowerCase()));
      const routeResults = [];
      for (const route of ROUTES) {
        for (const viewport of CROSS_BROWSER_VIEWPORTS) {
          routeResults.push(await auditRoute(browser, baseUrl, route, viewport, browserDirs, axeSource));
        }
      }
      await browser.close();
      return {
        available: true,
        browser: attempt.name,
        viewports: CROSS_BROWSER_VIEWPORTS.map((item) => item.label),
        artifactRoot: browserDirs.root,
        routeResults: routeResults.map((item) => ({
          route: item.route,
          viewport: item.viewport.label,
          status: item.appUnavailable ? "FAIL" : item.authWall ? "BLOCKED_AUTHENTICATION" : item.navigationError ? "FAIL" : item.overflow ? "WARN" : "PASS",
          title: item.title,
          finalUrl: item.finalUrl,
          appUnavailable: item.appUnavailable,
          overflow: item.overflow,
          axe: item.axe.summary,
          screenshotPath: item.screenshotPath,
          tracePath: item.tracePath,
          videoPath: item.videoPath,
        })),
        summary: {
          blockedAuthentication: routeResults.filter((item) => item.authWall).length,
          failedNavigation: routeResults.filter((item) => item.navigationError).length,
          overflow: routeResults.filter((item) => item.overflow).length,
          seriousOrCriticalA11y: routeResults.reduce(
            (count, item) => count + Number(item.axe.summary.critical || 0) + Number(item.axe.summary.serious || 0),
            0,
          ),
        },
        notes: [
          `${attempt.name} comparison covered all requested routes at representative desktop, tablet, and mobile viewports.`,
        ],
      };
    } catch (error) {
      unavailable.push(`${attempt.name} unavailable: ${sanitizeText(error?.message || error, 200)}`);
      if (browser) {
        await browser.close().catch(() => {});
      }
    }
  }
  return {
    available: false,
    browser: null,
    viewports: CROSS_BROWSER_VIEWPORTS.map((item) => item.label),
    artifactRoot: null,
    routeResults: [],
    summary: null,
    notes: unavailable.length ? unavailable : ["Firefox and WebKit were unavailable on this host."],
  };
}

function compareAgainstBaseline(previousRun, currentSummary) {
  if (!previousRun?.payload) {
    return {
      baselineFound: false,
      baselineRunDir: null,
      notes: ["No previous successful visual-QA baseline was available for comparison."],
      changedRoutes: [],
    };
  }
  const previousResults = new Map(
    (previousRun.payload.routeResults || []).map((item) => [`${item.route}::${item.viewport.label}`, item]),
  );
  const changedRoutes = [];
  for (const item of currentSummary.routeResults) {
    const key = `${item.route}::${item.viewport.label}`;
    const previous = previousResults.get(key);
    if (!previous) {
      changedRoutes.push({
        route: item.route,
        viewport: item.viewport.label,
        change: "No baseline result for this route/viewport pair.",
      });
      continue;
    }
    const previousFingerprint = JSON.stringify({
          title: previous.title,
          finalUrl: previous.finalUrl,
          appUnavailable: previous.appUnavailable,
          authWall: previous.authWall,
          headings: previous.metrics?.headings || [],
          mainCount: previous.metrics?.mainCount,
          buttonCount: previous.metrics?.buttonCount,
      overflow: previous.overflow,
      axe: previous.axe?.summary || {},
    });
    const currentFingerprint = JSON.stringify({
          title: item.title,
          finalUrl: item.finalUrl,
          appUnavailable: item.appUnavailable,
          authWall: item.authWall,
          headings: item.metrics?.headings || [],
          mainCount: item.metrics?.mainCount,
          buttonCount: item.metrics?.buttonCount,
      overflow: item.overflow,
      axe: item.axe?.summary || {},
    });
    if (previousFingerprint !== currentFingerprint) {
      changedRoutes.push({
        route: item.route,
        viewport: item.viewport.label,
        change: "Page title, auth state, route target, structure, overflow, or accessibility summary changed.",
      });
    }
  }
  return {
    baselineFound: true,
    baselineRunDir: previousRun.runDir,
    notes: changedRoutes.length
      ? ["Structural visual comparison found route-level changes versus the previous successful run."]
      : ["No meaningful route-level structural changes were detected versus the previous successful run."],
    changedRoutes,
  };
}

function isNetworkAccessBlockedError(value) {
  const text = String(value || "");
  return /ERR_NETWORK_ACCESS_DENIED|connect EACCES/i.test(text);
}

function determineOverall(routeResults, caseJourney) {
  if (routeResults.some((item) => item.appUnavailable) || caseJourney.status === "FAIL") {
    return "FAIL";
  }
  if (caseJourney.status === "BLOCKED_AUTHENTICATION" || routeResults.every((item) => item.authWall)) {
    return "BLOCKED_AUTHENTICATION";
  }
  if (routeResults.some((item) => item.navigationError)) {
    return "FAIL";
  }
  if (routeResults.some((item) => item.overflow) || routeResults.some((item) => item.axe?.summary?.critical || item.axe?.summary?.serious)) {
    return "WARN";
  }
  return "PASS";
}

function buildMatrix(routeResults) {
  return routeResults.map((item) => ({
    route: item.route,
    viewport: item.viewport.label,
    status: item.appUnavailable ? "FAIL" : item.authWall ? "BLOCKED_AUTHENTICATION" : item.navigationError ? "FAIL" : item.overflow ? "WARN" : "PASS",
    title: item.title,
    finalUrl: item.finalUrl,
  }));
}

function renderMarkdown(summary) {
  const lines = [];
  lines.push(`# MAD DATA LAB Visual QA Report`);
  lines.push("");
  lines.push(`- Overall: **${summary.overall}**`);
  lines.push(`- Timestamp: ${summary.startedAt}`);
  lines.push(`- Base URL: ${summary.baseUrl}`);
  lines.push(`- Authentication state: ${summary.authenticationState}`);
  lines.push(`- Browser: Chromium`);
  lines.push(`- Routes tested: ${summary.routes.join(", ")}`);
  lines.push(`- Viewports tested: ${summary.viewports.join(", ")}`);
  lines.push("");
  lines.push("## Executive Summary");
  lines.push("");
  lines.push(summary.executiveSummary);
  lines.push("");
  lines.push("## Pass/Fail Matrix");
  lines.push("");
  lines.push("| Route | Viewport | Status | Final URL | Title |");
  lines.push("| --- | --- | --- | --- | --- |");
  for (const item of summary.matrix) {
    lines.push(`| ${item.route} | ${item.viewport} | ${item.status} | ${item.finalUrl} | ${item.title || ""} |`);
  }
  lines.push("");
  lines.push("## Findings");
  lines.push("");
  if (!summary.findings.length) {
    lines.push("- No route-level defects were observed on the legitimately accessible surface.");
  } else {
    for (const finding of summary.findings) {
      lines.push(`### ${finding.severity} · ${finding.title}`);
      lines.push(`- Route: ${finding.route}`);
      lines.push(`- Viewport: ${finding.viewport}`);
      lines.push(`- Reproduction: ${finding.steps.join(" ")}`);
      lines.push(`- Expected: ${finding.expected}`);
      lines.push(`- Actual: ${finding.actual}`);
      lines.push(`- Impact: ${finding.impact}`);
      lines.push(`- Screenshot: ${finding.screenshot}`);
      lines.push(`- Trace: ${finding.trace}`);
      lines.push(`- Suggested fix: ${finding.suggestedFix}`);
      lines.push("");
    }
  }
  lines.push("## Route Results");
  lines.push("");
  for (const item of summary.routeResults) {
    lines.push(`### ${item.route} · ${item.viewport.label}`);
    lines.push(`- Status: ${item.appUnavailable ? "FAIL" : item.authWall ? "BLOCKED_AUTHENTICATION" : item.navigationError ? "FAIL" : item.overflow ? "WARN" : "PASS"}`);
    lines.push(`- Final URL: ${item.finalUrl}`);
    lines.push(`- Title: ${item.title}`);
    lines.push(`- Headings: ${(item.metrics.headings || []).join(" | ") || "None"}`);
    lines.push(`- Overflow: ${item.overflow ? "Yes" : "No"}`);
    lines.push(`- Axe summary: ${JSON.stringify(item.axe.summary)}`);
    lines.push(`- Screenshot: ${item.screenshotPath}`);
    lines.push(`- Trace: ${item.tracePath}`);
    lines.push(`- Video: ${item.videoPath || "Unavailable"}`);
    lines.push("");
  }
  lines.push("## Case #042 Journey");
  lines.push("");
  lines.push(`- Status: ${summary.caseJourney.status}`);
  lines.push(`- Authentication: ${summary.caseJourney.authState}`);
  if (summary.caseJourney.safeQuestion) {
    lines.push(`- Safe Genie question used: ${summary.caseJourney.safeQuestion}`);
  }
  if (summary.caseJourney.error) {
    lines.push(`- Error: ${summary.caseJourney.error}`);
  }
  lines.push(`- Trace: ${summary.caseJourney.tracePath}`);
  lines.push(`- Video: ${summary.caseJourney.videoPath || "Unavailable"}`);
  if (summary.caseJourney.experiments.length) {
    for (const experiment of summary.caseJourney.experiments) {
      lines.push(`- Experiment ${experiment.experimentIndex}: ${experiment.experimentId || "Unknown"} (${experiment.experimentNumber || "n/a"})`);
    }
  } else {
    lines.push("- Experiments: Not executed.");
  }
  lines.push("");
  lines.push("## Accessibility Results");
  lines.push("");
  lines.push(`- Serious or critical violations observed on accessible pages: ${summary.accessibility.seriousOrCriticalCount}`);
  lines.push(`- Axe run failures: ${summary.accessibility.failedRuns}`);
  lines.push("");
  lines.push("## Console, Network, Asset, and Runtime Errors");
  lines.push("");
  lines.push(`- Console errors/warnings captured: ${summary.runtime.consoleIssues}`);
  lines.push(`- Page errors captured: ${summary.runtime.pageErrors}`);
  lines.push(`- Failed requests captured: ${summary.runtime.requestFailures}`);
  lines.push(`- HTTP 4xx/5xx responses captured: ${summary.runtime.errorResponses}`);
  lines.push("");
  lines.push("## Performance Observations");
  lines.push("");
  lines.push(summary.performanceSummary);
  lines.push("");
  lines.push("## Visual Comparison");
  lines.push("");
  for (const note of summary.visualComparison.notes) {
    lines.push(`- ${note}`);
  }
  if (summary.visualComparison.baselineRunDir) {
    lines.push(`- Baseline run: ${summary.visualComparison.baselineRunDir}`);
  }
  for (const change of summary.visualComparison.changedRoutes.slice(0, 20)) {
    lines.push(`- ${change.route} @ ${change.viewport}: ${change.change}`);
  }
  lines.push("");
  lines.push("## Cross-Browser Comparison");
  lines.push("");
  if (!summary.crossBrowser.available) {
    lines.push("- Alternate browser run: NOT TESTED");
  } else {
    lines.push(`- Alternate browser run: ${summary.crossBrowser.browser}`);
    lines.push(`- Viewports: ${summary.crossBrowser.viewports.join(", ")}`);
    lines.push(`- Artifact root: ${summary.crossBrowser.artifactRoot}`);
    lines.push(`- Blocked authentication results: ${summary.crossBrowser.summary.blockedAuthentication}`);
    lines.push(`- Navigation failures: ${summary.crossBrowser.summary.failedNavigation}`);
    lines.push(`- Overflow findings: ${summary.crossBrowser.summary.overflow}`);
    lines.push(`- Serious/critical axe findings: ${summary.crossBrowser.summary.seriousOrCriticalA11y}`);
  }
  for (const note of summary.crossBrowser.notes) {
    lines.push(`- ${note}`);
  }
  lines.push("");
  lines.push("## Changes Since Previous Run");
  lines.push("");
  if (!summary.changesSincePreviousRun.length) {
    lines.push("- No prior successful run exists, so change tracking starts with this artifact set.");
  } else {
    for (const item of summary.changesSincePreviousRun) {
      lines.push(`- ${item}`);
    }
  }
  lines.push("");
  lines.push("## Prioritized Recommendations");
  lines.push("");
  for (const item of summary.recommendations.immediate) {
    lines.push(`- Immediate: ${item}`);
  }
  for (const item of summary.recommendations.nextIteration) {
    lines.push(`- Next iteration: ${item}`);
  }
  for (const item of summary.recommendations.cosmetic) {
    lines.push(`- Cosmetic: ${item}`);
  }
  lines.push("");
  lines.push("## Not Tested");
  lines.push("");
  for (const item of summary.notTested) {
    lines.push(`- ${item}`);
  }
  lines.push("");
  lines.push("## API Probes");
  lines.push("");
  for (const probe of summary.apiProbes) {
    lines.push(`- ${probe.endpoint}: ${probe.status ?? "n/a"} ${probe.ok ? "OK" : "NOT OK"}${probe.error ? ` · ${probe.error}` : ""}${probe.bodyPreview ? ` · ${probe.bodyPreview}` : ""}`);
  }
  return `${lines.join("\n")}\n`;
}

async function main() {
  const baseUrl = process.argv[2] || process.env.DEPLOYED_APP_URL || "https://mad-data-lab-7474643947913626.aws.databricksapps.com";
  const now = formatDateParts();
  const runDir = path.join(REPORT_ROOT, now.day, now.minute);
  try {
    await fs.access(runDir);
    throw new Error(`Refusing to overwrite existing run directory: ${runDir}`);
  } catch (error) {
    if (error.code !== "ENOENT") {
      throw error;
    }
  }
  const dirs = await createArtifactDirs(runDir);
  const axeSource = await fs.readFile(path.join(ROOT, "node_modules", "axe-core", "axe.min.js"), "utf8");
  const previousRuns = await listPreviousRuns(REPORT_ROOT, runDir);
  const previousSuccessfulRun = [...previousRuns].reverse().find((item) =>
    ["PASS", "WARN", "FAIL"].includes(String(item.payload.overall || "")),
  );
  const apiProbes = await runApiProbes(baseUrl);
  const browser = await chromium.launch({ headless: true });
  const routeResults = [];
  for (const route of ROUTES) {
    for (const viewport of VIEWPORTS) {
      routeResults.push(await auditRoute(browser, baseUrl, route, viewport, dirs, axeSource));
    }
  }
  const caseJourney = await maybeRunCaseJourney(browser, baseUrl, dirs);
  await browser.close();
  const crossBrowser = await runCrossBrowserComparison(baseUrl, dirs, axeSource);

  const findings = routeResults.flatMap((item) => item.findings);
  const overall = determineOverall(routeResults, caseJourney);
  const matrix = buildMatrix(routeResults);
  const unavailableCount = routeResults.filter((item) => item.appUnavailable).length;
  const authBlockedCount = routeResults.filter((item) => item.authWall).length;
  const accessibility = {
    seriousOrCriticalCount: routeResults.reduce(
      (count, item) => count + Number(item.axe.summary.critical || 0) + Number(item.axe.summary.serious || 0),
      0,
    ),
    failedRuns: routeResults.filter((item) => !item.axe.ok).length,
  };
  const runtime = {
    consoleIssues: routeResults.reduce((count, item) => count + item.consoleMessages.filter((entry) => entry.type === "error" || entry.type === "warning").length, 0),
    pageErrors: routeResults.reduce((count, item) => count + item.pageErrors.length, 0),
    requestFailures: routeResults.reduce((count, item) => count + item.requestFailures.length, 0),
    errorResponses: routeResults.reduce((count, item) => count + item.responses.filter((entry) => entry.status >= 400).length, 0),
  };
  const routeCount = routeResults.length;
  const networkBlockedCount = routeResults.filter((item) => isNetworkAccessBlockedError(item.navigationError)).length;
  const apiProbeNetworkBlocked = apiProbes.length > 0 && apiProbes.every((probe) => isNetworkAccessBlockedError(probe.error));
  const runnerNetworkBlocked = routeCount > 0 && networkBlockedCount === routeCount && apiProbeNetworkBlocked;
  const performanceEntries = routeResults
    .map((item) => item.metrics.navigation)
    .filter(Boolean)
    .map((item) => `${item.domContentLoadedMs}ms DCL / ${item.loadMs}ms load`);
  const performanceSummary = performanceEntries.length
    ? `Observed document timings ranged across accessible pages; sample navigation timings: ${performanceEntries.slice(0, 10).join(", ")}.`
    : "Navigation timing APIs were unavailable on the audited surface.";
  const authenticationState = runnerNetworkBlocked
    ? "RUNNER_NETWORK_BLOCKED"
    : caseJourney.authState === "AUTHENTICATED"
    ? "AUTHENTICATED"
    : unavailableCount && authBlockedCount
      ? "MIXED_UNAVAILABLE_AND_BLOCKED_AUTHENTICATION"
      : unavailableCount
        ? "UNAVAILABLE"
        : "BLOCKED_AUTHENTICATION";
  const visualComparison = compareAgainstBaseline(previousSuccessfulRun, { routeResults });
  const changesSincePreviousRun = visualComparison.baselineFound
    ? visualComparison.changedRoutes.map((item) => `${item.route} @ ${item.viewport}: ${item.change}`)
    : [];
  const notTested = [];
  if (runnerNetworkBlocked) {
    notTested.push("The runner could not reach the deployed host from this environment: every browser navigation failed with ERR_NETWORK_ACCESS_DENIED and both API probes failed with connect EACCES.");
    notTested.push("Authentication state was not validated because the deployment never loaded past transport-level network denial.");
    notTested.push("Case #042 catalog, investigation, all five experiments, evidence inspection, Genie interactions, final conclusion, verdict, scoring, badges, debrief, localization, and responsive product checks were not tested in the live app.");
  } else if (authenticationState !== "AUTHENTICATED") {
    if (unavailableCount) {
      notTested.push("Many deployed routes returned the Databricks App Not Available outage surface, so those product pages could not be audited.");
    }
    if (authBlockedCount) {
      notTested.push("Authenticated MAD DATA LAB app surfaces that did load beyond the outage shell were blocked by the Databricks sign-in wall, so the full product UI could not be audited.");
    }
    notTested.push("English and Spanish localization inside the authenticated product surface were not tested because the app did not load past authentication.");
    notTested.push("Case #042 catalog, investigation, all five experiments, evidence inspection, final conclusion, verdict, scoring, badges, and debrief were blocked by authentication.");
    notTested.push("Recovery and circuit-breaker behavior inside the live investigation flow were not tested because a session could not be created safely.");
  }
  const recommendations = {
    immediate: runnerNetworkBlocked
      ? ["Run this automation on a host with outbound access to the Databricks deployment, or restore egress for Playwright and API probes from the current runner."]
      : authenticationState !== "AUTHENTICATED"
      ? ["Provide a secure automation authentication path for the deployed review app so hourly visual QA can reach the actual product surface."]
      : ["Review any P1/P2 findings in this report before the next release candidate."],
    nextIteration: [
      "Keep this runner as the canonical hourly artifact source so future runs can compare route structure and state against a stable baseline.",
      "If auth is expected for production, add a dedicated automation-safe staging entry point or short-lived token injection for CI visual QA.",
    ],
    cosmetic: [
      "Once authenticated coverage is available, add Spanish screenshot baselines for the public routes and debrief states.",
    ],
  };
  const executiveSummary = runnerNetworkBlocked
    ? "This automation environment could not reach the live MAD DATA LAB deployment. All 54 Chromium route checks failed with ERR_NETWORK_ACCESS_DENIED, both API probes failed with connect EACCES, the Case #042 journey never started, and the resulting artifact set documents a runner-side network blocker rather than an application or authentication result."
    : authenticationState === "AUTHENTICATED"
    ? "The deployed app was reachable and the authenticated surface loaded, so the run completed the requested route matrix and attempted the Case #042 journey."
    : unavailableCount
      ? `The deployment did not present a stable product surface in this run: ${unavailableCount} route/viewport checks returned the Databricks App Not Available outage shell, and ${authBlockedCount} additional checks redirected to Databricks sign-in. The primary journey could not start, so the run is a live availability failure with remaining authenticated coverage blocked.`
      : "The target deployment was reachable, but every audited route in clean Chromium contexts resolved to a Databricks sign-in surface rather than the MAD DATA LAB application. This run therefore collected route, screenshot, accessibility, runtime, and API-probe evidence for the unauthenticated boundary and marked the primary in-app audit as BLOCKED_AUTHENTICATION.";

  const summary = {
    overall,
    startedAt: now.iso,
    baseUrl,
    authenticationState,
    browser: "Chromium",
    routes: ROUTES,
    viewports: VIEWPORTS.map((item) => item.label),
    executiveSummary,
    matrix,
    findings,
    routeResults,
    caseJourney,
    accessibility,
    runtime,
    performanceSummary,
    visualComparison,
    crossBrowser,
    changesSincePreviousRun,
    recommendations,
    notTested,
    apiProbes,
    artifactRoot: runDir,
    runHash: crypto.createHash("sha256").update(`${now.iso}:${baseUrl}`).digest("hex"),
  };

  await writeJson(path.join(runDir, "summary.json"), summary);
  const markdown = renderMarkdown(summary);
  await fs.writeFile(path.join(runDir, "report.md"), markdown, "utf8");
  await fs.writeFile(path.join(REPORT_ROOT, "LATEST.md"), markdown, "utf8");
  console.log(JSON.stringify({
    overall,
    runDir,
    reportPath: path.join(runDir, "report.md"),
    summaryPath: path.join(runDir, "summary.json"),
    authenticationState,
  }, null, 2));
}

main().catch((error) => {
  console.error(error?.stack || error?.message || String(error));
  process.exitCode = 1;
});
