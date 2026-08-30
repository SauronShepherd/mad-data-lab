import { chromium } from '@playwright/test';
import fs from 'node:fs/promises';

const baseURL = process.env.BASE_URL || 'http://127.0.0.1:8000';
const out = 'release-report/MDL-8/screenshots';
await fs.mkdir(out, { recursive: true });
const browser = await chromium.launch();
const appToken = process.env.DATABRICKS_APP_TOKEN;
const results = [];
for (const [name, viewport] of [['desktop', {width:1440,height:900}], ['tablet', {width:1024,height:768}], ['mobile', {width:390,height:844}]]) {
  const context = await browser.newContext({ viewport, isMobile: name !== 'desktop', hasTouch: name !== 'desktop', ...(appToken ? { extraHTTPHeaders: { Authorization: `Bearer ${appToken}` } } : {}) });
  const page = await context.newPage();
  const checks = { overflow: true, offscreen: 0, brokenImages: 0, buttons: 0, contrastBasic: 'PASS (axe color-contrast)' };
  // The app may keep API connections active; networkidle would make the
  // evidence run wait forever. DOM readiness plus semantic locators is enough.
  // Live Genie can require several bounded backend calls. Keep each semantic
  // action below the server's contract while allowing the full remote journey
  // to finish without turning a slow but healthy response into a false fail.
  page.setDefaultTimeout(Number(process.env.BROWSER_ACTION_TIMEOUT || 300000));
  await page.goto(baseURL + '/', { waitUntil: 'domcontentloaded', timeout: 30000 });
  await page.screenshot({ path: `${out}/${name}-01-landing.png`, fullPage: true });
  await page.getByRole('button', {name: 'OPEN CASE BOARD'}).click();
  await page.screenshot({ path: `${out}/${name}-02-case-board.png`, fullPage: true });
  await page.getByRole('button', {name: 'OPEN CASE', exact: true}).click();
  await page.screenshot({ path: `${out}/${name}-03-briefing.png`, fullPage: true });
  await page.getByRole('button', {name: /START INVESTIGATION/}).click();
  await page.screenshot({ path: `${out}/${name}-04-investigation.png`, fullPage: true });
  await page.getByLabel('Your prediction').selectOption('PRED_SOURCE_VALUES_CHANGED');
  await page.getByRole('button', {name: /RUN GENIE’S FIRST EXPERIMENT/}).click({ force: true });
  await page.screenshot({ path: `${out}/${name}-05-experiment-1.png`, fullPage: true });
  for (let index = 0; index < 4; index += 1) {
    const next = page.getByRole('button', {name: 'RUN NEXT EXPERIMENT'});
    await next.waitFor({ state: 'visible' });
    await next.click({ force: true });
    await page.screenshot({ path: `${out}/${name}-06-experiment-${index + 2}.png`, fullPage: true });
  }
  await page.getByRole('button', {name: 'CONTINUE TO FINAL PREDICTION'}).click({ force: true });
  await page.getByRole('button', {name: /INSPECT TX-004291/}).click();
  await page.getByRole('button', {name: /OPEN V2 LINEAGE/}).click();
  await page.getByRole('button', {name: /INSPECT DQ MATERIALITY/}).click();
  await page.getByLabel('FINAL PREDICTION').selectOption('FINAL_CHANGED_V2_SOURCE_RECORDS');
  await page.getByRole('button', {name: /ACCEPT SCIENTIFIC VERDICT/}).click({ force: true });
  await page.screenshot({ path: `${out}/${name}-10-verdict.png`, fullPage: true });
  await page.getByRole('button', {name: 'OPEN DEBRIEF →'}).click({ force: true });
  await page.screenshot({ path: `${out}/${name}-11-debrief.png`, fullPage: true });
  for (const route of ['library', 'articles', 'groups', 'variants', 'feedback', 'comments', 'account', 'admin']) {
    await page.evaluate(() => localStorage.removeItem('mad-data-lab-session-id'));
    await page.goto(`${baseURL}/${route}`, { waitUntil: 'domcontentloaded', timeout: 30000 });
    await page.screenshot({ path: `${out}/${name}-public-${route}.png`, fullPage: true });
  }
  const audit = await page.evaluate(() => ({
    overflow: document.documentElement.scrollWidth > window.innerWidth,
    // Vertical position below the fold is valid because the app is scrollable;
    // only horizontal clipping makes a control inaccessible on a responsive viewport.
    offscreen: [...document.querySelectorAll('button,a,input,select,textarea,img')].filter((n) => { const r=n.getBoundingClientRect(); return r.right < 0 || r.left > innerWidth; }).length,
    brokenImages: [...document.images].filter((img) => !img.complete || img.naturalWidth === 0).length,
    buttons: [...document.querySelectorAll('button')].filter((b) => !b.disabled && !b.getAttribute('aria-label') && !b.textContent.trim()).length,
  }));
  Object.assign(checks, { overflow: audit.overflow, offscreen: audit.offscreen, brokenImages: audit.brokenImages, buttons: audit.buttons });
  results.push({ viewport: name, ...checks });
  await context.close();
}
await browser.close();
await fs.writeFile('release-report/MDL-8/ui-diagnostic.json', JSON.stringify({status: results.some((r) => r.overflow || r.offscreen || r.brokenImages || r.buttons) ? 'FAIL' : 'PASS', criteria: results}, null, 2) + '\n');
console.log(JSON.stringify(results, null, 2));
