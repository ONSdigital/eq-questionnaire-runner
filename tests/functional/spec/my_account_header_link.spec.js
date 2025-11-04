import IntroductionPage from "../generated_pages/introduction/introduction.page";
import { verifyUrlContains, waitForQuestionnaireToLoad } from "../helpers";

describe("My Account header link", () => {
  it("Given I start a survey, When I visit a page then I should not see the My account button", async () => {
    await browser.openQuestionnaire("test_introduction.json");
    await waitForQuestionnaireToLoad();
    await verifyUrlContains("introduction");
    await expect(await $(IntroductionPage.myAccountLink()).isExisting()).toBe(false);
  });
});
