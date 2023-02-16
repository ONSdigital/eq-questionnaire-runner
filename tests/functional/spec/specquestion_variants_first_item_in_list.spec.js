import ListCollectorPage from "../generated_pages/variants_first_item_in_list/list-collector.page.js";
import ListCollectorAddPage from "../generated_pages/variants_first_item_in_list/list-collector-add.page.js";
import ListStatusQuestion from "../generated_pages/variants_first_item_in_list/list-status.page.js";
import HubPage from "../base_pages/hub.page.js";

describe("Question Variants First Item in List", () => {
  it("Given I am the first person on the list, When the when rule is set, Then I should the correct question variant", async ()=> {
    await browser.openQuestionnaire("test_new_variants_first_item_in_list.json");
    await $(await HubPage.submit()).click();
    await $(await ListCollectorPage.yes()).click();
    await $(await ListCollectorPage.submit()).click();
    await $(await ListCollectorAddPage.firstName()).setValue("Marcus");
    await $(await ListCollectorAddPage.lastName()).setValue("Twin");
    await $(await ListCollectorAddPage.submit()).click();
    await $(await ListCollectorPage.no()).click();
    await $(await ListCollectorPage.submit()).click();
    await $(await HubPage.submit()).click();
    await expect(await $(await ListStatusQuestion.questionText()).getText()).to.contain("You are the first person in the list");
  });

  it("Given I am the second person on the list, When the when rule is set, Then I should the correct question variant", async ()=> {
    await browser.openQuestionnaire("test_new_variants_first_item_in_list.json");
    await $(await HubPage.submit()).click();
    await $(await ListCollectorPage.yes()).click();
    await $(await ListCollectorPage.submit()).click();
    await $(await ListCollectorAddPage.firstName()).setValue("Marcus");
    await $(await ListCollectorAddPage.lastName()).setValue("Twin");
    await $(await ListCollectorAddPage.submit()).click();
    await $(await ListCollectorPage.yes()).click();
    await $(await ListCollectorPage.submit()).click();
    await $(await ListCollectorAddPage.firstName()).setValue("John");
    await $(await ListCollectorAddPage.lastName()).setValue("Doe");
    await $(await ListCollectorAddPage.submit()).click();
    await $(await ListCollectorPage.no()).click();
    await $(await ListCollectorPage.submit()).click();
    await $(await HubPage.summaryRowLink("personal-details-section-2")).click();
    await expect(await $(await ListStatusQuestion.questionText()).getText()).to.contain("You are not the first person in the list");
  });
});
