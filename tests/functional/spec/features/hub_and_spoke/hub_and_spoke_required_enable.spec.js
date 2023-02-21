import HouseholdRelationshipsBlockPage from "../../../generated_pages/hub_section_required_and_enabled/household-relationships-block.page";
import RelationshipsCountPage from "../../../generated_pages/hub_section_required_and_enabled/relationships-count.page";
import { SubmitPage } from "../../../base_pages/submit.page";

describe("Hub and spoke section required and enabled", () => {
  beforeEach("Load the survey", async () => {
    await browser.openQuestionnaire("test_hub_section_required_and_enabled.json");
  });
  it("Given a relationship question in household, When I answer 'Yes', meaning the second section is enabled, Then I am routed to second section", async () => {
    await $(HouseholdRelationshipsBlockPage.yes()).click();
    await $(HouseholdRelationshipsBlockPage.submit()).click();
    await expect(await $(RelationshipsCountPage.legend()).getText()).to.contain("How many people are related");
  });
  it("Given a relationship question in household, When I answer 'No', Then I am redirected to the hub and can submit my answers without completing the other section", async () => {
    await $(HouseholdRelationshipsBlockPage.no()).click();
    await $(HouseholdRelationshipsBlockPage.submit()).click();
    await expect(await $("body").getText()).to.contain("Submit survey");
    await $(SubmitPage.submit()).click();
    await expect(await browser.getUrl()).to.contain("thank-you");
  });
});
