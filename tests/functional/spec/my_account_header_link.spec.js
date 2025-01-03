import IntroductionPage from "../generated_pages/introduction/introduction.page";
import { verifyUrlContains } from "../helpers";

describe("My Account header link", () => {
  it("Given I start a survey, When I visit a page then I should not see the My account button", async () => {
    await browser.openQuestionnaire("test_introduction.json");
    await browser.pause(100);
    await verifyUrlContains("introduction");
    await expect(await $(IntroductionPage.myAccountLink()).isExisting()).toBe(false);
  });
});
