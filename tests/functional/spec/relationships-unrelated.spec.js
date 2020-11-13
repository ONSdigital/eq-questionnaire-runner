import ListCollectorPage from "../generated_pages/relationships_unrelated/list-collector.page.js";
import ListCollectorAddPage from "../generated_pages/relationships_unrelated/list-collector-add.page.js";
import RelationshipsPage from "../generated_pages/relationships_unrelated/relationships.page.js";
import RelatedToAnyoneElsePage from "../generated_pages/relationships_unrelated/related-to-anyone-else.page.js";
import RelationshipsInterstitialPage from "../generated_pages/relationships_unrelated/relationship-interstitial.page.js";

describe("Unrelated Relationships", () => {
  const schema = "test_relationships_unrelated.json";

  describe("Given I am completing the test_relationships_unrelated survey,", () => {
    before("load the survey", () => {
      browser.openQuestionnaire(schema);
    });

    describe("And I add six people", () => {
      before("add people", () => {
        addPerson("Andrew", "Austin");
        addPerson("Betty", "Burns");
        addPerson("Carla", "Clark");
        addPerson("Daniel", "Davis");
        addPerson("Eve", "Elliot");
        $(ListCollectorPage.no()).click();
        $(ListCollectorPage.submit()).click();
      });

      it("When I answer 'Unrelated' twice, Then I will be asked if anyone else is related with a list of the remaining people", () => {
        $(RelationshipsPage.unrelated()).click();
        $(RelationshipsPage.submit()).click();
        $(RelationshipsPage.unrelated()).click();
        $(RelationshipsPage.submit()).click();
        expect($(RelatedToAnyoneElsePage.questionText()).getText()).to.contain("Are any of these people related to you?");
        expect($(RelatedToAnyoneElsePage.listLabel(1)).getText()).to.equal("Daniel Davis");
        expect($(RelatedToAnyoneElsePage.listLabel(2)).getText()).to.equal("Eve Elliot");
      });

      it("When I click previous, Then I will go back to the previous relationship", () => {
        $(RelatedToAnyoneElsePage.previous()).click();
        expect($(RelationshipsPage.questionText()).getText()).to.contain("Carla Clark is unrelated to Andrew Austin");
      });

      it("When I return to the 'related to anyone else' question and select 'Yes', Then I will be taken to the next relationship for the first person", () => {
        $(RelationshipsPage.submit()).click();
        $(RelatedToAnyoneElsePage.yes()).click();
        $(RelatedToAnyoneElsePage.submit()).click();
        expect($(RelationshipsPage.questionText()).getText()).to.contain("Thinking about Andrew Austin, Daniel Davis is their");
      });

      it("When I click previous, Then I will go back to the 'related to anyone else' question", () => {
        $(RelationshipsPage.previous()).click();
        expect($(RelatedToAnyoneElsePage.questionText()).getText()).to.contain("Are any of these people related to you?");
        expect($(RelatedToAnyoneElsePage.yes()).isSelected()).to.be.true;
      });

      it("When I select 'No' to the 'related to anyone else' question, Then I will be taken to the first relationship for the second person", () => {
        $(RelatedToAnyoneElsePage.noNoneOfThesePeopleAreRelatedToMe()).click();
        $(RelatedToAnyoneElsePage.submit()).click();
        expect($(RelationshipsPage.questionText()).getText()).to.contain("Thinking about Betty Burns, Carla Clark is their");
      });

      it("When I click previous, Then I will go back to the 'related to anyone else' question for the first person", () => {
        $(RelationshipsPage.previous()).click();
        expect($(RelatedToAnyoneElsePage.questionText()).getText()).to.contain("Are any of these people related to you?");
        expect($(RelatedToAnyoneElsePage.listLabel(1)).getText()).to.equal("Daniel Davis");
        expect($(RelatedToAnyoneElsePage.listLabel(2)).getText()).to.equal("Eve Elliot");
        expect($(RelatedToAnyoneElsePage.noNoneOfThesePeopleAreRelatedToMe()).isSelected()).to.be.true;
      });

      it("When I click complete the remaining relationships, Then I will go to the relationships section complete page", () => {
        $(RelatedToAnyoneElsePage.submit()).click();
        $(RelationshipsPage.unrelated()).click();
        $(RelationshipsPage.submit()).click();
        $(RelationshipsPage.unrelated()).click();
        $(RelationshipsPage.submit()).click();
        $(RelationshipsPage.unrelated()).click();
        $(RelationshipsPage.submit()).click();
        $(RelationshipsPage.unrelated()).click();
        $(RelationshipsPage.submit()).click();
        $(RelationshipsPage.unrelated()).click();
        $(RelationshipsPage.submit()).click();
        $(RelationshipsPage.unrelated()).click();
        $(RelationshipsPage.submit()).click();
        expect(browser.getUrl()).to.contain(RelationshipsInterstitialPage.pageName);
      });
    });

    function addPerson(firstName, lastName) {
      $(ListCollectorPage.yes()).click();
      $(ListCollectorPage.submit()).click();
      $(ListCollectorAddPage.firstName()).setValue(firstName);
      $(ListCollectorAddPage.lastName()).setValue(lastName);
      $(ListCollectorAddPage.submit()).click();
    }
  });
});
