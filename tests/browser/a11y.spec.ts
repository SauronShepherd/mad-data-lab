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

test('runtime axe reports no serious or critical violations on every public route', async ({ page }) => {
  const axeSource = fs.readFileSync('node_modules/axe-core/axe.min.js', 'utf8');
  for (const route of ['/', '/library', '/articles', '/groups', '/variants', '/feedback', '/comments', '/account', '/admin']) {
    await page.goto(route);
    await page.addScriptTag({ content: axeSource });
    const result = await page.evaluate(async () => await (window as any).axe.run(document, { runOnly: { type: 'tag', values: ['wcag2a', 'wcag2aa'] } }));
    const serious = result.violations.filter((item: any) => item.impact === 'serious' || item.impact === 'critical');
    expect(serious, `${route}: ${JSON.stringify(serious)}`).toEqual([]);
    const contrast = result.violations.filter((item: any) => item.id === 'color-contrast');
    expect(contrast, `${route}: contrast ${JSON.stringify(contrast)}`).toEqual([]);
  }
});
