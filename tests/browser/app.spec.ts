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

test('audio failure does not block first interaction', async ({ page }) => {
  await page.route('**/audio/mad_data_lab_curiosity.mp3', (route) => route.abort());
  await page.goto('/');
  await page.getByRole('button', {name: 'Play laboratory music'}).click();
  await page.getByRole('button', {name: 'OPEN CASE BOARD'}).click();
  await expect(page.getByRole('button', {name: /START INVESTIGATION|OPEN CASE/}).first()).toBeVisible();
  await expect(page).not.toHaveTitle(/error/i);
});

test('music control persists mute preference and uses a looped track', async ({ page }) => {
  await page.goto('/');
  const audio = page.locator('audio');
  await expect(audio).toHaveAttribute('loop', '');
  await page.getByRole('button', {name: 'Play laboratory music'}).click();
  await expect(page.getByRole('button', {name: 'Mute laboratory music'})).toBeVisible();
  await expect.poll(() => page.evaluate(() => localStorage.getItem('mad-data-lab-audio'))).toBe('on');
  await page.getByRole('button', {name: 'Mute laboratory music'}).click();
  await expect.poll(() => page.evaluate(() => localStorage.getItem('mad-data-lab-audio'))).toBe('off');
});

test('Case #042 visible flow reaches final prediction and Debrief', async ({ page }) => {
  await page.goto('/');
  await page.getByRole('button', {name: 'OPEN CASE BOARD'}).click();
  const start = page.getByRole('button', {name: /START INVESTIGATION/});
  if (await start.count() === 0) {
    await page.getByRole('button', {name: 'OPEN CASE'}).first().click();
  }
  await page.getByRole('button', {name: /START INVESTIGATION/}).click();
  await page.getByLabel('Your prediction').selectOption('PRED_SOURCE_VALUES_CHANGED');
  await Promise.all([
    page.waitForResponse((response) => response.url().includes('/next') && response.request().method() === 'POST'),
    page.getByRole('button', {name: /RUN GENIE’S FIRST EXPERIMENT/}).click(),
  ]);
  await page.reload();
  await expect(page.getByRole('button', {name: 'RUN NEXT EXPERIMENT'})).toBeVisible();
  for (let index = 0; index < 4; index += 1) {
    await Promise.all([
      page.waitForResponse((response) => response.url().includes('/next') && response.request().method() === 'POST'),
      page.getByRole('button', {name: 'RUN NEXT EXPERIMENT'}).click(),
    ]);
  }
  await page.getByRole('button', {name: 'CONTINUE TO FINAL PREDICTION'}).click();
  await expect(page.getByLabel('FINAL PREDICTION')).toBeVisible();
  await page.getByRole('button', {name: /INSPECT TX-004291/}).click();
  await page.getByRole('button', {name: /OPEN V2 LINEAGE/}).click();
  await page.getByRole('button', {name: /INSPECT DQ MATERIALITY/}).click();
  await page.getByLabel('FINAL PREDICTION').selectOption('FINAL_CHANGED_V2_SOURCE_RECORDS');
  await Promise.all([
    page.waitForResponse((response) => response.url().includes('/conclude') && response.request().method() === 'POST'),
    page.getByRole('button', {name: /ACCEPT SCIENTIFIC VERDICT/}).click(),
  ]);
  await expect(page.getByRole('button', {name: 'OPEN DEBRIEF →'})).toBeVisible();
  await page.getByRole('button', {name: 'OPEN DEBRIEF →'}).click();
  await expect(page.getByText('LAB SCORE')).toBeVisible();
  await expect(page.getByText('✦ DATA_APPRENTICE', {exact: true})).toHaveCount(1);
});
