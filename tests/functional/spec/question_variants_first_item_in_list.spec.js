import ListCollectorPage from "../generated_pages/variants_first_item_in_list/list-collector.page.js";
import ListCollectorAddPage from "../generated_pages/variants_first_item_in_list/list-collector-add.page.js";
import ListStatusQuestion from "../generated_pages/variants_first_item_in_list/list-status.page.js";
import HubPage from "../base_pages/hub.page.js";

describe("Question Variants First Item in List", () => {
  it("Given I am the first person on the list, When the when rule is set, Then I should the correct question variant", () => {
    browser.openQuestionnaire("test_new_variants_first_item_in_list.json");
    $(HubPage.submit()).click();
    $(ListCollectorPage.yes()).click();
    $(ListCollectorPage.submit()).click();
    $(ListCollectorAddPage.firstName()).setValue("Marcus");
    $(ListCollectorAddPage.lastName()).setValue("Twin");
    $(ListCollectorAddPage.submit()).click();
    $(ListCollectorPage.no()).click();
    $(ListCollectorPage.submit()).click();
    $(HubPage.submit()).click();
    expect($(ListStatusQuestion.questionText()).getText()).to.contain("You are the first person in the list");
  });

  it("Given I am the second person on the list, When the when rule is set, Then I should the correct question variant", () => {
    browser.openQuestionnaire("test_new_variants_first_item_in_list.json");
    $(HubPage.submit()).click();
    $(ListCollectorPage.yes()).click();
    $(ListCollectorPage.submit()).click();
    $(ListCollectorAddPage.firstName()).setValue("Marcus");
    $(ListCollectorAddPage.lastName()).setValue("Twin");
    $(ListCollectorAddPage.submit()).click();
    $(ListCollectorPage.yes()).click();
    $(ListCollectorPage.submit()).click();
    $(ListCollectorAddPage.firstName()).setValue("John");
    $(ListCollectorAddPage.lastName()).setValue("Doe");
    $(ListCollectorAddPage.submit()).click();
    $(ListCollectorPage.no()).click();
    $(ListCollectorPage.submit()).click();
    $(HubPage.summaryRowLink("personal-details-section-2")).click();
    expect($(ListStatusQuestion.questionText()).getText()).to.contain("You are not the first person in the list");
  });
});
