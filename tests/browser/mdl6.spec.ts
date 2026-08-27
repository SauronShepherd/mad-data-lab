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
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth + 1)).toBeTruthy();
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
