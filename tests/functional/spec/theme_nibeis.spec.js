import RadioPage from "../generated_pages/theme_nibeis/radio.page";

describe("Theme NIBEIS", () => {
  describe("Given I launch a NIBEIS themed questionnaire", () => {
    before(() => {
      browser.openQuestionnaire("test_theme_nibeis.json");
    });

    it("When I navigate to the radio page, Then I should see NIBEIS theme content", () => {
      expect(browser.getUrl()).to.contain(RadioPage.pageName);
      expect($("#nibeis-logo-alt").getHTML()).to.contain("Department for Business, Energy and Industrial Strategy");
    });
  });
});
