import TimeoutInterstitialPage from "../../../generated_pages/timeout_modal/timeout-modal-interstitial.page";
import { TimeoutModalTestCase } from "../timeout_modal.js";

describe("Timeout Modal Expired", () => {
  describe("Given I am completing the survey,", () => {
    before(async () => {
      await browser.openQuestionnaire("test_timeout_modal.json");
    });
    TimeoutModalTestCase.testCaseExtended(TimeoutInterstitialPage);
  });
});
