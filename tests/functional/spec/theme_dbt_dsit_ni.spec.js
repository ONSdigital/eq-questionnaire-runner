import RadioPage from "../generated_pages/theme_dbt_dsit_ni/radio.page";
import { verifyUrlContains, getRawHTML } from "../helpers";

describe("Theme DBT-DSIT-NI", () => {
  describe("Given I launch a DBT-DSIT-NI themed questionnaire", () => {
    before(async () => {
      await browser.openQuestionnaire("test_theme_dbt_dsit_ni.json");
    });

    it("When I navigate to the radio page, Then I should see DBT-DSIT-NI theme content", async () => {
      await verifyUrlContains(RadioPage.pageName);
      await expect(await getRawHTML($("#dbt-logo-alt"))).toContain("Department for Business and Trade logo");
      await expect(await getRawHTML($("#dsit-logo-alt"))).toContain("Department for Science, Innovation and Technology logo");
      await expect(await getRawHTML($("#finance-ni-logo-alt"))).toContain("Northern Ireland Department of Finance logo");
    });
  });
});
