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
    // :TODO: Add data attributes to elements below so we don't rely on tags or classes that are subject to DS changes
    expect($(previewQuestion).$("h3").getText()).to.equal("Are you able to report for the calendar month 1 January 2017 to 1 February 2017?");
    expect($(previewQuestion).$(".ons-question__description").getText()).to.equal("Your return should relate to the calendar year 2016.");
    expect($(previewQuestion).$$(".ons-panel__body")[0].getText()).to.equal("Please provide figures for the period in which you were trading.");
    $(".ons-details__heading").click();
    expect($(previewQuestion).$("#answer-guidance--content div p").getText()).to.equal("For example select `yes` if you can report for this period");
    expect($(previewQuestion).$$("p")[2].getText()).to.equal("You can answer with one of the following options:");
    expect($(previewQuestion).$$("p")[3].getText()).to.equal("Select your answer");
    expect($(previewQuestion).$$("ul")[0].getText()).to.equal("Yes\nNo");
  });
  it("Given I start a survey, When I view the preview page of hub flow schema, Then the twisty button should read 'Show all' and answers should be invisible", () => {
    browser.openQuestionnaire(introductionSchema);
    $(IntroductionPage.previewQuestions()).click();
    expect(browser.getUrl()).to.contain("questionnaire/preview");
    expect($(showButton).getText()).to.equal("Show all");
    expect($(previewSummaryContent).isClickable()).to.be.false;
    it("and click the twisty button, Then the twisty button should read 'Hide all' and the answers should be visible", () => {
      $(showButton).click();
      expect($(showButton).getText()).to.equal("Hide all");
      expect($(previewSummaryContent).isClickable()).to.be.true;
    });
  });
});
