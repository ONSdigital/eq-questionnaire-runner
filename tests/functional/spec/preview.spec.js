import IntroductionPage from "../generated_pages/introduction_hub/introduction.page";
import IntroductionPageLinear from "../generated_pages/introduction/introduction.page";
import { expect } from "chai";

describe("Introduction preview questions", () => {
  const introductionSchema = "test_introduction_hub.json";
  const introductionSchemaLinear = "test_introduction.json";
  const showButton = 'button[data-ga-category="Preview Survey"]';
  const previewSummaryContent = "#summary-accordion-1-content";
  const previewSectionTitle = ".ons-summary__group-title";
  const previewQuestion = ".ons-summary__item";
  const printButton = 'button[data-qa="btn-print"]';
  const pdfButton = 'a[data-qa="btn-pdf"]';
  const detailsHeading = ".ons-details__heading";
  const startSurveyButton = ".qa-btn-get-started";
  const dateQuestionType = '[data-qa="question-type"]';
  const noRadio = "#report-radio-answer-1";
  const submitButton = 'button[data-qa="btn-submit"]';
  const answerFromDay = "#answer-from-day";
  const answerFromMonth = "#answer-from-month";
  const answerFromYear = "#answer-from-year";
  const answerToDay = "#answer-to-day";
  const answerToMonth = "#answer-to-month";
  const answerToYear = "#answer-to-year";

  it("Given I start a survey, When I view the preview page, Then all preview elements should be visible", () => {
    browser.openQuestionnaire(introductionSchemaLinear);
    $(IntroductionPageLinear.previewQuestions()).click();
    expect(browser.getUrl()).to.contain("questionnaire/preview");
    expect($(previewSectionTitle).getText()).to.equal("Main section");
    // :TODO: Add data attributes to elements below so we don't rely on tags or classes that are subject to DS changes
    expect($(previewQuestion).$("h3").getText()).to.equal("Are you able to report for the calendar month 1 January 2017 to 1 February 2017?");
    expect($(previewQuestion).$(".ons-question__description").getText()).to.equal("Your return should relate to the calendar year 2016.");
    expect($(previewQuestion).$$(".ons-panel__body")[0].getText()).to.equal("Please provide figures for the period in which you were trading.");
    expect($(showButton).length).to.be.undefined;
    expect($(printButton).isClickable()).to.be.true;
    expect($(pdfButton).isClickable()).to.be.true;
    $(detailsHeading).click();
    expect($(previewQuestion).$("#answer-guidance--content div p").getText()).to.equal("For example select `yes` if you can report for this period");
    expect($(previewQuestion).$$("p")[2].getText()).to.equal("You can answer with one of the following options:");
    expect($(previewQuestion).$$("ul")[0].getText()).to.equal("Yes\nNo");
    expect($(dateQuestionType).getText()).to.equal("DateRange");
  });

  it("Given I complete some of a survey and the piped answers should be being populated, Then preview answers should still be showing placeholders", () => {
    browser.openQuestionnaire(introductionSchemaLinear);
    $(startSurveyButton).click();
    $(noRadio).click();
    $(submitButton).click();
    $(answerFromDay).setValue(5);
    $(answerFromMonth).setValue(12);
    $(answerFromYear).setValue(2016);
    $(answerToDay).setValue(20);
    $(answerToMonth).setValue(12);
    $(answerToYear).setValue(2016);
    $(submitButton).click();
    expect($("h1").getText()).to.equal("Are you sure you are able to report for the calendar month 5 December 2016 to 20 December 2016?");
    browser.url("questionnaire/introduction/");
    $(IntroductionPageLinear.previewQuestions()).click();
    expect(browser.getUrl()).to.contain("questionnaire/preview");
    expect($(previewSectionTitle).getText()).to.equal("Main section");
    expect($$(previewQuestion)[2].$("h3").getText()).to.equal("Are you sure you are able to report for the calendar month start_date to end_date?");
  });

  it("Given I start a survey, When I view the preview page of hub flow schema, Then the twisty button should read 'Show all' and answers should be invisible", () => {
    browser.openQuestionnaire(introductionSchema);
    $(IntroductionPage.previewQuestions()).click();
    expect(browser.getUrl()).to.contain("questionnaire/preview");
    expect($(printButton).isClickable()).to.be.true;
    expect($(pdfButton).isClickable()).to.be.true;
    expect($(showButton).getText()).to.equal("Show all");
    expect($(previewSummaryContent).isClickable()).to.be.false;
    it("and if the twisty button is clicked, Then the twisty button should read 'Hide all' and the answers should be visible", () => {
      $(showButton).click();
      expect($(showButton).getText()).to.equal("Hide all");
      expect($(previewSummaryContent).isClickable()).to.be.true;
    });
  });
});
