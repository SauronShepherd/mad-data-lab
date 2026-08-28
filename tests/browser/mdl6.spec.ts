import { test, expect } from '@playwright/test';

test('MDL-6 missing-session API exposes a safe recoverable envelope', async ({ request }) => {
  const response = await request.get('/api/sessions/does-not-exist');
  expect(response.status()).toBe(404);
  const body = await response.json();
  expect(body.error.code).toBe('SESSION_NOT_FOUND');
  expect(body.error.request_id).toBeTruthy();
  expect(JSON.stringify(body)).not.toMatch(/traceback|stack|private_truth/i);
});

test('MDL-6 mobile shell keeps primary action reachable', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto('/');
  await expect(page.getByRole('button', { name: 'OPEN CASE BOARD' })).toBeVisible();
  await page.getByRole('button', { name: 'OPEN CASE BOARD' }).click();
  await expect(page.getByRole('button', { name: /OPEN CASE|START INVESTIGATION/ }).first()).toBeVisible();
  const layout = await page.evaluate(() => ({
    width: document.documentElement.scrollWidth,
    viewport: window.innerWidth,
    offenders: [...document.querySelectorAll('*')]
      .filter((item) => item.getBoundingClientRect().right > window.innerWidth + 1)
      .slice(0, 8)
      .map((item) => ({ tag: item.tagName, cls: item.className, right: item.getBoundingClientRect().right })),
  }));
  expect(layout.width, JSON.stringify(layout)).toBeLessThanOrEqual(layout.viewport + 1);
});

test('MDL-6 production artwork is reachable and decodable', async ({ page, request }) => {
  for (const asset of ['/assets/mdl6-achievement-badges.png', '/assets/mdl6-recovery-background.png']) {
    const response = await request.get(asset);
    expect(response.status()).toBe(200);
    expect(response.headers()['content-type']).toContain('image/png');
  }
  await page.goto('/');
  const decoded = await page.evaluate(async () => Promise.all([
    '/assets/mdl6-achievement-badges.png',
    '/assets/mdl6-recovery-background.png',
  ].map((src) => new Promise((resolve, reject) => {
    const image = new Image();
    image.onload = () => resolve({ src, width: image.naturalWidth, height: image.naturalHeight });
    image.onerror = reject;
    image.src = src;
  }))));
  expect(decoded).toHaveLength(2);
  expect(decoded.every((item) => item.width > 0 && item.height > 0)).toBeTruthy();
});

test('MDL-6 keyboard-only path reaches the investigation briefing', async ({ page }) => {
  await page.goto('/');
  await page.getByRole('button', { name: 'OPEN CASE BOARD' }).focus();
  await page.keyboard.press('Enter');
  const open = page.getByRole('button', { name: /OPEN CASE/ }).first();
  if (await open.count()) {
    await open.focus();
    await page.keyboard.press('Enter');
  }
  const start = page.getByRole('button', { name: /START INVESTIGATION/ });
  await expect(start).toBeVisible();
  await start.focus();
  await page.keyboard.press('Enter');
  await expect(page.getByRole('button', { name: /RUN GENIE’S FIRST EXPERIMENT/ })).toBeVisible({ timeout: 120_000 });
});

test('MDL-6 failed catalog request does not expose a playable analytical fallback', async ({ page }) => {
  await page.route('**/api/cases', (route) => route.abort());
  await page.goto('/');
  await expect(page.getByText(/remote catalog unavailable/i)).toBeVisible();
  await page.getByRole('button', { name: 'OPEN CASE BOARD' }).click();
  await expect(page.getByRole('button', { name: 'OPEN CASE' })).toHaveCount(0);
});

test('MDL-6 desktop layout remains usable at 1440x900', async ({ page }) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto('/');
  await expect(page.getByRole('button', { name: 'OPEN CASE BOARD' })).toBeVisible();
  const overflow = await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth + 1);
  expect(overflow).toBeFalsy();
});

test('MDL-6 compact desktop layout remains usable at 1280x720', async ({ page }) => {
  await page.setViewportSize({ width: 1280, height: 720 });
  await page.goto('/');
  await expect(page.getByRole('button', { name: 'OPEN CASE BOARD' })).toBeVisible();
  const overflow = await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth + 1);
  expect(overflow).toBeFalsy();
});

test('MDL-6 rejected autoplay does not block the first action', async ({ page }) => {
  await page.addInitScript(() => {
    HTMLMediaElement.prototype.play = () => Promise.reject(new DOMException('autoplay blocked', 'NotAllowedError'));
  });
  await page.goto('/');
  await page.getByRole('button', { name: /laboratory music/ }).click();
  await expect(page.getByRole('button', { name: 'OPEN CASE BOARD' })).toBeEnabled();
  await page.getByRole('button', { name: 'OPEN CASE BOARD' }).click();
  await expect(page.getByRole('button', { name: /OPEN CASE|START INVESTIGATION/ }).first()).toBeVisible();
});

test('MDL-6 illustration 404 preserves usable controls', async ({ page }) => {
  await page.route('**/assets/mdl6-recovery-background.png', (route) => route.fulfill({ status: 404, body: 'missing' }));
  await page.goto('/');
  await expect(page.getByRole('button', { name: 'OPEN CASE BOARD' })).toBeVisible();
  await expect(page.locator('#root')).toBeVisible();
});

test('MDL-6 network restoration allows catalog retry', async ({ page }) => {
  let offline = true;
  await page.route('**/api/cases', async (route) => {
    if (offline) return route.abort();
    return route.continue();
  });
  await page.goto('/');
  await expect(page.getByText(/remote catalog unavailable/i)).toBeVisible();
  offline = false;
  await page.reload();
  await expect(page.getByRole('button', { name: 'OPEN CASE BOARD' })).toBeVisible();
});
