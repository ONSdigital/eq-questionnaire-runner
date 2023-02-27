import ListCollectorPage from "../generated_pages/relationships_unrelated/list-collector.page.js";
import ListCollectorAddPage from "../generated_pages/relationships_unrelated/list-collector-add.page.js";
import RelationshipsPage from "../generated_pages/relationships_unrelated/relationships.page.js";
import RelatedToAnyoneElsePage from "../generated_pages/relationships_unrelated/related-to-anyone-else.page.js";
import RelationshipsInterstitialPage from "../generated_pages/relationships_unrelated/relationship-interstitial.page.js";

describe("Unrelated Relationships", () => {
  const schema = "test_relationships_unrelated.json";

  describe("Given I am completing the test_relationships_unrelated survey,", () => {
    before("load the survey", async () => {
      await browser.openQuestionnaire(schema);
    });

    describe("And I add six people", () => {
      before("add people", async () => {
        await addPerson("Andrew", "Austin");
        await addPerson("Betty", "Burns");
        await addPerson("Carla", "Clark");
        await addPerson("Daniel", "Davis");
        await addPerson("Eve", "Elliot");
        await $(ListCollectorPage.no()).click();
        await $(ListCollectorPage.submit()).click();
      });

      it("When I answer 'Unrelated' twice, Then I will be asked if anyone else is related with a list of the remaining people", async () => {
        await $(RelationshipsPage.unrelated()).click();
        await $(RelationshipsPage.submit()).click();
        await $(RelationshipsPage.unrelated()).click();
        await $(RelationshipsPage.submit()).click();
        await expect(await $(RelatedToAnyoneElsePage.questionText()).getText()).to.contain("Are any of these people related to you?");
        await expect(await $(RelatedToAnyoneElsePage.listLabel(1)).getText()).to.equal("Daniel Davis");
        await expect(await $(RelatedToAnyoneElsePage.listLabel(2)).getText()).to.equal("Eve Elliot");
      });

      it("When I click previous, Then I will go back to the previous relationship", async () => {
        await $(RelatedToAnyoneElsePage.previous()).click();
        await expect(await $(RelationshipsPage.questionText()).getText()).to.contain("Carla Clark is unrelated to Andrew Austin");
      });

      it("When I return to the 'related to anyone else' question and select 'Yes', Then I will be taken to the next relationship for the first person", async () => {
        await $(RelationshipsPage.submit()).click();
        await $(RelatedToAnyoneElsePage.yes()).click();
        await $(RelatedToAnyoneElsePage.submit()).click();
        await expect(await $(RelationshipsPage.questionText()).getText()).to.contain("Thinking about Andrew Austin, Daniel Davis is their");
      });

      it("When I click previous, Then I will go back to the 'related to anyone else' question", async () => {
        await $(RelationshipsPage.previous()).click();
        await expect(await $(RelatedToAnyoneElsePage.questionText()).getText()).to.contain("Are any of these people related to you?");
        await expect(await $(RelatedToAnyoneElsePage.yes()).isSelected()).to.be.true;
      });

      it("When I select 'No' to the 'related to anyone else' question, Then I will be taken to the first relationship for the second person", async () => {
        await $(RelatedToAnyoneElsePage.noNoneOfThesePeopleAreRelatedToMe()).click();
        await $(RelatedToAnyoneElsePage.submit()).click();
        await expect(await $(RelationshipsPage.questionText()).getText()).to.contain("Thinking about Betty Burns, Carla Clark is their");
      });

      it("When I click previous, Then I will go back to the 'related to anyone else' question for the first person", async () => {
        await $(RelationshipsPage.previous()).click();
        await expect(await $(RelatedToAnyoneElsePage.questionText()).getText()).to.contain("Are any of these people related to you?");
        await expect(await $(RelatedToAnyoneElsePage.listLabel(1)).getText()).to.equal("Daniel Davis");
        await expect(await $(RelatedToAnyoneElsePage.listLabel(2)).getText()).to.equal("Eve Elliot");
        await expect(await $(RelatedToAnyoneElsePage.noNoneOfThesePeopleAreRelatedToMe()).isSelected()).to.be.true;
      });

      it("When I click complete the remaining relationships, Then I will go to the relationships section complete page", async () => {
        await $(RelatedToAnyoneElsePage.submit()).click();
        await $(RelationshipsPage.unrelated()).click();
        await $(RelationshipsPage.submit()).click();
        await $(RelationshipsPage.unrelated()).click();
        await $(RelationshipsPage.submit()).click();
        await $(RelationshipsPage.unrelated()).click();
        await $(RelationshipsPage.submit()).click();
        await $(RelationshipsPage.unrelated()).click();
        await $(RelationshipsPage.submit()).click();
        await $(RelationshipsPage.unrelated()).click();
        await $(RelationshipsPage.submit()).click();
        await $(RelationshipsPage.unrelated()).click();
        await $(RelationshipsPage.submit()).click();
        await expect(await browser.getUrl()).to.contain(RelationshipsInterstitialPage.pageName);
      });
    });

    async function addPerson(firstName, lastName) {
      await $(ListCollectorPage.yes()).click();
      await $(ListCollectorPage.submit()).scrollIntoView();
      await $(ListCollectorPage.submit()).click();
      await $(ListCollectorAddPage.firstName()).setValue(firstName);
      await $(ListCollectorAddPage.lastName()).setValue(lastName);
      await $(ListCollectorAddPage.submit()).click();
    }
  });
});
