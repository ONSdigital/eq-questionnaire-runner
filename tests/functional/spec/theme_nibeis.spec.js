import RadioPage from "../generated_pages/theme_beisni/radio.page";

describe("Theme BEISNI", () => {
  describe("Given I launch a BEISNI themed questionnaire", () => {
    before(() => {
      browser.openQuestionnaire("test_theme_beisni.json");
    });

    it("When I navigate to the radio page, Then I should see BEISNI theme content", () => {
      expect(browser.getUrl()).to.contain(RadioPage.pageName);
      expect($("#beis-logo-alt").getHTML()).to.contain("Department for Business, Energy and Industrial Strategy");
      expect($("#ni-finance-logo-alt").getHTML()).to.contain("Northern Ireland Department of Finance logo");
    });
  });
});
