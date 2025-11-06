import IntroductionPageHub from "../generated_pages/introduction_hub/introduction.page";
import IntroductionPageLinear from "../generated_pages/introduction/introduction.page";
import { verifyUrlContains, waitForPageToLoad } from "../helpers";

describe("Introduction preview questions", () => {
  const introductionSchemaHub = "test_introduction_hub.json";
  const introductionSchemaLinear = "test_introduction.json";
  const showButton = 'button[data-ga-label="Hide all"]';
  const previewSummaryContent = "#summary-accordion-1-content";
  const previewSectionTitle = ".ons-summary__group-title";
  const previewQuestion = ".ons-summary__item";
  const printButton = 'button[data-qa="btn-print"]';
  const pdfButton = 'a[data-qa="btn-pdf"]';
  // const detailsHeading = ".ons-details__heading";
  const startSurveyButton = ".qa-btn-get-started";
  const noRadio = "#report-radio-answer-1";
  const submitButton = 'button[data-qa="btn-submit"]';
  const answerFromDay = "#answer-from-day";
  const answerFromMonth = "#answer-from-month";
  const answerFromYear = "#answer-from-year";
  const answerToDay = "#answer-to-day";
  const answerToMonth = "#answer-to-month";
  const answerToYear = "#answer-to-year";

  async function testPreview(schema, page) {
    await browser.openQuestionnaire(schema);
    await $(page.previewQuestions()).click();
    await verifyUrlContains("questionnaire/preview");
    if (schema === "test_introduction.json") {
      expect(await $(previewSectionTitle).getText()).toBe("Main section");
    } else {
      await $(showButton).click();
    }
    // :TODO: Add data attributes to elements below so we don't rely on tags or classes that are subject to DS changes
    expect(await $(previewQuestion).$("h3").getText()).toBe("Are you able to report for the calendar month 1 January 2017 to 1 February 2017?");
    expect(await $(previewQuestion).$(".ons-question__description").getText()).toBe("Your return should relate to the calendar year 2021.");
    expect(await $(previewQuestion).$$(".ons-panel__body")[0].getText()).toBe("Please provide figures for the period in which you were trading.");
    expect(await $(showButton).length).toBeUndefined();
    expect(await $(printButton).isClickable()).toBe(true);
    expect(await $(pdfButton).isClickable()).toBe(true);
    // answer guidance not implemented yet due to some work that needs to be done in the DS will be implemented in iteration 2
    // $(detailsHeading).click();
    // expect($(previewQuestion).$("#answer-guidance--content div p").getText()).to.equal("For example select `yes` if you can report for this period");
    expect(await $(previewQuestion).$$("p")[2].getText()).toBe("You can answer with one of the following options:");
    expect(await $(previewQuestion).$$("ul")[0].getText()).toBe("Yes\nNo");
  }

  it("Given I start a survey, When I view the preview page, Then all preview elements should be visible and any metadata piped answers are resolved", async () => {
    await testPreview(introductionSchemaHub, IntroductionPageHub);
    await testPreview(introductionSchemaLinear, IntroductionPageLinear);
  });

  it("Given I complete some of a survey and the piped answers should be being populated, Then preview answers should still be showing placeholders", async () => {
    await browser.openQuestionnaire(introductionSchemaLinear);
    await waitForPageToLoad();
    await $(startSurveyButton).click();
    await $(noRadio).click();
    await $(submitButton).click();
    await $(answerFromDay).setValue(5);
    await $(answerFromMonth).setValue(12);
    await $(answerFromYear).setValue(2016);
    await $(answerToDay).setValue(20);
    await $(answerToMonth).setValue(12);
    await $(answerToYear).setValue(2016);
    await $(submitButton).click();
    expect(await $("h1").getText()).toBe("Are you sure you are able to report for the calendar month 5 December 2016 to 20 December 2016?");
    await browser.url("questionnaire/introduction/");
    await $(IntroductionPageLinear.previewQuestions()).click();
    await verifyUrlContains("questionnaire/preview");
    expect(await $(previewSectionTitle).getText()).toBe("Main section");
    expect(await $$(previewQuestion)[2].$("h3").getText()).toBe(
      "Are you sure you are able to report for the calendar month {calendar_start_date} to {calendar_end_date}?",
    );
  });

  it("Given I start a survey, When I view the preview page of hub flow schema, Then the twisty button should read 'Show all' and answers should be invisible", async () => {
    await browser.openQuestionnaire(introductionSchemaHub);
    await $(IntroductionPageHub.previewQuestions()).click();
    await verifyUrlContains("questionnaire/preview");
    expect(await $(printButton).isClickable()).toBe(true);
    expect(await $(pdfButton).isClickable()).toBe(true);
    expect(await $(showButton).getText()).toBe("Show all");
    expect(await $(previewSummaryContent).isClickable()).toBe(false);
    it("and if the twisty button is clicked, Then the twisty button should read 'Hide all' and the answers should be visible", async () => {
      await $(showButton).click();
      expect(await $(showButton).getText()).toBe("Hide all");
      expect(await $(previewSummaryContent).isClickable()).toBe(true);
    });
  });
});
