import InitialChoicePage from "../../../generated_pages/routing_not_affected_by_answers_not_on_path/initial-choice.page.js";
import InvalidPathPage from "../../../generated_pages/routing_not_affected_by_answers_not_on_path/invalid-path.page.js";
import InvalidPathInterstitialPage from "../../../generated_pages/routing_not_affected_by_answers_not_on_path/invalid-path-interstitial.page.js";
import ValidPathPage from "../../../generated_pages/routing_not_affected_by_answers_not_on_path/valid-path.page.js";
import ValidFinalInterstitialPage from "../../../generated_pages/routing_not_affected_by_answers_not_on_path/valid-final-interstitial.page.js";
import { click } from "../../../helpers";
describe("Answers not on path are not considered when routing", () => {
  beforeEach(async () => {
    await browser.openQuestionnaire("test_routing_not_affected_by_answers_not_on_path.json");
  });

  it("Given the user enters an answer on the first path, when they return to the second path, they should be routed to the valid path interstitial", async () => {
    await $(InitialChoicePage.goHereFirst()).click();
    await click(InitialChoicePage.submit());

    await expect(await browser.getUrl()).toContain(InvalidPathPage.pageName);
    await $(InvalidPathPage.answer()).setValue(123);
    await click(InvalidPathPage.submit());

    // We now have an answer in the store on the 'invalid' path

    await expect(await browser.getUrl()).toContain(InvalidPathInterstitialPage.pageName);
    await $(InvalidPathInterstitialPage.previous()).click();
    await $(InvalidPathPage.previous()).click();

    // Take the second route

    await $(InitialChoicePage.goHereSecond()).click();
    await click(InitialChoicePage.submit());

    await $(ValidPathPage.answer()).setValue(321);
    await click(ValidPathPage.submit());

    // We should be routed to the valid interstitial page since the invalid path answer should not be considered whilst routing.
    await expect(await browser.getUrl()).toContain(ValidFinalInterstitialPage.pageName);
  });
});
