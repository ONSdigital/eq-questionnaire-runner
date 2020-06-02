const HouseholdSummary = require("../../../generated_pages/hub_and_spoke_custom_content/household-section-summary.page.js");
const HowManyPeopleLiveHere = require("../../../generated_pages/hub_and_spoke_custom_content/how-many-people-live-here.page.js");
const DoesAnyoneLiveHere = require("../../../generated_pages/hub_and_spoke_custom_content/does-anyone-live-here.page.js");

const HubPage = require("../../../base_pages/hub.page.js");

describe("Feature: Hub and Spoke with custom content", () => {
  const hubAndSpokeSchema = "test_hub_and_spoke_custom_content.json";

  it("When the questionnaire is incomplete, then custom content should be displayed correctly", () => {
    browser.openQuestionnaire(hubAndSpokeSchema);
    expect($(HubPage.displayedName()).getText()).to.contain("Choose another section to complete");
    expect($(HubPage.displayedGuidance()).getText()).to.contain("Guidance displayed on hub when incomplete");
    expect($(HubPage.submit()).getText()).to.contain("Continue");
  });

  it("When the questionnaire is complete, then custom content should be displayed correctly", () => {
    browser.openQuestionnaire(hubAndSpokeSchema);
    $(HubPage.summaryRowLink(1)).click();
    $(DoesAnyoneLiveHere.yes()).click();
    $(DoesAnyoneLiveHere.submit()).click();
    $(HowManyPeopleLiveHere.answer1()).click();
    $(HowManyPeopleLiveHere.submit()).click();
    $(HouseholdSummary.submit()).click();
    expect($(HubPage.displayedName()).getText()).to.contain("Title displayed on hub when complete");
    expect($(HubPage.displayedGuidance()).getText()).to.contain("Guidance displayed on hub when complete");
    expect($(HubPage.submit()).getText()).to.contain("Submission text");
  });
});
