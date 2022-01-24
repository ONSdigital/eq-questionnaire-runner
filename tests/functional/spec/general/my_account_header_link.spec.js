import IntroductionPage from "../generated_pages/introduction/introduction.page";

describe("My Account header link", () => {
  it("Given I start a survey, When I visit a page then I should not see the My account button", () => {
    browser.openQuestionnaire("test_introduction.json");
    expect(browser.getUrl()).to.contain("introduction");
    expect($(IntroductionPage.myAccountLink()).isExisting()).to.be.false;
  });
});
