import { test, expect } from '@playwright/test';

for (const route of ['library', 'articles', 'groups', 'variants', 'feedback', 'comments', 'account', 'admin']) {
  test(`public route /${route} renders and returns to lab`, async ({ page }) => {
    await page.goto(`/${route}`);
    await expect(page.locator('#root')).toBeVisible();
    await expect(page.locator('main.public-hub')).toBeVisible();
    await expect(page.getByRole('button', { name: 'RETURN TO LAB' })).toBeVisible();
    await page.getByRole('button', { name: 'RETURN TO LAB' }).click();
    await expect(page.getByRole('button', { name: 'OPEN CASE BOARD' })).toBeVisible();
  });
}

test('preferences and feedback persist locally', async ({ page }) => {
  await page.goto('/account');
  await page.locator('select').nth(0).selectOption('es');
  await page.locator('select').nth(1).selectOption('high-contrast');
  await expect.poll(() => page.evaluate(() => localStorage.getItem('mad-data-lab-language'))).toBe('es');
  await page.goto('/feedback');
  await page.locator('#feedback-message').fill('The evidence flow is clear.');
  await page.getByRole('button', { name: /SEND FEEDBACK|ENVIAR COMENTARIOS/ }).click();
  await expect(page.getByRole('alert')).toContainText(/Feedback saved locally|Comentarios guardados localmente/);
});

test('public controls cover variants, comments, subscription and administration', async ({ page }) => {
  await page.goto('/variants');
  await page.getByRole('button', { name: 'OPEN CASE BOARD' }).click();
  await expect(page.getByRole('button', { name: 'OPEN CASE', exact: true })).toBeVisible();

  await page.goto('/comments');
  await page.locator('#comment-message').fill('Snapshot evidence reviewed.');
  await page.getByRole('button', { name: 'POST COMMENT' }).click();
  await expect(page.getByRole('alert')).toContainText('Comment saved locally');
  await expect.poll(() => page.evaluate(() => localStorage.getItem('mad-data-lab-comment'))).toBe('saved');

  await page.goto('/account');
  await page.getByRole('button', { name: /MANAGE SUBSCRIPTION|GESTIONAR SUSCRIPCIÓN/ }).click();
  await expect(page.getByRole('alert')).toContainText(/Subscription checkout is not enabled|checkout de suscripción no está habilitado/);

  await page.goto('/admin');
  await expect(page.locator('pre')).toContainText('cases');
});

test('articles follow the persisted language after navigation and reload', async ({ page }) => {
  await page.addInitScript(() => localStorage.setItem('mad-data-lab-language', 'es'));
  await page.goto('/articles');
  await expect(page.getByRole('heading', { name: 'Artículos de la comunidad' })).toBeVisible();
  await expect(page.getByText('Maravilloso. Algo no cuadra.')).toBeVisible();
  await page.reload();
  await expect(page.getByRole('heading', { name: 'Artículos de la comunidad' })).toBeVisible();
  await expect(page.getByRole('button', { name: 'VOLVER AL LABORATORIO' })).toBeVisible();
});

test('articles do not expose the removed Apache Spark WTF entry', async ({ page }) => {
  await page.goto('/articles');
  await expect(page.locator('body')).not.toContainText(/Apache Spark WTF\?\?\?/i);
});

test('all public surfaces localize their primary copy to Spanish', async ({ page }) => {
  await page.addInitScript(() => localStorage.setItem('mad-data-lab-language', 'es'));
  const expected = {
    library: 'Biblioteca de evidencias',
    articles: 'Artículos de la comunidad',
    groups: 'Grupos de casos',
    variants: 'Variantes del caso',
    feedback: 'Comentarios',
    comments: 'Comentarios de la investigación',
    account: 'Cuenta y suscripción',
    admin: 'Administración',
  };
  for (const [route, heading] of Object.entries(expected)) {
    await page.goto(`/${route}`);
    await expect(page.getByRole('heading', { name: heading })).toBeVisible();
  }
});
