import HouseholdSummary from "../../../generated_pages/hub_and_spoke_custom_content/household-section-summary.page.js";
import HowManyPeopleLiveHere from "../../../generated_pages/hub_and_spoke_custom_content/how-many-people-live-here.page.js";
import DoesAnyoneLiveHere from "../../../generated_pages/hub_and_spoke_custom_content/does-anyone-live-here.page.js";
import HubPage from "../../../base_pages/hub.page.js";
import { click } from "../../../helpers";
describe("Feature: Hub and Spoke with custom content", () => {
  const hubAndSpokeSchema = "test_hub_and_spoke_custom_content.json";

  it("When the questionnaire is incomplete, then custom content should be displayed correctly", async () => {
    await browser.openQuestionnaire(hubAndSpokeSchema);
    await expect(await $(HubPage.heading()).getText()).toBe("Choose another section to complete");
    await expect(await $(HubPage.guidance()).isExisting()).toBe(false);
    await expect(await $(HubPage.summaryRowLink("household-section")).getHTML()).toContain("Start section: Household residents");
    await expect(await $(HubPage.submit()).getText()).toBe("Continue");
    await expect(await $(HubPage.warning()).isExisting()).toBe(false);
  });

  it("When the questionnaire is complete, then custom content should be displayed correctly", async () => {
    await browser.openQuestionnaire(hubAndSpokeSchema);
    await $(HubPage.summaryRowLink("household-section")).click();
    await $(DoesAnyoneLiveHere.yes()).click();
    await click(DoesAnyoneLiveHere.submit());
    await $(HowManyPeopleLiveHere.answer1()).click();
    await click(HowManyPeopleLiveHere.submit());
    await click(HouseholdSummary.submit());
    await expect(await $(HubPage.summaryRowLink("household-section")).getHTML()).toContain("View answers: Household residents");
    await expect(await $(HubPage.heading()).getText()).toBe("Submission title");
    await expect(await $(HubPage.guidance()).getText()).toBe("Submission guidance");
    await expect(await $(HubPage.submit()).getText()).toBe("Submission button");
    await expect(await $(HubPage.warning()).getText()).toBe("Submission warning");
  });
});
