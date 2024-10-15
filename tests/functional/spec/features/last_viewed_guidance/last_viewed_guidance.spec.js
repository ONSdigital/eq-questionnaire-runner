import { getRandomString } from "../../../jwt_helper";
import AddressConfirmationPage from "../../../generated_pages/last_viewed_question_guidance/address-confirmation.page";
import HouseholdInterstitialPage from "../../../generated_pages/last_viewed_question_guidance/household-interstitial.page.js";
import PrimaryPersonListCollectorPage from "../../../generated_pages/last_viewed_question_guidance/primary-person-list-collector.page.js";
import { click } from "../../../helpers";
describe("Last viewed question guidance", () => {
  const resumableLaunchParams = {
    responseId: getRandomString(16),
    userId: "test_user",
  };

  describe("Given the last viewed question guidance questionnaire", () => {
    before("Open survey", async () => {
      await browser.openQuestionnaire("test_last_viewed_question_guidance.json", resumableLaunchParams);
    });

    it("When the respondent first launches the survey, then last question guidance is not shown", async () => {
      await expect(browser).toHaveUrl(expect.stringContaining(HouseholdInterstitialPage.url()));
      await expect(await $(HouseholdInterstitialPage.lastViewedQuestionGuidance()).isExisting()).toBe(false);
    });

    it("When the respondent resumes on the first block of a section, then last question guidance is not shown", async () => {
      await $(HouseholdInterstitialPage.saveSignOut()).click();
      await browser.openQuestionnaire("test_last_viewed_question_guidance.json", resumableLaunchParams);
      await browser.pause(100);
      await expect(browser).toHaveUrl(expect.stringContaining(HouseholdInterstitialPage.url()));
      await expect(await $(HouseholdInterstitialPage.lastViewedQuestionGuidance()).isExisting()).toBe(false);
    });

    it("When the respondent saves and resumes from a section which is in progress, then last question guidance is shown", async () => {
      await click(HouseholdInterstitialPage.submit());
      await $(AddressConfirmationPage.saveSignOut()).click();
      await browser.openQuestionnaire("test_last_viewed_question_guidance.json", resumableLaunchParams);
      await browser.pause(100);
      await expect(browser).toHaveUrl(expect.stringContaining(AddressConfirmationPage.url()));
      await expect(await $(AddressConfirmationPage.lastViewedQuestionGuidanceLink()).getAttribute("href")).toContain(HouseholdInterstitialPage.url());
      await expect(await $(AddressConfirmationPage.lastViewedQuestionGuidance()).isExisting()).toBe(true);
    });

    it("When the respondent answers the question and saves and continues, then last question guidance is not shown on the next question", async () => {
      await $(AddressConfirmationPage.yes()).click();
      await click(AddressConfirmationPage.submit());
      await expect(browser).toHaveUrl(expect.stringContaining(PrimaryPersonListCollectorPage.url()));
      await expect(await $(HouseholdInterstitialPage.lastViewedQuestionGuidance()).isExisting()).toBe(false);
    });

    it("When the respondent uses the previous link from the next question, then last question guidance is not shown", async () => {
      await click(AddressConfirmationPage.submit());
      await $(PrimaryPersonListCollectorPage.previous()).click();
      await expect(await $(HouseholdInterstitialPage.lastViewedQuestionGuidance()).isExisting()).toBe(false);
    });
  });
});
