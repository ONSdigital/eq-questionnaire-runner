import { getRandomString } from "../../../jwt_helper";
import AddressConfirmationPage from "../../../generated_pages/last_viewed_question_guidance/address-confirmation.page.js";
import HouseholdInterstitialPage from "../../../generated_pages/last_viewed_question_guidance/household-interstitial.page.js";
import PrimaryPersonListCollectorPage from "../../../generated_pages/last_viewed_question_guidance/primary-person-list-collector.page.js";

describe("Last viewed question guidance", () => {
  const resumableLaunchParams = {
    responseId: getRandomString(16),
    userId: "test_user",
  };

  describe("Given the last viewed question guidance questionnaire", () => {
    before("Open survey", () => {
      browser.openQuestionnaire("test_last_viewed_question_guidance.json", resumableLaunchParams);
    });

    it("When the respondent first launches the survey, then last question guidance is not shown", () => {
      expect(browser.getUrl()).to.contain(HouseholdInterstitialPage.url());
      expect($(HouseholdInterstitialPage.lastViewedQuestionGuidance()).isExisting()).to.be.false;
    });

    it("When the respondent resumes on the first block of a section, then last question guidance is not shown", () => {
      $(HouseholdInterstitialPage.saveSignOut()).click();
      browser.openQuestionnaire("test_last_viewed_question_guidance.json", resumableLaunchParams);
      expect(browser.getUrl()).to.contain(HouseholdInterstitialPage.url());
      expect($(HouseholdInterstitialPage.lastViewedQuestionGuidance()).isExisting()).to.be.false;
    });

    it("When the respondent saves and resumes from a section which is in progress, then last question guidance is shown", () => {
      $(HouseholdInterstitialPage.submit()).click();
      $(AddressConfirmationPage.saveSignOut()).click();
      browser.openQuestionnaire("test_last_viewed_question_guidance.json", resumableLaunchParams);
      expect(browser.getUrl()).to.contain(AddressConfirmationPage.url());
      expect($(AddressConfirmationPage.lastViewedQuestionGuidanceLink()).getAttribute("href")).to.contain(HouseholdInterstitialPage.url());
      expect($(AddressConfirmationPage.lastViewedQuestionGuidance()).isExisting()).to.be.true;
    });

    it("When the respondent answers the question and saves and continues, then last question guidance is not shown on the next question", () => {
      $(AddressConfirmationPage.yes()).click();
      $(AddressConfirmationPage.submit()).click();
      expect(browser.getUrl()).to.contain(PrimaryPersonListCollectorPage.url());
      expect($(HouseholdInterstitialPage.lastViewedQuestionGuidance()).isExisting()).to.be.false;
    });

    it("When the respondent uses the previous link from the next question, then last question guidance is not shown", () => {
      $(AddressConfirmationPage.submit()).click();
      $(PrimaryPersonListCollectorPage.previous()).click();
      expect($(HouseholdInterstitialPage.lastViewedQuestionGuidance()).isExisting()).to.be.false;
    });
  });
});
