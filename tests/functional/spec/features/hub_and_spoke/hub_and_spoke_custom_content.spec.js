import HouseholdSummary from "../../../generated_pages/hub_and_spoke_custom_content/household-section-summary.page.js";
import HowManyPeopleLiveHere from "../../../generated_pages/hub_and_spoke_custom_content/how-many-people-live-here.page.js";
import DoesAnyoneLiveHere from "../../../generated_pages/hub_and_spoke_custom_content/does-anyone-live-here.page.js";
import HubPage from "../../../base_pages/hub.page.js";
import { click } from "../../../helpers";
describe("Feature: Hub and Spoke with custom content", () => {
  const hubAndSpokeSchema = "test_hub_and_spoke_custom_content.json";

  it("When the questionnaire is incomplete, then custom content should be displayed correctly", async () => {
    await browser.openQuestionnaire(hubAndSpokeSchema);
    await expect(await $(HubPage.heading()).getText()).to.contain("Choose another section to complete");
    await expect(await $(HubPage.guidance()).isExisting()).to.be.false;
    await expect(await $(HubPage.submit()).getText()).to.contain("Continue");
    await expect(await $(HubPage.warning()).isExisting()).to.be.false;
  });

  it("When the questionnaire is complete, then custom content should be displayed correctly", async () => {
    await browser.openQuestionnaire(hubAndSpokeSchema);
    await $(HubPage.summaryRowLink("household-section")).click();
    await $(DoesAnyoneLiveHere.yes()).click();
    await click(DoesAnyoneLiveHere.submit());
    await $(HowManyPeopleLiveHere.answer1()).click();
    await click(HowManyPeopleLiveHere.submit());
    await click(HouseholdSummary.submit());
    await expect(await $(HubPage.heading()).getText()).to.contain("Submission title");
    await expect(await $(HubPage.guidance()).getText()).to.contain("Submission guidance");
    await expect(await $(HubPage.submit()).getText()).to.contain("Submission button");
    await expect(await $(HubPage.warning()).getText()).to.contain("Submission warning");
  });
});
