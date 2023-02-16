import HouseholdSummary from "../../../generated_pages/hub_and_spoke_custom_content/household-section-summary.page.js";
import HowManyPeopleLiveHere from "../../../generated_pages/hub_and_spoke_custom_content/how-many-people-live-here.page.js";
import DoesAnyoneLiveHere from "../../../generated_pages/hub_and_spoke_custom_content/does-anyone-live-here.page.js";
import HubPage from "../../../base_pages/hub.page.js";

describe("Feature: Hub and Spoke with custom content", () => {
  const hubAndSpokeSchema = "test_hub_and_spoke_custom_content.json";

  it("When the questionnaire is incomplete, then custom content should be displayed correctly", async ()=> {
    await browser.openQuestionnaire(hubAndSpokeSchema);
    await expect(await $(await HubPage.heading()).getText()).to.contain("Choose another section to complete");
    await expect(await $(await HubPage.guidance()).isExisting()).to.be.false;
    await expect(await $(await HubPage.submit()).getText()).to.contain("Continue");
    await expect(await $(await HubPage.warning()).isExisting()).to.be.false;
  });

  it("When the questionnaire is complete, then custom content should be displayed correctly", async ()=> {
    await browser.openQuestionnaire(hubAndSpokeSchema);
    await $(await HubPage.summaryRowLink("household-section")).click();
    await $(await DoesAnyoneLiveHere.yes()).click();
    await $(await DoesAnyoneLiveHere.submit()).click();
    await $(await HowManyPeopleLiveHere.answer1()).click();
    await $(await HowManyPeopleLiveHere.submit()).click();
    await $(await HouseholdSummary.submit()).click();
    await expect(await $(await HubPage.heading()).getText()).to.contain("Submission title");
    await expect(await $(await HubPage.guidance()).getText()).to.contain("Submission guidance");
    await expect(await $(await HubPage.submit()).getText()).to.contain("Submission button");
    await expect(await $(await HubPage.warning()).getText()).to.contain("Submission warning");
  });
});
