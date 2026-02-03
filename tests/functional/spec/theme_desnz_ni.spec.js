import RadioPage from "../generated_pages/theme_desnz_ni/radio.page";
import { verifyUrlContains, getInnerHTML } from "../helpers";

describe("Theme DESNZ-NI", () => {
  describe("Given I launch a DESNZ-NI themed questionnaire", () => {
    before(async () => {
      await browser.openQuestionnaire("test_theme_desnz_ni.json");
    });

    it("When I navigate to the radio page, Then I should see DESNZ-NI theme content", async () => {
      await verifyUrlContains(RadioPage.pageName);
      await expect(await getInnerHTML($("#desnz-logo-alt"))).toContain("Department for Energy Security and Net Zero");
      await expect(await getInnerHTML($("#finance-ni-logo-alt"))).toContain("Northern Ireland Department of Finance logo");
    });
  });
});
