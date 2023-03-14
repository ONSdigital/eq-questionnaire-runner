import TimeoutInterstitialPage from "../../../generated_pages/timeout_modal/timeout-modal-interstitial.page";
import TimeoutSubmitPage from "../../../generated_pages/timeout_modal/submit.page";
import ThankYouPage from "../../../base_pages/thank-you.page";
import { TimeoutModalTestCase } from "../timeout_modal.js";

describe("Timeout Modal Post Submission Expired", () => {
  describe("Given I am completing the survey and get to post submission page,", () => {
    before(async () => {
      await browser.openQuestionnaire("test_timeout_modal.json");
      await $(TimeoutInterstitialPage.submit()).click();
      await $(TimeoutSubmitPage.submit()).click();
    });
    TimeoutModalTestCase.testCaseExpired(ThankYouPage);
  });
});
