import RadioPage from "../generated_pages/theme_dbt/radio.page";
import { verifyUrlContains, getRawHTMLrom "../helpers";

describe("Theme DBT", () => {
  describe("Given I launch a DBT themed questionnaire", () => {
    before(async () => {
      await browser.openQuestionnaire("test_theme_dbt.json");
    });

    it("When I navigate to the radio page, Then I should see DBT theme content", async () => {
      await verifyUrlContains(RadioPage.pageName);
      await expect(await getRawHTML("#dbt-logo-alt"))).toContain("Department for Business and Trade");
    });
  });
});
