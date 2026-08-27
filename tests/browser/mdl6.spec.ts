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
