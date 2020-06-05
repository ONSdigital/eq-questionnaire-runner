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
    before("Open survey", () => {
      browser.openQuestionnaire("test_last_viewed_question_guidance_hub.json", resumableLaunchParams);
    });

    it("When the respondent launches the survey, then last question guidance is not shown", () => {
      expect(browser.getUrl()).to.contain(WorkInterstitialPage.url());
      expect($(WorkInterstitialPage.lastViewedQuestionGuidance()).isExisting()).to.be.false;
    });

    it("When the respondent saves and resumes from a section which is not started, then last question guidance is not shown", () => {
      $(WorkInterstitialPage.saveSignOut()).click();
      browser.openQuestionnaire("test_last_viewed_question_guidance_hub.json", resumableLaunchParams);
      expect(browser.getUrl()).to.contain(WorkInterstitialPage.url());
      expect($(WorkInterstitialPage.lastViewedQuestionGuidance()).isExisting()).to.be.false;
    });

    it("When the respondent saves and resumes from a section which is in progress, then last question guidance is shown", () => {
      $(WorkInterstitialPage.submit()).click();
      $(PaidWorkPage.saveSignOut()).click();
      browser.openQuestionnaire("test_last_viewed_question_guidance_hub.json", resumableLaunchParams);
      expect($(PaidWorkPage.lastViewedQuestionGuidanceLink()).getAttribute("href")).to.contain(WorkInterstitialPage.url());
      expect($(PaidWorkPage.lastViewedQuestionGuidance()).isExisting()).to.be.true;
    });
  });

  describe("Given the respondent has completed the required section and is on the hub", () => {
    before("Open survey and complete first section", () => {
      browser.openQuestionnaire("test_last_viewed_question_guidance_hub.json");
      $(WorkInterstitialPage.submit()).click();
      $(PaidWorkPage.yes()).click();
      $(PaidWorkPage.submit()).click();
      $(UnPaidWorkPage.yes()).click();
      $(UnPaidWorkPage.submit()).click();
    });

    it("When the respondent selects a section which is not started, then last question guidance is not shown", () => {
      $(HubPage.summaryRowLink(2)).click();
      expect(browser.getUrl()).to.contain(GcsesPage.url());
      expect($(GcsesPage.lastViewedQuestionGuidance()).isExisting()).to.be.false;
    });

    it("When the respondent selects a section which is in progress, then last question guidance is shown", () => {
      $(HubPage.submit()).click();
      $(GcsesPage.yes()).click();
      $(GcsesPage.submit()).click();
      browser.url(HubPage.url());
      $(HubPage.summaryRowLink(2)).click();
      expect(browser.getUrl()).to.contain(ALevelsPage.url());
      expect($(ALevelsPage.lastViewedQuestionGuidanceLink()).getAttribute("href")).to.contain(GcsesPage.url());
      expect($(ALevelsPage.lastViewedQuestionGuidance()).isExisting()).to.be.true;
    });

    it("When the respondent selects a section which is complete , then last question guidance is not shown on the summary or any link clicked from the summary", () => {
      $(ALevelsPage.yes()).click();
      $(ALevelsPage.submit()).click();
      expect($(EducationSectionSummaryPage.lastViewedQuestionGuidance()).isExisting()).to.be.false;
      $(EducationSectionSummaryPage.submit()).click();
      $(HubPage.summaryRowLink(2)).click();
      expect(browser.getUrl()).to.contain(EducationSectionSummaryPage.url());
      $(EducationSectionSummaryPage.alevelsAnswerEdit()).click();
      expect($(ALevelsPage.lastViewedQuestionGuidance()).isExisting()).to.be.false;
    });

    it("When the user clicks continue on the hub and it takes you to a section which is not started, then last question guidance is not shown", () => {
      browser.url(HubPage.url());
      $(HubPage.submit()).click();
      expect(browser.getUrl()).to.contain(SportsPage.url());
      expect($(SportsPage.lastViewedQuestionGuidance()).isExisting()).to.be.false;
    });

    it("When the user clicks continue on the hub and it takes you to a section which is in progress, then last question guidance is shown", () => {
      $(HubPage.submit()).click();
      $(SportsPage.yes()).click();
      $(SportsPage.submit()).click();
      browser.url(HubPage.url());
      $(HubPage.submit()).click();
      expect(browser.getUrl()).to.contain(HobbiesPage.url());
      expect($(HobbiesPage.lastViewedQuestionGuidanceLink()).getAttribute("href")).to.contain(SportsPage.url());
      expect($(HobbiesPage.lastViewedQuestionGuidance()).isExisting()).to.be.true;
    });

    it("When the user clicks continue on the hub and it takes you to a section which is complete but doesnt have a summary, then last question guidance is not shown", () => {
      $(HobbiesPage.yes()).click();
      $(HobbiesPage.submit()).click();
      $(HubPage.summaryRowLink(3)).click();
      expect(browser.getUrl()).to.contain(SportsPage.url());
      expect($(SportsPage.lastViewedQuestionGuidance()).isExisting()).to.be.false;
    });
  });
});
