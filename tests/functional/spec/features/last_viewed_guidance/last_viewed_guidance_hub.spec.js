const JwtHelper = require("../../../jwt_helper");

const ALevelsPage = require('../../../generated_pages/last_viewed_question_guidance_hub/a-levels.page.js');
const EducationSectionSummaryPage = require('../../../generated_pages/last_viewed_question_guidance_hub/education-section-summary.page.js');
const GcsesPage = require('../../../generated_pages/last_viewed_question_guidance_hub/gcses.page.js');
const HobbiesPage = require('../../../generated_pages/last_viewed_question_guidance_hub/hobbies.page.js');
const PaidWorkPage = require('../../../generated_pages/last_viewed_question_guidance_hub/paid-work.page.js');
const SportsPage = require('../../../generated_pages/last_viewed_question_guidance_hub/sports.page.js');
const UnPaidWorkPage = require('../../../generated_pages/last_viewed_question_guidance_hub/unpaid-work.page.js');
const WorkInterstitialPage = require('../../../generated_pages/last_viewed_question_guidance_hub/work-interstitial.page.js');

const HubPage = require('../../../base_pages/hub.page.js');

describe('Last viewed question guidance', function () {

  const last_viewed_question_text = 'This is the last viewed question in this section'
  const last_viewed_question_url_arg='last_viewed_question_guidance=True'
  const responseId = JwtHelper.getRandomString(16);

  describe('Given the hub has a required section, which has not been completed', function () {
    before('Open survey', function () {
      browser.openQuestionnaire('test_last_viewed_question_guidance_hub.json', { userId: "test_user", responseId: responseId });
    });

    it('When the respondent launches the survey, then last question guidance is not shown', function () {
      expect(browser.getUrl()).to.contain(WorkInterstitialPage.url());
      expect(browser.getUrl()).not.to.contain(last_viewed_question_url_arg);
      expect($(WorkInterstitialPage.mainContent()).getText()).not.to.contain(last_viewed_question_text);
    });

    it('When the respondent saves and resumes from a section which is not started, then last question guidance is not shown', function () {
      $(WorkInterstitialPage.saveSignOut()).click();
      browser.openQuestionnaire('test_last_viewed_question_guidance_hub.json', { userId: "test_user", responseId: responseId });
      expect(browser.getUrl()).to.contain(WorkInterstitialPage.url());
      expect(browser.getUrl()).not.to.contain(last_viewed_question_url_arg);
      expect($(WorkInterstitialPage.mainContent()).getText()).not.to.contain(last_viewed_question_text);

    });

    it('When the respondent saves and resumes from a section which is in progress, then last question guidance is shown', function () {
      $(WorkInterstitialPage.submit()).click();
      $(PaidWorkPage.saveSignOut()).click();
      browser.openQuestionnaire('test_last_viewed_question_guidance_hub.json', { userId: "test_user", responseId: responseId });
      expect(browser.getUrl()).to.contain(last_viewed_question_url_arg);
      expect($(PaidWorkPage.lastViewedQuestionGuidanceLink()).getAttribute('href')).to.contain(WorkInterstitialPage.url());
      expect($(PaidWorkPage.lastViewedQuestionGuidance()).getText()).to.contain(last_viewed_question_text);
    });
  });


  describe('Given the respondent has completed the required section and is on the hub', function () {
    before('Open survey and complete first section', function () {
      browser.openQuestionnaire('test_last_viewed_question_guidance_hub.json');
      $(WorkInterstitialPage.submit()).click();
      $(PaidWorkPage.yes()).click();
      $(PaidWorkPage.submit()).click();
      $(UnPaidWorkPage.yes()).click();
      $(UnPaidWorkPage.submit()).click();
    });

    it('When the respondent selects a section which is not started, then last question guidance is not shown', function () {
        $(HubPage.summaryRowLink(2)).click();
        expect(browser.getUrl()).to.contain(GcsesPage.url());
        expect(browser.getUrl()).to.not.contain(last_viewed_question_url_arg);
        expect($(GcsesPage.mainContent()).getText()).not.to.contain(last_viewed_question_text);
      });

    it('When the respondent selects a section which is in progress, then last question guidance is shown', function () {
        $(HubPage.submit()).click();
        $(GcsesPage.yes()).click();
        $(GcsesPage.submit()).click();
        browser.url(HubPage.url());
        $(HubPage.summaryRowLink(2)).click();
        expect(browser.getUrl()).to.contain(ALevelsPage.url());
        expect(browser.getUrl()).to.contain(last_viewed_question_url_arg);
        expect($(ALevelsPage.lastViewedQuestionGuidanceLink()).getAttribute('href')).to.contain(GcsesPage.url());
        expect($(ALevelsPage.lastViewedQuestionGuidance()).getText()).to.contain('This is the last viewed question in this section');
      });

    it('When the respondent selects a section which is complete , then last question guidance is not shown on the summary or any link clicked from the summary', function () {
        $(ALevelsPage.yes()).click();
        $(ALevelsPage.submit()).click();
        $(EducationSectionSummaryPage.submit()).click();
        $(HubPage.summaryRowLink(2)).click();
        expect(browser.getUrl()).to.contain(EducationSectionSummaryPage.url());
        expect(browser.getUrl()).not.to.contain(last_viewed_question_url_arg);
        $(EducationSectionSummaryPage.alevelsAnswerEdit()).click()
        expect(browser.getUrl()).not.to.contain(last_viewed_question_url_arg);
        expect($(ALevelsPage.mainContent()).getText()).not.to.contain(last_viewed_question_text);
    });

    it('When the user clicks continue on the hub and it takes you to a section which is not started, then last question guidance is not shown', function () {
        browser.url(HubPage.url());
        $(HubPage.submit()).click();
        expect(browser.getUrl()).to.contain(SportsPage.url());
        expect(browser.getUrl()).not.to.contain(last_viewed_question_url_arg);
        expect($(SportsPage.mainContent()).getText()).not.to.contain(last_viewed_question_text);

      });

    it('When the user clicks continue on the hub and it takes you to a section which is in progress, then last question guidance is shown', function () {
        $(HubPage.submit()).click();
        $(SportsPage.yes()).click();
        $(SportsPage.submit()).click();
        browser.url(HubPage.url());
        $(HubPage.submit()).click();
        expect(browser.getUrl()).to.contain(HobbiesPage.url());
        expect(browser.getUrl()).to.contain(last_viewed_question_url_arg);
        expect($(HobbiesPage.lastViewedQuestionGuidanceLink()).getAttribute('href')).to.contain(SportsPage.url());
        expect($(HobbiesPage.lastViewedQuestionGuidance()).getText()).to.contain(last_viewed_question_text);
      });

    it('When the user clicks continue on the hub and it takes you to a section which is complete but doesnt have a summary, then last question guidance is not shown', function () {
        $(HobbiesPage.yes()).click();
        $(HobbiesPage.submit()).click();
        $(HubPage.summaryRowLink(3)).click();
        expect(browser.getUrl()).to.contain(SportsPage.url());
        expect(browser.getUrl()).not.to.contain(last_viewed_question_url_arg);
        expect($(SportsPage.mainContent()).getText()).not.to.contain(last_viewed_question_text);
      });
    });
  });


