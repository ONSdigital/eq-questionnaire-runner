const JwtHelper = require("../../../jwt_helper");

const AddressConfirmationPage = require('../../../generated_pages/last_viewed_question_guidance/address-confirmation.page.js');
const HouseholdInterstitialPage = require('../../../generated_pages/last_viewed_question_guidance/household-interstitial.page.js');
const PrimaryPersonListCollectorPage = require('../../../generated_pages/last_viewed_question_guidance/primary-person-list-collector.page.js');

describe('Last viewed question guidance', function () {

  const responseId = JwtHelper.getRandomString(16);

  describe('Given a standard survey', function () {
    before('Open survey', function () {
      browser.openQuestionnaire('test_last_viewed_question_guidance.json', { userId: "test_user", responseId: responseId });
    });

    it('When the respondent first launches the survey, then last question guidance is not shown', function () {
      expect(browser.getUrl()).to.contain(HouseholdInterstitialPage.url());
      expect($(HouseholdInterstitialPage.lastViewedQuestionGuidance()).isExisting()).to.be.false;
    });

    it('When the respondent resumes on the first block of a section, then last question guidance is not shown' , function () {
      $(HouseholdInterstitialPage.saveSignOut()).click();
      browser.openQuestionnaire('test_last_viewed_question_guidance.json', { userId: "test_user", responseId: responseId });
      expect(browser.getUrl()).to.contain(HouseholdInterstitialPage.url());
      expect($(HouseholdInterstitialPage.lastViewedQuestionGuidance()).isExisting()).to.be.false;
    });

    it('When the respondent saves and resumes from a section which is in progress, then last question guidance is shown', function () {
      $(HouseholdInterstitialPage.submit()).click();
      $(AddressConfirmationPage.saveSignOut()).click();
      browser.openQuestionnaire('test_last_viewed_question_guidance.json', { userId: "test_user", responseId: responseId });
      expect(browser.getUrl()).to.contain(AddressConfirmationPage.url());
      expect($(AddressConfirmationPage.lastViewedQuestionGuidanceLink()).getAttribute('href')).to.contain(HouseholdInterstitialPage.url());
      expect($(AddressConfirmationPage.lastViewedQuestionGuidance()).isExisting()).to.be.true;

    });

    it('When the respondent answers the next question and saves and continues, then last question guidance is not shown', function () {
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
