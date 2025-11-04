import RadioPage from "../generated_pages/theme_ons_nhs/radio.page";
import { expect } from "@wdio/globals";
import { verifyUrlContains } from "../helpers";

describe("Theme NHSE", () => {
  describe("Given I launch a NHSE themed questionnaire", () => {
    before(async () => {
      await browser.openQuestionnaire("test_theme_ons_nhs.json");
    });

    it("When I navigate to the radio page, Then I should see NHSE theme content", async () => {
      await verifyUrlContains(RadioPage.pageName);
      await expect(await $("#ons-logo-stacked-en-alt").getHTML({ prettify: false }) prettify: false })).toContain("Office for National Statistics");
      await expect(await $("#nhs-logo-alt").getHTML({ prettify: false })).toContain("National Heath Service");
    });
  });
});
