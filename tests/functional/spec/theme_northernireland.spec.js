import RadioPage from "../generated_pages/theme_northernireland/radio.page";

describe("Theme Northern Ireland", () => {
  describe("Given I launch a Northern Ireland themed questionnaire", () => {
    before(() => {
      browser.openQuestionnaire("test_theme_northernireland.json");
    });

    it("When I navigate to the radio page, Then I should see Northern Ireland theme content", () => {
      expect(browser.getUrl()).to.contain(RadioPage.pageName);
      expect($("#finance-ni-logo-alt").getHTML()).to.contain("Northern Ireland Department of Finance logo");
    });
  });
});
