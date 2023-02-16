import RadioPage from "../generated_pages/theme_orr/radio.page";

describe("Theme Rail and Road", () => {
  describe("Given I launch a Rail and Road themed questionnaire", () => {
    before(async ()=> {
      await browser.openQuestionnaire("test_theme_orr.json");
    });

    it("When I navigate to the radio page, Then I should see Rail and Road theme content", async ()=> {
      await expect(browser.getUrl()).to.contain(RadioPage.pageName);
      await expect($("#orr-logo-mobile-alt").getHTML()).to.contain("Office of Rail and Road logo");
    });
  });
});
