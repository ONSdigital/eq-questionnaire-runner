import RadioPage from "../generated_pages/theme_beis/radio.page";

describe("Theme ORR", () => {
  describe("Given I launch a ORR themed questionnaire", () => {
    before(() => {
      browser.openQuestionnaire("test_theme_orr.json");
    });

    it("When I navigate to the radio page, Then I should see ORR theme content", () => {
      expect(browser.getUrl()).to.contain(RadioPage.pageName);
      expect($("#orr-logo-alt").getHTML()).to.contain("Office of Rail and Road");
    });
  });
});
