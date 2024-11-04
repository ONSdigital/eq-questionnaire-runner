import RadioPage from "../generated_pages/theme_desnz_ni/radio.page";
import { verifyUrlContains } from "../helpers";

describe("Theme DESNZ-NI", () => {
  describe("Given I launch a DESNZ-NI themed questionnaire", () => {
    before(async () => {
      await browser.openQuestionnaire("test_theme_desnz_ni.json");
    });

    it("When I navigate to the radio page, Then I should see DESNZ-NI theme content", async () => {
      await verifyUrlContains(RadioPage.pageName);
      await expect(await $("#desnz-logo-alt").getHTML()).toContain("Department for Energy Security and Net Zero");
      await expect(await $("#finance-ni-logo-alt").getHTML()).toContain("Northern Ireland Department of Finance logo");
    });
  });
});
