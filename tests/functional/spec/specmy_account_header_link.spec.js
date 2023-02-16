import IntroductionPage from "../generated_pages/introduction/introduction.page";

describe("My Account header link", () => {
  it("Given I start a survey, When I visit a page then I should not see the My account button", async ()=> {
    await browser.openQuestionnaire("test_introduction.json");
    await expect(browser.getUrl()).to.contain("introduction");
    await expect(await $(await IntroductionPage.myAccountLink()).isExisting()).to.be.false;
  });
});
