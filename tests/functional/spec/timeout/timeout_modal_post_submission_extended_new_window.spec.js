import TimeoutInterstitialPage from "../../generated_pages/timeout_modal/timeout-modal-interstitial.page";
import TimeoutSubmitPage from "../../generated_pages/timeout_modal/submit.page";
import ThankYouPage from "../../base_pages/thank-you.page.js";

import { TimeoutModalTestCase } from "./timeout_modal.js";

describe("Timeout Modal Post Submission", () => {
  describe("Given I am completing the survey and get to post submission page,", () => {
    beforeEach(() => {
      browser.openQuestionnaire("test_timeout_modal.json");
      $(TimeoutInterstitialPage.submit()).click();
      $(TimeoutSubmitPage.submit()).click();
    });
    TimeoutModalTestCase.testCaseExtendedNewWindow(ThankYouPage);
  });
});
