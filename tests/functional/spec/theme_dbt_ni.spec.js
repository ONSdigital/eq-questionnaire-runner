import RadioPage from "../generated_pages/theme_dbt_ni/radio.page";
import { verifyUrlContains, getInnerHTML } from "../helpers";

describe("Theme DBT-NI", () => {
  describe("Given I launch a DBT-NI themed questionnaire", () => {
    before(async () => {
      await browser.openQuestionnaire("test_theme_dbt_ni.json");
    });

    it("When I navigate to the radio page, Then I should see DBT-NI theme content", async () => {
      await verifyUrlContains(RadioPage.pageName);
      await expect(await getInnerHTML($("#dbt-logo-alt"))).toContain("Department for Business and Trade");
      await expect(await getInnerHTML($("#finance-ni-logo-alt"))).toContain("Northern Ireland Department of Finance logo");
    });
  });
});
