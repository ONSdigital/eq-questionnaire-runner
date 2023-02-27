import IntroductionPage from "../generated_pages/introduction_hub/introduction.page";
import IntroductionPageLinear from "../generated_pages/introduction/introduction.page";

describe("Introduction preview questions", () => {
  const introductionSchema = "test_introduction_hub.json";
  const introductionSchemaLinear = "test_introduction.json";
  const showButton = 'button[data-ga-category="Preview Survey"]';
  const previewSummaryContent = "#summary-accordion-1-content";
  const previewSectionTitle = ".ons-summary__group-title";
  const previewQuestion = ".ons-summary__item";

  it("Given I start a survey, When I view the preview page, Then all preview elements should be visible", () => {
    browser.openQuestionnaire(introductionSchemaLinear);
    $(IntroductionPageLinear.previewQuestions()).click();
    expect(browser.getUrl()).to.contain("questionnaire/preview");
    expect($(previewSectionTitle).getText()).to.equal("Main section");
    expect($(previewQuestion).$("h3").getText()).to.equal("Are you able to report for the calendar month 1 January 2017 to 1 February 2017?");
    expect($(previewQuestion).$(".ons-question__description").getText()).to.equal("Your return should relate to the calendar year 2021.");
    expect($(previewQuestion).$(".ons-question__instruction").getText()).to.equal("Select your answer");
    expect($(previewQuestion).$(".ons-panel__body").getText()).to.equal("You can only pick one answer");
    expect($(previewQuestion).$$("p")[3].getText()).to.equal("Choose Yes or No answer");
    expect($(previewQuestion).$$("p")[4].getText()).to.equal("You can answer with the following options:");
    expect($(previewQuestion).$("ul").getText()).to.equal("Yes\nNo");
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
