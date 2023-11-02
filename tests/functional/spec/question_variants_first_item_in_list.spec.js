import ListCollectorPage from "../generated_pages/variants_first_item_in_list/list-collector.page.js";
import ListCollectorAddPage from "../generated_pages/variants_first_item_in_list/list-collector-add.page.js";
import ListStatusQuestion from "../generated_pages/variants_first_item_in_list/list-status.page.js";
import HubPage from "../base_pages/hub.page.js";
import { click } from "../helpers";

describe("Question Variants First Item in List", () => {
  it("Given I am the first person on the list, When the when rule is set, Then I should the correct question variant", async () => {
    await browser.openQuestionnaire("test_variants_first_item_in_list.json");
    await click(HubPage.submit());
    await $(ListCollectorPage.yes()).click();
    await click(ListCollectorPage.submit());
    await $(ListCollectorAddPage.firstName()).setValue("Marcus");
    await $(ListCollectorAddPage.lastName()).setValue("Twin");
    await click(ListCollectorAddPage.submit());
    await $(ListCollectorPage.no()).click();
    await click(ListCollectorPage.submit());
    await click(HubPage.submit());
    await expect(await $(ListStatusQuestion.questionText()).getText()).toBe("You are the first person in the list");
  });

  it("Given I am the second person on the list, When the when rule is set, Then I should the correct question variant", async () => {
    await browser.openQuestionnaire("test_variants_first_item_in_list.json");
    await click(HubPage.submit());
    await $(ListCollectorPage.yes()).click();
    await click(ListCollectorPage.submit());
    await $(ListCollectorAddPage.firstName()).setValue("Marcus");
    await $(ListCollectorAddPage.lastName()).setValue("Twin");
    await click(ListCollectorAddPage.submit());
    await $(ListCollectorPage.yes()).click();
    await click(ListCollectorPage.submit());
    await $(ListCollectorAddPage.firstName()).setValue("John");
    await $(ListCollectorAddPage.lastName()).setValue("Doe");
    await click(ListCollectorAddPage.submit());
    await $(ListCollectorPage.no()).click();
    await click(ListCollectorPage.submit());
    await $(HubPage.summaryRowLink("personal-details-section-2")).click();
    await expect(await $(ListStatusQuestion.questionText()).getText()).toBe("You are not the first person in the list");
  });
});
