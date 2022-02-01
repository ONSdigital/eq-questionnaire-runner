import HouseholdRelationshipsBlockPage from "../../../generated_pages/hub_section_required_and_enabled/household-relationships-block.page";
import RelationshipsCountPage from "../../../generated_pages/hub_section_required_and_enabled/relationships-count.page";

describe("Hub and spoke section required and enabled", () => {
  beforeEach("Load the survey", () => {
    browser.openQuestionnaire("test_hub_section_required_and_enabled.json");
  });
  it(" When I answer 'Yes' to the first section, meaning the second section is enabled,Then I should be redirected to the relationship count section", () => {
    $(HouseholdRelationshipsBlockPage.yes()).click();
    $(HouseholdRelationshipsBlockPage.submit()).click();
    expect($(RelationshipsCountPage.legend()).getText()).to.contain("How many people are related");
  });
  it(" When I answer 'No' to the first section,Then I should be redirected to the hub and can submit my answers without completing the other section", () => {
    $(HouseholdRelationshipsBlockPage.no()).click();
    $(HouseholdRelationshipsBlockPage.submit()).click();
    expect($("body").getText()).to.contain("Submit survey");
  });
});
