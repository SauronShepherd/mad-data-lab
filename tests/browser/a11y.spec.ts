import { test, expect } from '@playwright/test';
import fs from 'node:fs';

test('keyboard and dialog accessibility contract', async ({ page }) => {
  await page.goto('/');
  await page.getByRole('button', { name: 'OPEN CASE BOARD' }).focus();
  await expect(page.getByRole('button', { name: 'OPEN CASE BOARD' })).toBeFocused();
  await page.keyboard.press('Enter');
  await page.getByRole('button', { name: 'Help' }).click();
  const dialog = page.getByRole('dialog');
  await expect(dialog).toBeVisible();
  await page.waitForTimeout(100);
  const close = dialog.getByRole('button', { name: 'Close panel' });
  await close.focus();
  await expect(close).toBeFocused();
  await page.keyboard.press('Tab');
  await page.keyboard.press('Tab');
  await page.keyboard.press('Shift+Tab');
  await expect(close).toBeFocused();
  await page.keyboard.press('Escape');
  await expect(dialog).toBeHidden();
});

test('runtime axe reports no serious or critical violations', async ({ page }) => {
  await page.goto('/');
  const axeSource = fs.readFileSync('node_modules/axe-core/axe.min.js', 'utf8');
  await page.addScriptTag({ content: axeSource });
  const result = await page.evaluate(async () => await (window as any).axe.run(document));
  const serious = result.violations.filter((item: any) => item.impact === 'serious' || item.impact === 'critical');
  expect(serious, JSON.stringify(serious)).toEqual([]);
});
