import RadioPage from "../generated_pages/theme_ons_nhs/radio.page";
import { expect } from "@wdio/globals";
import { verifyUrlContains, getRawHTML } from "../helpers";

describe("Theme NHSE", () => {
  describe("Given I launch a NHSE themed questionnaire", () => {
    before(async () => {
      await browser.openQuestionnaire("test_theme_ons_nhs.json");
    });

    it("When I navigate to the radio page, Then I should see NHSE theme content", async () => {
      await verifyUrlContains(RadioPage.pageName);
      await expect(await getRawHTML("#ons-logo-stacked-en-alt", { includeSelectorTag: false })).toContain("Office for National Statistics");
      await expect(await getRawHTML("#nhs-logo-alt", { includeSelectorTag: false })).toContain("National Heath Service");
    });
  });
});
