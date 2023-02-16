import RadioPage from "../generated_pages/theme_beis_ni/radio.page";

describe("Theme BEIS-NI", () => {
  describe("Given I launch a BEIS-NI themed questionnaire", () => {
    before(async ()=> {
      await browser.openQuestionnaire("test_theme_beis_ni.json");
    });

    it("When I navigate to the radio page, Then I should see BEIS-NI theme content", async ()=> {
      await expect(browser.getUrl()).to.contain(RadioPage.pageName);
      await expect($("#beis-logo-mobile-alt").getHTML()).to.contain("Department for Business, Energy and Industrial Strategy");
      await expect($("#finance-ni-logo-alt").getHTML()).to.contain("Northern Ireland Department of Finance logo");
    });
  });
});
