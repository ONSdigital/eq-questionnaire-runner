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
      await expect(await browser.getUrl()).to.contain(WorkInterstitialPage.url());
      await expect(await $(WorkInterstitialPage.lastViewedQuestionGuidance()).isExisting()).to.be.false;
    });

    it("When the respondent saves and resumes from a section which is not started, then last question guidance is not shown", async () => {
      await $(WorkInterstitialPage.saveSignOut()).click();
      await browser.openQuestionnaire("test_last_viewed_question_guidance_hub.json", resumableLaunchParams);
      await browser.pause(100);
      await expect(await browser.getUrl()).to.contain(WorkInterstitialPage.url());
      await expect(await $(WorkInterstitialPage.lastViewedQuestionGuidance()).isExisting()).to.be.false;
    });

    it("When the respondent saves and resumes from a section which is in progress, then last question guidance is shown", async () => {
      await $(WorkInterstitialPage.submit()).click();
      await $(PaidWorkPage.saveSignOut()).click();
      await browser.openQuestionnaire("test_last_viewed_question_guidance_hub.json", resumableLaunchParams);
      await expect(await $(PaidWorkPage.lastViewedQuestionGuidanceLink()).getAttribute("href")).to.contain(WorkInterstitialPage.url());
      await expect(await $(PaidWorkPage.lastViewedQuestionGuidance()).isExisting()).to.be.true;
    });
  });

  describe("Given the respondent has completed the required section and is on the hub", () => {
    before("Open survey and complete first section", async () => {
      await browser.openQuestionnaire("test_last_viewed_question_guidance_hub.json");
      await $(WorkInterstitialPage.submit()).click();
      await $(PaidWorkPage.yes()).click();
      await $(PaidWorkPage.submit()).click();
      await $(UnPaidWorkPage.yes()).click();
      await $(UnPaidWorkPage.submit()).click();
    });

    it("When the respondent selects a section which is not started, then last question guidance is not shown", async () => {
      await $(HubPage.summaryRowLink("education-section")).click();
      await expect(await browser.getUrl()).to.contain(GcsesPage.url());
      await expect(await $(GcsesPage.lastViewedQuestionGuidance()).isExisting()).to.be.false;
    });

    it("When the respondent selects a section which is in progress, then last question guidance is shown", async () => {
      await $(HubPage.submit()).click();
      await $(GcsesPage.yes()).click();
      await $(GcsesPage.submit()).click();
      await browser.url(HubPage.url());
      await $(HubPage.summaryRowLink("education-section")).click();
      await expect(await browser.getUrl()).to.contain(ALevelsPage.url());
      await expect(await $(ALevelsPage.lastViewedQuestionGuidanceLink()).getAttribute("href")).to.contain(GcsesPage.url());
      await expect(await $(ALevelsPage.lastViewedQuestionGuidance()).isExisting()).to.be.true;
    });

    it("When the respondent selects a section which is complete , then last question guidance is not shown on the summary or any link clicked from the summary", async () => {
      await $(ALevelsPage.yes()).click();
      await $(ALevelsPage.submit()).click();
      await expect(await browser.getUrl()).to.contain(EducationSectionSummaryPage.url());
      await expect(await $(ALevelsPage.lastViewedQuestionGuidance()).isExisting()).to.be.false;
      await $(EducationSectionSummaryPage.submit()).click();
      await $(HubPage.summaryRowLink("education-section")).click();
      await expect(await browser.getUrl()).to.contain(EducationSectionSummaryPage.url());
      await $(EducationSectionSummaryPage.alevelsAnswerEdit()).click();
      await expect(await $(ALevelsPage.lastViewedQuestionGuidance()).isExisting()).to.be.false;
    });

    it("When the user clicks continue on the hub and it takes you to a section which is not started, then last question guidance is not shown", async () => {
      await browser.url(HubPage.url());
      await $(HubPage.submit()).click();
      await expect(await browser.getUrl()).to.contain(SportsPage.url());
      await expect(await $(SportsPage.lastViewedQuestionGuidance()).isExisting()).to.be.false;
    });

    it("When the user clicks continue on the hub and it takes you to a section which is in progress, then last question guidance is shown", async () => {
      await $(HubPage.submit()).click();
      await $(SportsPage.yes()).click();
      await $(SportsPage.submit()).click();
      await browser.url(HubPage.url());
      await $(HubPage.submit()).click();
      await expect(await browser.getUrl()).to.contain(HobbiesPage.url());
      await expect(await $(HobbiesPage.lastViewedQuestionGuidanceLink()).getAttribute("href")).to.contain(SportsPage.url());
      await expect(await $(HobbiesPage.lastViewedQuestionGuidance()).isExisting()).to.be.true;
    });

    it("When the user clicks continue on the hub and it takes you to a section which is complete but doesnt have a summary, then last question guidance is not shown", async () => {
      await $(HobbiesPage.yes()).click();
      await $(HobbiesPage.submit()).click();
      await $(HubPage.summaryRowLink("interests-section")).click();
      await expect(await browser.getUrl()).to.contain(SportsPage.url());
      await expect(await $(SportsPage.lastViewedQuestionGuidance()).isExisting()).to.be.false;
    });
  });
});
