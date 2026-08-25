import { test, expect } from '@playwright/test';

test('same-origin Case #042 browser contract', async ({ page, request }) => {
  const health = await request.get('/health');
  expect(health.ok()).toBeTruthy();
  const cases = await request.get('/api/cases');
  expect((await cases.json()).cases.some((item: {id: string}) => item.id === 'CASE_0042')).toBeTruthy();
  await page.goto('/');
  await expect(page.locator('#root')).toBeVisible();
  await expect(page).not.toHaveTitle(/error/i);
});
