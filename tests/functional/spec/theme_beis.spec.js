import RadioPage from "../generated_pages/theme_beis/radio.page";

describe("Theme BEIS", () => {
  describe("Given I launch a BEIS themed questionnaire", () => {
    before(async () => {
      await browser.openQuestionnaire("test_theme_beis.json");
    });

    it("When I navigate to the radio page, Then I should see BEIS theme content", async () => {
      await expect(await browser.getUrl()).to.contain(RadioPage.pageName);
      await expect(await $("#beis-logo-alt").getHTML()).to.contain("Department for Business, Energy and Industrial Strategy");
    });
  });
});
