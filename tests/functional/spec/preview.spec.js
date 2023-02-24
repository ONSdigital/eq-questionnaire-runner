import IntroductionPage from "../generated_pages/introduction_preview_hub/introduction.page";

describe("Introduction preview questions", () => {
  const introductionSchema = "test_introduction_preview_hub.json";
  const showButton = 'button[data-ga-category="Preview Survey"]';
  const previewSummaryContent = "#summary-accordion-1-content";
  beforeEach(() => {
    browser.openQuestionnaire(introductionSchema);
  });

  it("Given I start a survey, When I view the preview page of hub flow schema, Then the twisty button should read 'Show all' and answers should be invisible", () => {
    browser.openQuestionnaire(introductionSchema);
    $(IntroductionPage.previewQuestions()).click();
    expect(browser.getUrl()).to.contain("questionnaire/preview");
    expect($(showButton).getText()).to.equal("Show all");
    expect($(previewSummaryContent).isClickable()).to.be.false;
  });
  it("Given I start a survey, When I view the preview page and click the twisty button, Then the twisty button should read 'Hide all' and the answers should be visible", () => {
    browser.openQuestionnaire(introductionSchema);
    $(IntroductionPage.previewQuestions()).click();
    expect(browser.getUrl()).to.contain("questionnaire/preview");
    $(showButton).click();
    expect($(showButton).getText()).to.equal("Hide all");
    expect($(previewSummaryContent).isClickable()).to.be.true;
  });
});
