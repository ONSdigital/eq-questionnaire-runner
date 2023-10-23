import InterstitialDefinitionPage from "../generated_pages/interstitial_definition/interstitial-definition.page";

describe("Component: Interstitial Definition", () => {
  describe("Given I launch the interstitial definition questionnaire", () => {
    before(async () => {
      await browser.openQuestionnaire("test_interstitial_definition.json");
    });

    it("When there is a definition on an interstitial, then the page is displayed correctly", async () => {
      await expect(await $(InterstitialDefinitionPage.definitionTitle()).isDisplayed()).toBe(true);
      await expect(await $(InterstitialDefinitionPage.definitionContent()).getText()).toBe("");
    });

    it("When I click on a definition title, the content is displayed for just that definition", async () => {
      await $(InterstitialDefinitionPage.definitionTitle()).click();

      await expect(await $(InterstitialDefinitionPage.definitionTitle()).isDisplayed()).toBe(true);
      await expect(await $(InterstitialDefinitionPage.definitionContent()).getText()).toBe("In a way that accomplishes a desired aim or result");
    });
  });
});
