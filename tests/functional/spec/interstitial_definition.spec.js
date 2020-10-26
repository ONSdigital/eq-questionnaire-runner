import InterstitialDefinitionPage from "../generated_pages/interstitial_definition/interstitial-definition.page";

describe("Component: Interstitial Definition", () => {
  describe("Given I launch the interstitial definition questionnaire", () => {
    before(() => {
      browser.openQuestionnaire("test_interstitial_definition.json");
    });

    it("When there is a definition on an interstitial, then the page is displayed correctly", () => {
      expect($(InterstitialDefinitionPage.definitionSuccessfullyTitle()).isDisplayed()).to.be.true;
      expect($(InterstitialDefinitionPage.definitionSuccessfullyContent()).isDisplayed()).to.be.false;
      expect($(InterstitialDefinitionPage.definitionSuccessfullyButton()).isDisplayed()).to.be.false;

      expect($(InterstitialDefinitionPage.definitionQuestionnaireTitle()).isDisplayed()).to.be.true;
      expect($(InterstitialDefinitionPage.definitionQuestionnaireContent()).isDisplayed()).to.be.false;
      expect($(InterstitialDefinitionPage.definitionQuestionnaireButton()).isDisplayed()).to.be.false;
    });

    it("When I click on a definition title, the content and button is display for just that definition", () => {
      $(InterstitialDefinitionPage.definitionSuccessfullyTitle()).click();

      expect($(InterstitialDefinitionPage.definitionSuccessfullyTitle()).isDisplayed()).to.be.true;
      expect($(InterstitialDefinitionPage.definitionSuccessfullyContent()).isDisplayed()).to.be.true;
      expect($(InterstitialDefinitionPage.definitionSuccessfullyButton()).isDisplayed()).to.be.true;

      expect($(InterstitialDefinitionPage.definitionQuestionnaireTitle()).isDisplayed()).to.be.true;
      expect($(InterstitialDefinitionPage.definitionQuestionnaireContent()).isDisplayed()).to.be.false;
      expect($(InterstitialDefinitionPage.definitionQuestionnaireButton()).isDisplayed()).to.be.false;
    });

    it("When I click on the hide content button, then the page is displayed correctly", () => {
      $(InterstitialDefinitionPage.definitionSuccessfullyButton()).click();

      expect($(InterstitialDefinitionPage.definitionSuccessfullyTitle()).isDisplayed()).to.be.true;
      expect($(InterstitialDefinitionPage.definitionSuccessfullyContent()).isDisplayed()).to.be.false;
      expect($(InterstitialDefinitionPage.definitionSuccessfullyButton()).isDisplayed()).to.be.false;

      expect($(InterstitialDefinitionPage.definitionQuestionnaireTitle()).isDisplayed()).to.be.true;
      expect($(InterstitialDefinitionPage.definitionQuestionnaireContent()).isDisplayed()).to.be.false;
      expect($(InterstitialDefinitionPage.definitionQuestionnaireButton()).isDisplayed()).to.be.false;
    });
  });
});
