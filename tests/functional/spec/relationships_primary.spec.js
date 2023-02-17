import PrimaryPersonListCollectorPage from "../generated_pages/relationships_primary/primary-person-list-collector.page.js";
import PrimaryPersonListCollectorAddPage from "../generated_pages/relationships_primary/primary-person-list-collector-add.page.js";
import ListCollectorPage from "../generated_pages/relationships_primary/list-collector.page.js";
import ListCollectorAddPage from "../generated_pages/relationships_primary/list-collector-add.page.js";
import RelationshipsPage from "../generated_pages/relationships_primary/relationships.page.js";

describe("Relationships - Primary Person", () => {
  const schema = "test_relationships_primary.json";

  describe("Given I am completing the test_relationships_primary survey", () => {
    beforeEach(async () => {
      await browser.openQuestionnaire(schema);
    });

    it("When I add household members, Then I will be asked my relationships as a primary person", async () => {
      addPrimaryAndTwoOthers();

      await $(ListCollectorPage.no()).click();
      await $(ListCollectorPage.submit()).click();
      await expect(await $(RelationshipsPage.questionText()).getText()).to.contain("is your");
    });

    it("When I add household members, Then non-primary relationships will be asked as a non primary person", async () => {
      addPrimaryAndTwoOthers();

      await $(ListCollectorPage.no()).click();
      await $(ListCollectorPage.submit()).click();
      await $(RelationshipsPage.relationshipBrotherOrSister()).click();
      await $(RelationshipsPage.submit()).click();
      await $(RelationshipsPage.relationshipSonOrDaughter()).click();
      await $(RelationshipsPage.submit()).click();
      await expect(await $(RelationshipsPage.questionText()).getText()).to.contain("is their");
    });

    it("When I add household members And add thir relationships And remove the primary person And add a new primary person then I will be asked for the relationships again", async () => {
      addPrimaryAndTwoOthersAndCompleteRelationships();

      browser.url("/questionnaire/primary-person-list-collector");

      await $(PrimaryPersonListCollectorPage.no()).click();
      await $(PrimaryPersonListCollectorPage.submit()).click();

      browser.url("/questionnaire/primary-person-list-collector");

      await $(PrimaryPersonListCollectorPage.yes()).click();
      await $(PrimaryPersonListCollectorPage.submit()).click();
      await $(PrimaryPersonListCollectorAddPage.firstName()).setValue("Marcus");
      await $(PrimaryPersonListCollectorAddPage.lastName()).setValue("Twin");
      await $(PrimaryPersonListCollectorAddPage.submit()).click();
      await $(ListCollectorPage.no()).click();
      await $(ListCollectorPage.submit()).click();

      await expect(await $(RelationshipsPage.questionText()).getText()).to.contain("Samuel Clemens is your");
    });

    async function addPrimaryAndTwoOthersAndCompleteRelationships() {
      addPrimaryAndTwoOthers();

      await $(ListCollectorPage.no()).click();
      await $(ListCollectorPage.submit()).click();
      await $(RelationshipsPage.relationshipBrotherOrSister()).click();
      await $(RelationshipsPage.submit()).click();
      await $(RelationshipsPage.relationshipSonOrDaughter()).click();
      await $(RelationshipsPage.submit()).click();
      await $(RelationshipsPage.relationshipBrotherOrSister()).click();
    }

    async function addPrimaryAndTwoOthers() {
      await $(PrimaryPersonListCollectorPage.yes()).click();
      await $(PrimaryPersonListCollectorPage.submit()).click();
      await $(PrimaryPersonListCollectorAddPage.firstName()).setValue("Marcus");
      await $(PrimaryPersonListCollectorAddPage.lastName()).setValue("Twin");
      await $(PrimaryPersonListCollectorAddPage.submit()).click();
      await $(ListCollectorPage.yes()).click();
      await $(ListCollectorPage.submit()).click();
      await $(ListCollectorAddPage.firstName()).setValue("Samuel");
      await $(ListCollectorAddPage.lastName()).setValue("Clemens");
      await $(ListCollectorAddPage.submit()).click();
      await $(ListCollectorPage.yes()).click();
      await $(ListCollectorPage.submit()).click();
      await $(ListCollectorAddPage.firstName()).setValue("Olivia");
      await $(ListCollectorAddPage.lastName()).setValue("Clemens");
      await $(ListCollectorAddPage.submit()).click();
    }
  });
});
