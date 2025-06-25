import RadioPage from "../generated_pages/theme_dbt_ni/radio.page";
import { expect } from "@wdio/globals";
import { verifyUrlContains } from "../helpers";

describe("Theme UKHSA-ONS", () => {
  describe("Given I launch a UKHSA-ONS themed questionnaire", () => {
    before(async () => {
      await browser.openQuestionnaire("test_theme_ukhsa_ons.json");
    });

    it("When I navigate to the radio page, Then I should see UKHSA-ONS theme content", async () => {
      await verifyUrlContains(RadioPage.pageName);
      await expect(await $("#ons-logo-stacked-en-alt").getText()).toContain("Office for National Statistics");
      await expect(await $("#ukhsa-logo-alt").getText()).toContain("UK Health Security Agency");
    });
  });
});
