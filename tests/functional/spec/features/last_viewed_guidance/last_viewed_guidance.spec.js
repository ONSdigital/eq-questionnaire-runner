const JwtHelper = require("../../../jwt_helper");

const AddressConfirmationPage = require('../../../generated_pages/last_viewed_question_guidance/address-confirmation.page.js');
const HouseholdInterstitialPage = require('../../../generated_pages/last_viewed_question_guidance/household-interstitial.page.js');
const PrimaryPersonListCollectorPage = require('../../../generated_pages/last_viewed_question_guidance/primary-person-list-collector.page.js');

describe('Last viewed question guidance', function () {

  const resumableLaunchParams = {
    responseId: JwtHelper.getRandomString(16),
    userId: "test_user"
  };

  describe('Given the last viewed question guidance questionnaire', function () {
    before('Open survey', function () {
      browser.openQuestionnaire('test_last_viewed_question_guidance.json', resumableLaunchParams);
    });

    it('When the respondent first launches the survey, then last question guidance is not shown', function () {
      expect(browser.getUrl()).to.contain(HouseholdInterstitialPage.url());
      expect($(HouseholdInterstitialPage.lastViewedQuestionGuidance()).isExisting()).to.be.false;
    });

    it('When the respondent resumes on the first block of a section, then last question guidance is not shown' , function () {
      $(HouseholdInterstitialPage.saveSignOut()).click();
      browser.openQuestionnaire('test_last_viewed_question_guidance.json', resumableLaunchParams);
      expect(browser.getUrl()).to.contain(HouseholdInterstitialPage.url());
      expect($(HouseholdInterstitialPage.lastViewedQuestionGuidance()).isExisting()).to.be.false;
    });

    it('When the respondent saves and resumes from a section which is in progress, then last question guidance is shown', function () {
      $(HouseholdInterstitialPage.submit()).click();
      $(AddressConfirmationPage.saveSignOut()).click();
      browser.openQuestionnaire('test_last_viewed_question_guidance.json', resumableLaunchParams);
      expect(browser.getUrl()).to.contain(AddressConfirmationPage.url());
      expect($(AddressConfirmationPage.lastViewedQuestionGuidanceLink()).getAttribute('href')).to.contain(HouseholdInterstitialPage.url());
      expect($(AddressConfirmationPage.lastViewedQuestionGuidance()).isExisting()).to.be.true;

    });

    it('When the respondent answers the question and saves and continues, then last question guidance is not shown on the next question', function () {
      $(AddressConfirmationPage.yes()).click();
      $(AddressConfirmationPage.submit()).click();
      expect(browser.getUrl()).to.contain(PrimaryPersonListCollectorPage.url());
      expect($(HouseholdInterstitialPage.lastViewedQuestionGuidance()).isExisting()).to.be.false;
    });

    it('When the respondent uses the previous link from the next question, then last question guidance is not shown', function () {
      $(AddressConfirmationPage.submit()).click();
      $(PrimaryPersonListCollectorPage.previous()).click();
      expect($(HouseholdInterstitialPage.lastViewedQuestionGuidance()).isExisting()).to.be.false;
    });
  });
});
