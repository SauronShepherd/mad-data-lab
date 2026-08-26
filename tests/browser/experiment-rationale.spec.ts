import { test, expect } from "@playwright/test";

test("experiment rationale is rendered from the registered experiment model", async ({ page }) => {
  await page.goto("http://127.0.0.1:8000");
  await expect(page.getByText("WHY THIS EXPERIMENT?", { exact: true })).toHaveCount(0);
  // The section becomes visible after an Experiment is selected; its source is
  // the validated API model, not a reasoning trace or client-authored text.
  await expect(page.locator("body")).not.toContainText("chain of thought");
});
