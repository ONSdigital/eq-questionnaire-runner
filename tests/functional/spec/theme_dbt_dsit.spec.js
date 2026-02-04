import RadioPage from "../generated_pages/theme_dbt_dsit/radio.page";
import { verifyUrlContains, getRawHTMLm "../helpers";

describe("Theme DBT-DSIT", () => {
  describe("Given I launch a DBT-DSIT themed questionnaire", () => {
    before(async () => {
      await browser.openQuestionnaire("test_theme_dbt_dsit.json");
    });

    it("When I navigate to the radio page, Then I should see DBT-DSIT theme content", async () => {
      await verifyUrlContains(RadioPage.pageName);
      await expect(await getRawHTML#dbt-logo-alt"))).toContain("Department for Business and Trade logo");
      await expect(await getRawHTML("#dsit-logo-alt"))).toContain("Department for Science, Innovation and Technology logo");
    });
  });
});
