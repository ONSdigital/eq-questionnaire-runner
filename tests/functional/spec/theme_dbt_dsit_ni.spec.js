import RadioPage from "../generated_pages/theme_dbt_dsit_ni/radio.page";

describe("Theme DBT-DSIT-NI", () => {
  describe("Given I launch a DBT-DSIT-NI themed questionnaire", () => {
    before(async () => {
      await browser.openQuestionnaire("test_theme_dbt_dsit_ni.json");
    });

    it("When I navigate to the radio page, Then I should see DBT-DSIT-NI theme content", async () => {
      await expect(await browser.getUrl()).to.contain(RadioPage.pageName);
      await expect(await $("#dbt-logo-alt").getHTML()).to.contain("Department for Business and Trade logo");
      await expect(await $("#dsit-logo-alt").getHTML()).to.contain("Department for Science, Innovation and Technology logo");
      await expect(await $("#finance-ni-logo-alt").getHTML()).to.contain("Northern Ireland Department of Finance logo");
    });
  });
});
