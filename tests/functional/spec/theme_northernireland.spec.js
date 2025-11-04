import RadioPage from "../generated_pages/theme_northernireland/radio.page";
import { verifyUrlContains } from "../helpers";

describe("Theme Northern Ireland", () => {
  describe("Given I launch a Northern Ireland themed questionnaire", () => {
    before(async () => {
      await browser.openQuestionnaire("test_theme_northernireland.json");
    });

    it("When I navigate to the radio page, Then I should see Northern Ireland theme content", async () => {
      await verifyUrlContains(RadioPage.pageName);
      await expect(await $("#finance-ni-logo-alt").getHTML({ prettify: false }) prettify: false })).toContain("Northern Ireland Department of Finance logo");
    });
  });
});
