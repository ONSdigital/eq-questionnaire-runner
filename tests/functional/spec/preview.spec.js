import IntroductionPage from "../generated_pages/introduction_preview_hub/introduction.page";
import HubPage from "../base_pages/hub.page.js";

describe("Introduction preview questions", () => {
  const introductionSchema = "test_introduction_preview_hub.json";
  const showButton = 'button[data-ga-category="Preview Survey"]';
  const summaryContent = "#summary-accordion-1-content";
  beforeEach(() => {
    browser.openQuestionnaire(introductionSchema);
  });

  it("Given I start a survey, When I view the preview page of hub flow schema, Then I should be able to use the twisty button", () => {
    browser.openQuestionnaire(introductionSchema);
    $(HubPage.submit()).click();
    $(IntroductionPage.previewQuestions()).click();
    expect(browser.getUrl()).to.contain("questionnaire/preview");
    expect($(showButton).getText()).to.equal("Show all");
    expect($(summaryContent).isClickable()).to.be.false;
    $(showButton).click();
    expect($(showButton).getText()).to.equal("Hide all");
    expect($(summaryContent).isClickable()).to.be.true;
  });
});
