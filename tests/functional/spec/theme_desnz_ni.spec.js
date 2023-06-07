import RadioPage from "../generated_pages/theme_dbt_ni/radio.page";

describe("Theme DESNZ-NI", () => {
  describe("Given I launch a DESNZ-NI themed questionnaire", () => {
    before(async () => {
      await browser.openQuestionnaire("test_theme_dbt_ni.json");
    });

    it("When I navigate to the radio page, Then I should see DESNZ-NI theme content", async () => {
      await expect(await browser.getUrl()).to.contain(RadioPage.pageName);
      await expect(await $("#desnz-logo-alt").getHTML()).to.contain("Department for Energy Security and Net Zero");
      await expect(await $("#finance-ni-logo-alt").getHTML()).to.contain("Northern Ireland Department of Finance logo");
    });
  });
});
