import DefinitionPage from "../generated_pages/question_definition/definition-block.page";

describe("Component: Definition", () => {
  describe("Given I start a survey which contains question definition", () => {
    beforeEach(() => {
      browser.openQuestionnaire("test_question_definition.json");
    });

    it('When I click the title link, then the description and "Hide this" button should be visible', () => {
      expect($(DefinitionPage.definitionContent(1)).isDisplayed()).to.be.false;
      expect($(DefinitionPage.definitionButton(1)).isDisplayed()).to.be.false;

      // When
      $(DefinitionPage.definitionTitle("1")).click();

      // Then
      $(DefinitionPage.definitionContent(1)).waitForDisplayed({ timeout: 300 });
      $(DefinitionPage.definitionButton(1)).waitForDisplayed({ timeout: 300 });
    });

    it('When I click the title link twice, then the description and "Hide this" button should not be visible', () => {
      expect($(DefinitionPage.definitionContent(1)).isDisplayed()).to.be.false;
      expect($(DefinitionPage.definitionButton(1)).isDisplayed()).to.be.false;

      // When
      $(DefinitionPage.definitionTitle("1")).click();
      $(DefinitionPage.definitionTitle("1")).click();

      // Then
      $(DefinitionPage.definitionContent(1)).waitForDisplayed({ timeout: 300, reverse: true });
      $(DefinitionPage.definitionButton(1)).waitForDisplayed({ timeout: 300, reverse: true });
    });

    it('When I click the title link then click "Hide this" button, then the description and button should not be visible', () => {
      expect($(DefinitionPage.definitionContent(1)).isDisplayed()).to.be.false;
      expect($(DefinitionPage.definitionButton(1)).isDisplayed()).to.be.false;

      // When
      $(DefinitionPage.definitionTitle("1")).click();

      // Then
      $(DefinitionPage.definitionContent(1)).waitForDisplayed({ timeout: 300 });
      $(DefinitionPage.definitionButton(1)).waitForDisplayed({ timeout: 300 });

      // When
      $(DefinitionPage.definitionButton(1)).click();

      // Then
      $(DefinitionPage.definitionContent(1)).waitForDisplayed({ timeout: 300, reverse: true });
      $(DefinitionPage.definitionButton(1)).waitForDisplayed({ timeout: 300, reverse: true });
    });

    it('When I click the second definition\'s title link then the description and "Hide this" button for the second definition should be visible', () => {
      expect($(DefinitionPage.definitionContent(2)).isDisplayed()).to.be.false;
      expect($(DefinitionPage.definitionButton(2)).isDisplayed()).to.be.false;

      // When
      $(DefinitionPage.definitionTitle("2")).click();

      // Then
      $(DefinitionPage.definitionContent(2)).waitForDisplayed({ timeout: 300 });
      $(DefinitionPage.definitionButton(2)).waitForDisplayed({ timeout: 300 });
    });
  });
});
