import { getRandomString } from "../../../jwt_helper";
import ALevelsPage from "../../../generated_pages/last_viewed_question_guidance_hub/a-levels.page.js";
import EducationSectionSummaryPage from "../../../generated_pages/last_viewed_question_guidance_hub/education-section-summary.page.js";
import GcsesPage from "../../../generated_pages/last_viewed_question_guidance_hub/gcses.page.js";
import HobbiesPage from "../../../generated_pages/last_viewed_question_guidance_hub/hobbies.page.js";
import PaidWorkPage from "../../../generated_pages/last_viewed_question_guidance_hub/paid-work.page.js";
import SportsPage from "../../../generated_pages/last_viewed_question_guidance_hub/sports.page.js";
import UnPaidWorkPage from "../../../generated_pages/last_viewed_question_guidance_hub/unpaid-work.page.js";
import WorkInterstitialPage from "../../../generated_pages/last_viewed_question_guidance_hub/work-interstitial.page.js";
import HubPage from "../../../base_pages/hub.page.js";
import { click, verifyUrlContains } from "../../../helpers";
describe("Last viewed question guidance", () => {
  const resumableLaunchParams = {
    responseId: getRandomString(16),
    userId: "test_user",
  };

  describe("Given the hub has a required section, which has not been completed", () => {
    before("Open survey", async () => {
      await browser.openQuestionnaire("test_last_viewed_question_guidance_hub.json", resumableLaunchParams);
    });

    it("When the respondent launches the survey, then last question guidance is not shown", async () => {
      await verifyUrlContains(WorkInterstitialPage.url());
      await expect(await $(WorkInterstitialPage.lastViewedQuestionGuidance()).isExisting()).toBe(false);
    });

    it("When the respondent saves and resumes from a section which is not started, then last question guidance is not shown", async () => {
      await $(WorkInterstitialPage.saveSignOut()).click();
      await browser.openQuestionnaire("test_last_viewed_question_guidance_hub.json", resumableLaunchParams);
      await browser.pause(100);
      await verifyUrlContains(WorkInterstitialPage.url());
      await expect(await $(WorkInterstitialPage.lastViewedQuestionGuidance()).isExisting()).toBe(false);
    });

    it("When the respondent saves and resumes from a section which is in progress, then last question guidance is shown", async () => {
      await click(WorkInterstitialPage.submit());
      await $(PaidWorkPage.saveSignOut()).click();
      await browser.openQuestionnaire("test_last_viewed_question_guidance_hub.json", resumableLaunchParams);
      await expect(await $(PaidWorkPage.lastViewedQuestionGuidanceLink()).getAttribute("href")).toContain(WorkInterstitialPage.url());
      await expect(await $(PaidWorkPage.lastViewedQuestionGuidance()).isExisting()).toBe(true);
    });
  });

  describe("Given the respondent has completed the required section and is on the hub", () => {
    before("Open survey and complete first section", async () => {
      await browser.openQuestionnaire("test_last_viewed_question_guidance_hub.json");
      await click(WorkInterstitialPage.submit());
      await $(PaidWorkPage.yes()).click();
      await click(PaidWorkPage.submit());
      await $(UnPaidWorkPage.yes()).click();
      await click(UnPaidWorkPage.submit());
    });

    it("When the respondent selects a section which is not started, then last question guidance is not shown", async () => {
      await $(HubPage.summaryRowLink("education-section")).click();
      await verifyUrlContains(GcsesPage.url());
      await expect(await $(GcsesPage.lastViewedQuestionGuidance()).isExisting()).toBe(false);
    });

    it("When the respondent selects a section which is in progress, then last question guidance is shown", async () => {
      await click(HubPage.submit());
      await $(GcsesPage.yes()).click();
      await click(GcsesPage.submit());
      await browser.url(HubPage.url());
      await $(HubPage.summaryRowLink("education-section")).click();
      await verifyUrlContains(ALevelsPage.url());
      await expect(await $(ALevelsPage.lastViewedQuestionGuidanceLink()).getAttribute("href")).toContain(GcsesPage.url());
      await expect(await $(ALevelsPage.lastViewedQuestionGuidance()).isExisting()).toBe(true);
    });

    it("When the respondent selects a section which is complete , then last question guidance is not shown on the summary or any link clicked from the summary", async () => {
      await $(ALevelsPage.yes()).click();
      await click(ALevelsPage.submit());
      await verifyUrlContains(EducationSectionSummaryPage.url());
      await expect(await $(ALevelsPage.lastViewedQuestionGuidance()).isExisting()).toBe(false);
      await click(EducationSectionSummaryPage.submit());
      await $(HubPage.summaryRowLink("education-section")).click();
      await verifyUrlContains(EducationSectionSummaryPage.url());
      await $(EducationSectionSummaryPage.alevelsAnswerEdit()).click();
      await expect(await $(ALevelsPage.lastViewedQuestionGuidance()).isExisting()).toBe(false);
    });

    it("When the user clicks continue on the hub and it takes you to a section which is not started, then last question guidance is not shown", async () => {
      await browser.url(HubPage.url());
      await click(HubPage.submit());
      await verifyUrlContains(SportsPage.url());
      await expect(await $(SportsPage.lastViewedQuestionGuidance()).isExisting()).toBe(false);
    });

    it("When the user clicks continue on the hub and it takes you to a section which is in progress, then last question guidance is shown", async () => {
      await click(HubPage.submit());
      await $(SportsPage.yes()).click();
      await click(SportsPage.submit());
      await browser.url(HubPage.url());
      await click(HubPage.submit());
      await verifyUrlContains(HobbiesPage.url());
      await expect(await $(HobbiesPage.lastViewedQuestionGuidanceLink()).getAttribute("href")).toContain(SportsPage.url());
      await expect(await $(HobbiesPage.lastViewedQuestionGuidance()).isExisting()).toBe(true);
    });

    it("When the user clicks continue on the hub and it takes you to a section which is complete but doesnt have a summary, then last question guidance is not shown", async () => {
      await $(HobbiesPage.yes()).click();
      await click(HobbiesPage.submit());
      await $(HubPage.summaryRowLink("interests-section")).click();
      await verifyUrlContains(SportsPage.url());
      await expect(await $(SportsPage.lastViewedQuestionGuidance()).isExisting()).toBe(false);
    });
  });
});
