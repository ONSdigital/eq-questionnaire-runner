import RadioPage from "../generated_pages/theme_orr/radio.page";
import { verifyUrlContains } from "../helpers";

describe("Theme Rail and Road", () => {
  describe("Given I launch a Rail and Road themed questionnaire", () => {
    before(async () => {
      await browser.openQuestionnaire("test_theme_orr.json");
    });

    it("When I navigate to the radio page, Then I should see Rail and Road theme content", async () => {
      await verifyUrlContains(RadioPage.pageName);
      await expect(await $("#orr-logo-mobile-alt").getHTML({ prettify: false })).toContain("Office of Rail and Road logo");
    });
  });
});
