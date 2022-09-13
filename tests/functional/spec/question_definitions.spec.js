import DefinitionPage from "../generated_pages/question_definition/definition-block.page";

describe("Component: Definition", () => {
  describe("Given I start a survey which contains question definition", () => {
    beforeEach(() => {
      browser.openQuestionnaire("test_question_definition.json");
    });

    it("When I click the title link, then the description should be visible", () => {
      expect($(DefinitionPage.definitionContent(1)).getText()).to.equal("");

      // When
      $(DefinitionPage.definitionTitle("1")).click();

      // Then
      expect($(DefinitionPage.definitionContent(1)).getText()).to.contain(
        "A typical photovoltaic system employs solar panels, each comprising a number of solar cells, which generate electrical power."
      );
    });

    it("When I click the title link twice, then the description should not be visible", () => {
      expect($(DefinitionPage.definitionContent(1)).getText()).to.equal("");

      // When
      $(DefinitionPage.definitionTitle("1")).click();
      $(DefinitionPage.definitionTitle("1")).click();

      // Then
      expect($(DefinitionPage.definitionContent(1)).getText()).to.equal("");
    });
  });
});
