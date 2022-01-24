import InterstitialDefinitionPage from "../generated_pages/interstitial_definition/interstitial-definition.page";

describe("Component: Interstitial Definition", () => {
  describe("Given I launch the interstitial definition questionnaire", () => {
    before(() => {
      browser.openQuestionnaire("test_interstitial_definition.json");
    });

    it("When there is a definition on an interstitial, then the page is displayed correctly", () => {
      expect($(InterstitialDefinitionPage.definitionTitle(1)).isDisplayed()).to.be.true;
      expect($(InterstitialDefinitionPage.definitionContent(1)).isDisplayed()).to.be.false;
      expect($(InterstitialDefinitionPage.definitionButton(1)).isDisplayed()).to.be.false;

      expect($(InterstitialDefinitionPage.definitionTitle(2)).isDisplayed()).to.be.true;
      expect($(InterstitialDefinitionPage.definitionContent(2)).isDisplayed()).to.be.false;
      expect($(InterstitialDefinitionPage.definitionButton(2)).isDisplayed()).to.be.false;
    });

    it("When I click on a definition title, the content and button is display for just that definition", () => {
      $(InterstitialDefinitionPage.definitionTitle(1)).click();

      expect($(InterstitialDefinitionPage.definitionTitle(1)).isDisplayed()).to.be.true;
      expect($(InterstitialDefinitionPage.definitionContent(1)).isDisplayed()).to.be.true;
      expect($(InterstitialDefinitionPage.definitionButton(1)).isDisplayed()).to.be.true;

      expect($(InterstitialDefinitionPage.definitionTitle(2)).isDisplayed()).to.be.true;
      expect($(InterstitialDefinitionPage.definitionContent(2)).isDisplayed()).to.be.false;
      expect($(InterstitialDefinitionPage.definitionButton(2)).isDisplayed()).to.be.false;
    });

    it("When I click on the hide content button, then the page is displayed correctly", () => {
      $(InterstitialDefinitionPage.definitionButton(1)).click();

      expect($(InterstitialDefinitionPage.definitionTitle(1)).isDisplayed()).to.be.true;
      expect($(InterstitialDefinitionPage.definitionContent(1)).isDisplayed()).to.be.false;
      expect($(InterstitialDefinitionPage.definitionButton(1)).isDisplayed()).to.be.false;

      expect($(InterstitialDefinitionPage.definitionTitle(2)).isDisplayed()).to.be.true;
      expect($(InterstitialDefinitionPage.definitionContent(2)).isDisplayed()).to.be.false;
      expect($(InterstitialDefinitionPage.definitionButton(2)).isDisplayed()).to.be.false;
    });
  });
});
