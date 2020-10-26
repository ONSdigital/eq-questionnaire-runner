import InterstitialDefinitionPage from "../generated_pages/interstitial_definition/interstitial-definition.page";

describe("Component: Interstitial Definition", () => {
  describe("Given I launch the interstitial definition questionnaire", () => {
    before(() => {
      browser.openQuestionnaire("test_interstitial_definition.json");
    });

    it("When there is a definition on an interstitial, then the page is displayed correctly", () => {
      expect($(InterstitialDefinitionPage.definition0Title()).isDisplayed()).to.be.true;
      expect($(InterstitialDefinitionPage.definition0Content()).isDisplayed()).to.be.false;
      expect($(InterstitialDefinitionPage.definition0Button()).isDisplayed()).to.be.false;

      expect($(InterstitialDefinitionPage.definition1Title()).isDisplayed()).to.be.true;
      expect($(InterstitialDefinitionPage.definition1Content()).isDisplayed()).to.be.false;
      expect($(InterstitialDefinitionPage.definition1Button()).isDisplayed()).to.be.false;
    });

    it("When I click on a definition title, the content and button is display for just that definition", () => {
      $(InterstitialDefinitionPage.definition0Title()).click();

      expect($(InterstitialDefinitionPage.definition0Title()).isDisplayed()).to.be.true;
      expect($(InterstitialDefinitionPage.definition0Content()).isDisplayed()).to.be.true;
      expect($(InterstitialDefinitionPage.definition0Button()).isDisplayed()).to.be.true;

      expect($(InterstitialDefinitionPage.definition1Title()).isDisplayed()).to.be.true;
      expect($(InterstitialDefinitionPage.definition1Content()).isDisplayed()).to.be.false;
      expect($(InterstitialDefinitionPage.definition1Button()).isDisplayed()).to.be.false;
    });

    it("When I click on the hide content button, then the page is displayed correctly", () => {
      $(InterstitialDefinitionPage.definition0Button()).click();

      expect($(InterstitialDefinitionPage.definition0Title()).isDisplayed()).to.be.true;
      expect($(InterstitialDefinitionPage.definition0Content()).isDisplayed()).to.be.false;
      expect($(InterstitialDefinitionPage.definition0Button()).isDisplayed()).to.be.false;

      expect($(InterstitialDefinitionPage.definition1Title()).isDisplayed()).to.be.true;
      expect($(InterstitialDefinitionPage.definition1Content()).isDisplayed()).to.be.false;
      expect($(InterstitialDefinitionPage.definition1Button()).isDisplayed()).to.be.false;
    });
  });
});
