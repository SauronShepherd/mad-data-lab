import { test, expect } from '@playwright/test';

for (const viewport of [{ width: 1920, height: 1080 }, { width: 1440, height: 900 }, { width: 1366, height: 768 }]) {
  test(`Case #042 investigation layout fits ${viewport.width}x${viewport.height}`, async ({ page }) => {
    await page.setViewportSize(viewport);
    await page.goto('/');
    await page.getByRole('button', { name: 'OPEN CASE BOARD' }).click();
    if (await page.getByRole('button', { name: /START INVESTIGATION/ }).count() === 0) {
      await page.getByRole('button', { name: 'OPEN CASE' }).first().click();
    }
    await page.getByRole('button', { name: /START INVESTIGATION/ }).click();
    await expect(page.getByLabel('State-driven investigation map')).toBeVisible();
    expect(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth)).toBeTruthy();
    expect(await page.locator('.side').evaluate((node) => node.getBoundingClientRect().bottom <= window.innerHeight + 2 || window.innerWidth < 801)).toBeTruthy();
  });
}
