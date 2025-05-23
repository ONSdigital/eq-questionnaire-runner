import RadioPage from "../generated_pages/theme_desnz/radio.page";
import { verifyUrlContains } from "../helpers";

describe("Theme DESNZ", () => {
  describe("Given I launch a DESNZ themed questionnaire", () => {
    before(async () => {
      await browser.openQuestionnaire("test_theme_desnz.json");
    });

    it("When I navigate to the radio page, Then I should see DESNZ theme content", async () => {
      await verifyUrlContains(RadioPage.pageName);
      await expect(await $("#desnz-logo-alt").getHTML()).toContain("Department for Energy Security and Net Zero");
    });
  });
});
