import PrimaryPersonListCollectorPage from "../../generated_pages/relationships_primary/primary-person-list-collector.page.js";
import PrimaryPersonListCollectorAddPage from "../../generated_pages/relationships_primary/primary-person-list-collector-add.page.js";
import ListCollectorPage from "../../generated_pages/relationships_primary/list-collector.page.js";
import ListCollectorAddPage from "../../generated_pages/relationships_primary/list-collector-add.page.js";
import RelationshipsPage from "../../generated_pages/relationships_primary/relationships.page.js";
import { click } from "../../helpers";

describe("Relationships - Primary Person", () => {
  const schema = "test_relationships_primary.json";

  describe("Given I am completing the test_relationships_primary survey", () => {
    beforeEach(async () => {
      await browser.openQuestionnaire(schema);
    });

    it("When I add household members, Then I will be asked my relationships as a primary person", async () => {
      await addPrimaryAndTwoOthers();

      await $(ListCollectorPage.no()).click();
      await click(ListCollectorPage.submit());
      await expect(await $(RelationshipsPage.questionText()).getText()).toContain("is your");
    });

    it("When I add household members, Then non-primary relationships will be asked as a non primary person", async () => {
      await addPrimaryAndTwoOthers();

      await $(ListCollectorPage.no()).click();
      await click(ListCollectorPage.submit());
      await $(RelationshipsPage.relationshipBrotherOrSister()).click();
      await click(RelationshipsPage.submit());
      await $(RelationshipsPage.relationshipSonOrDaughter()).click();
      await click(RelationshipsPage.submit());
      await expect(await $(RelationshipsPage.questionText()).getText()).toContain("is their");
    });

    it("When I add household members And add their relationships And remove the primary person And add a new primary person then I will be asked for the relationships again", async () => {
      await addPrimaryAndTwoOthersAndCompleteRelationships();

      await browser.url("/questionnaire/primary-person-list-collector");

      await $(PrimaryPersonListCollectorPage.no()).click();
      await click(PrimaryPersonListCollectorPage.submit());

      await browser.url("/questionnaire/primary-person-list-collector");

      await $(PrimaryPersonListCollectorPage.yes()).click();
      await click(PrimaryPersonListCollectorPage.submit());
      await $(PrimaryPersonListCollectorAddPage.firstName()).setValue("Marcus");
      await $(PrimaryPersonListCollectorAddPage.lastName()).setValue("Twin");
      await click(PrimaryPersonListCollectorAddPage.submit());
      await $(ListCollectorPage.no()).click();
      await click(ListCollectorPage.submit());

      await expect(await $(RelationshipsPage.questionText()).getText()).toContain("Samuel Clemens is your");
    });

    async function addPrimaryAndTwoOthersAndCompleteRelationships() {
      await addPrimaryAndTwoOthers();

      await $(ListCollectorPage.no()).click();
      await $(ListCollectorPage.submit()).scrollIntoView();
      await click(ListCollectorPage.submit());
      await $(RelationshipsPage.relationshipBrotherOrSister()).click();
      await click(RelationshipsPage.submit());
      await $(RelationshipsPage.relationshipSonOrDaughter()).click();
      await click(RelationshipsPage.submit());
      await $(RelationshipsPage.relationshipBrotherOrSister()).click();
    }

    async function addPrimaryAndTwoOthers() {
      await $(PrimaryPersonListCollectorPage.yes()).click();
      await $(PrimaryPersonListCollectorPage.submit()).scrollIntoView();
      await click(PrimaryPersonListCollectorPage.submit());
      await $(PrimaryPersonListCollectorAddPage.firstName()).setValue("Marcus");
      await $(PrimaryPersonListCollectorAddPage.lastName()).setValue("Twin");
      await click(PrimaryPersonListCollectorAddPage.submit());
      await $(ListCollectorPage.yes()).click();
      await click(ListCollectorPage.submit());
      await $(ListCollectorAddPage.firstName()).setValue("Samuel");
      await $(ListCollectorAddPage.lastName()).setValue("Clemens");
      await click(ListCollectorAddPage.submit());
      await $(ListCollectorPage.yes()).click();
      await click(ListCollectorPage.submit());
      await $(ListCollectorAddPage.firstName()).setValue("Olivia");
      await $(ListCollectorAddPage.lastName()).setValue("Clemens");
      await click(ListCollectorAddPage.submit());
    }
  });
});
