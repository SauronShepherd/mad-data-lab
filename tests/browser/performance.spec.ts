import { test, expect } from '@playwright/test';

test('Case #042 performance checkpoints remain bounded', async ({ page }) => {
  const timings: Record<string, number> = {};
  let start = Date.now();
  await page.goto('/');
  await expect(page.getByRole('button', { name: 'OPEN CASE BOARD' })).toBeVisible();
  timings.first_usable_screen_ms = Date.now() - start;
  await page.getByRole('button', { name: 'OPEN CASE BOARD' }).click();
  if (await page.getByRole('button', { name: /START INVESTIGATION/ }).count() === 0) await page.getByRole('button', { name: 'OPEN CASE' }).first().click();
  start = Date.now();
  await page.getByRole('button', { name: /START INVESTIGATION/ }).click();
  await expect(page.getByRole('button', { name: /RUN GENIE’S FIRST EXPERIMENT/ })).toBeVisible();
  timings.case_start_ms = Date.now() - start;
  timings.genie_response_ms = timings.case_start_ms;
  start = Date.now();
  await page.getByRole('button', { name: /RUN GENIE’S FIRST EXPERIMENT/ }).click();
  await expect(page.getByRole('button', { name: 'RUN NEXT EXPERIMENT' })).toBeVisible();
  timings.experiment_execution_ms = Date.now() - start;
  start = Date.now();
  await expect(page.getByText('EVIDENCE EXPLORER')).toBeVisible();
  timings.evidence_rendering_ms = Date.now() - start;
  for (let index = 0; index < 4; index += 1) {
    await page.getByRole('button', { name: 'RUN NEXT EXPERIMENT' }).click();
    await expect(page.getByRole('button', { name: index === 3 ? 'CONTINUE TO FINAL PREDICTION' : 'RUN NEXT EXPERIMENT' })).toBeVisible();
  }
  await page.getByRole('button', { name: 'CONTINUE TO FINAL PREDICTION' }).click();
  await page.getByRole('button', { name: /INSPECT TX-004291/ }).click();
  await page.getByRole('button', { name: /OPEN V2 LINEAGE/ }).click();
  await page.getByRole('button', { name: /INSPECT DQ MATERIALITY/ }).click();
  await page.getByLabel('FINAL PREDICTION').selectOption('FINAL_CHANGED_V2_SOURCE_RECORDS');
  start = Date.now();
  await page.getByRole('button', { name: /ACCEPT SCIENTIFIC VERDICT/ }).click();
  await expect(page.getByRole('button', { name: 'OPEN DEBRIEF →' })).toBeVisible();
  timings.verdict_submission_ms = Date.now() - start;
  console.log(`MDL-5 performance checkpoints ${JSON.stringify(timings)}`);
  expect(timings.first_usable_screen_ms).toBeLessThan(5000);
  expect(timings.case_start_ms).toBeLessThan(10000);
  expect(timings.experiment_execution_ms).toBeLessThan(10000);
});
