import RadioPage from "../generated_pages/theme_ons_nhs/radio.page";
import { expect } from "@wdio/globals";

describe("Theme NHSE", () => {
  describe("Given I launch a NHSE themed questionnaire", () => {
    before(async () => {
      await browser.openQuestionnaire("test_theme_ons_nhs.json");
    });

    it("When I navigate to the radio page, Then I should see NHSE theme content", async () => {
      await expect(browser).toHaveUrl(expect.stringContaining(RadioPage.pageName));
      await expect(await $("#ons-logo-stacked-en-alt").getHTML()).toContain("Office for National Statistics");
      await expect(await $("#nhs-logo-alt").getHTML()).toContain("National Heath Service");
    });
  });
});
