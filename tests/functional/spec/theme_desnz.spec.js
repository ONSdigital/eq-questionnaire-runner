import RadioPage from "../generated_pages/theme_desnz/radio.page";

describe("Theme DESNZ", () => {
  describe("Given I launch a DESNZ themed questionnaire", () => {
    before(async () => {
      await browser.openQuestionnaire("test_theme_desnz.json");
    });

    it("When I navigate to the radio page, Then I should see DESNZ theme content", async () => {
      await expect(await browser.getUrl()).to.contain(RadioPage.pageName);
      await expect(await $("#desnz-logo-alt").getHTML()).to.contain("Department for Energy Security and Net Zero");
    });
  });
});
