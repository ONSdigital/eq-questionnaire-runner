import DefinitionPage from "../generated_pages/question_definition/definition-block.page";

describe("Component: Definition", () => {
  describe("Given I start a survey which contains question definition", () => {
    beforeEach(() => {
      browser.openQuestionnaire("test_question_definition.json");
    });

    it("When I click the title link, then the description should be visible", () => {
      expect($(DefinitionPage.definitionContent(1)).isDisplayed()).to.be.false;

      // When
      $(DefinitionPage.definitionTitle("1")).click();

      // Then
      $(DefinitionPage.definitionContent(1)).waitForDisplayed({ timeout: 300 });
    });

    it("When I click the title link twice, then the description should not be visible", () => {
      expect($(DefinitionPage.definitionContent(1)).isDisplayed()).to.be.false;

      // When
      $(DefinitionPage.definitionTitle("1")).click();
      $(DefinitionPage.definitionTitle("1")).click();

      // Then
      $(DefinitionPage.definitionContent(1)).waitForDisplayed({ timeout: 300, reverse: true });
    });
  });
});
