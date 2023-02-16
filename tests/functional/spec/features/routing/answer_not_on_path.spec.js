import InitialChoicePage from "../../../generated_pages/new_routing_not_affected_by_answers_not_on_path/initial-choice.page.js";
import InvalidPathPage from "../../../generated_pages/new_routing_not_affected_by_answers_not_on_path/invalid-path.page.js";
import InvalidPathInterstitialPage from "../../../generated_pages/new_routing_not_affected_by_answers_not_on_path/invalid-path-interstitial.page.js";
import ValidPathPage from "../../../generated_pages/new_routing_not_affected_by_answers_not_on_path/valid-path.page.js";
import ValidFinalInterstitialPage from "../../../generated_pages/new_routing_not_affected_by_answers_not_on_path/valid-final-interstitial.page.js";

describe("Answers not on path are not considered when routing", () => {
  beforeEach(async ()=> {
    await browser.openQuestionnaire("test_new_routing_not_affected_by_answers_not_on_path.json");
  });

  it("Given the user enters an answer on the first path, when they return to the second path, they should be routed to the valid path interstitial", async ()=> {
    await $(await InitialChoicePage.goHereFirst()).click();
    await $(await InitialChoicePage.submit()).click();

    await expect(browser.getUrl()).to.contain(InvalidPathPage.pageName);
    await $(await InvalidPathPage.answer()).setValue(123);
    await $(await InvalidPathPage.submit()).click();

    // We now have an answer in the store on the 'invalid' path

    await expect(browser.getUrl()).to.contain(InvalidPathInterstitialPage.pageName);
    await $(await InvalidPathInterstitialPage.previous()).click();
    await $(await InvalidPathPage.previous()).click();

    // Take the second route

    await $(await InitialChoicePage.goHereSecond()).click();
    await $(await InitialChoicePage.submit()).click();

    await $(await ValidPathPage.answer()).setValue(321);
    await $(await ValidPathPage.submit()).click();

    // We should be routed to the valid interstitial page since the invalid path answer should not be considered whilst routing.
    await expect(browser.getUrl()).to.contain(ValidFinalInterstitialPage.pageName);
  });
});
