import RadioPage from "../generated_pages/theme_northernireland/radio.page";
import SubmitPage from "../generated_pages/theme_northernireland/submit.page.js";

describe("Theme Northern Ireland", () => {
  describe("Given I launch a Northern Ireland themed questionnaire", () => {
    before(() => {
      browser.openQuestionnaire("test_theme_northernireland.json");
    });

    it("When I navigate to the radio page, Then I should see Northern Ireland theme content", () => {
      expect(browser.getUrl()).to.contain(RadioPage.pageName);
      expect($("#ni-finance-logo-alt").isExisting()).to.equal(true);
      expect($("#ni-finance-logo-alt").getHTML()).to.contain("Northern Ireland Department of Finance logo");
    });
    it("When I navigate to the submit page, Then I should see Northern Ireland theme content", () => {
      $(SubmitPage.submit()).click();
      expect(browser.getUrl()).to.contain(SubmitPage.pageName);
      expect($("#ni-finance-logo-alt").isExisting()).to.equal(true);
      expect($("#ni-finance-logo-alt").getHTML()).to.contain("Northern Ireland Department of Finance logo");
    });
  });
});
