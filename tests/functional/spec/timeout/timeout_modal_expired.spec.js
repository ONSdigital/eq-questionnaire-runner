import TimeoutInterstitialPage from "../../generated_pages/timeout_modal/timeout-modal-interstitial.page";
import { TimeoutModalTestCase } from "./timeout_modal.js";

describe("Timeout Modal", () => {
  describe("Given I am completing the survey,", () => {
    beforeEach(() => {
      browser.openQuestionnaire("test_timeout_modal.json");
    });
    TimeoutModalTestCase.testCaseExpired(TimeoutInterstitialPage);
  });
});
