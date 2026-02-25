import { test, expect } from "@playwright/test";

test.describe("Layout spec", () => {
  test("spec layout matches baseline", async ({ page }) => {
    await page.goto("/specs/layout");
    await page.waitForTimeout(300);
    await expect(page).toHaveScreenshot("layout.png", {
      maxDiffPixelRatio: 0.02,
      fullPage: true,
    });
  });
});

