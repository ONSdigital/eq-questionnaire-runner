import RadioPage from "../generated_pages/theme_dbt_dsit/radio.page";
import { verifyUrlContains } from "../helpers";

describe("Theme DBT-DSIT", () => {
  describe("Given I launch a DBT-DSIT themed questionnaire", () => {
    before(async () => {
      await browser.openQuestionnaire("test_theme_dbt_dsit.json");
    });

    it("When I navigate to the radio page, Then I should see DBT-DSIT theme content", async () => {
      await verifyUrlContains(RadioPage.pageName);
      await expect(await $("#dbt-logo-alt").getHTML({ includeSelectorTag: false, prettify: false })).toContain("Department for Business and Trade logo");
      await expect(await $("#dsit-logo-alt").getHTML({ includeSelectorTag: false, prettify: false })).toContain(
        "Department for Science, Innovation and Technology logo",
      );
    });
  });
});
