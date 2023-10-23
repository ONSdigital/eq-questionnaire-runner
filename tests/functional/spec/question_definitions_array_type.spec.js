import DefinitionPage from "../generated_pages/question_definition/definition-block.page";

describe("Component: Definition", () => {
  describe("Given I start a survey which contains question definition", () => {
    beforeEach(async () => {
      await browser.openQuestionnaire("test_question_definition_array_type.json");
    });

    it("When I click the title link, then the description should be visible", async () => {
      await expect(await $(DefinitionPage.definitionContent()).getText()).toBe("");

      // When
      await $(DefinitionPage.definitionTitle()).click();

      // Then
      await expect(await $(DefinitionPage.definitionContent()).getText()).toContain(
        "A typical photovoltaic system employs solar panels, each comprising a number of solar cells, which generate electrical power."
      );
    });

    it("When I click the title link twice, then the description should not be visible", async () => {
      await expect(await $(DefinitionPage.definitionContent()).getText()).toBe("");

      // When
      await $(DefinitionPage.definitionTitle()).click();
      await $(DefinitionPage.definitionTitle()).click();

      // Then
      await expect(await $(DefinitionPage.definitionContent()).getText()).toBe("");
    });
  });
});
