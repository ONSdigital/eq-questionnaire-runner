import DateQuestionPage from "../generated_pages/generate_date_range/date-question.page";
import DaysQuestionBlockPage from "../generated_pages/generate_date_range/days-question-block.page";
import RangeQuestionBlockPage from "../generated_pages/generate_date_range/range-question-block.page";
import RangeMonthQuestionBlockPage from "../generated_pages/generate_date_range/range-month-question-block.page";
import RangeYearQuestionBlockPage from "../generated_pages/generate_date_range/range-year-question-block.page";
// import SubmitPage from "../generated_pages/generate_date_range/submit.page";

describe("Date checks", () => {
  beforeEach("Load the survey", () => {
    browser.openQuestionnaire("test_generate_date_range.json");
  });

  it("Given a reference date is provided, when I get to the next page, then the placeholder contains a formatted date range based on the reference date", () => {
    $(DateQuestionPage.day()).setValue(15);
    $(DateQuestionPage.month()).setValue(9);
    $(DateQuestionPage.year()).setValue(2021);

    $(DateQuestionPage.submit()).click();

    expect($(DaysQuestionBlockPage.questionText()).getText()).to.contain("Monday 30 August to Monday 13 September 2021");
    $(DaysQuestionBlockPage.submit()).click();
  });

  it("Given a reference date is provided, when I get to the next page, then the placeholder contains a formatted date range", () => {

    $(DateQuestionPage.day()).setValue(15);
    $(DateQuestionPage.month()).setValue(9);
    $(DateQuestionPage.year()).setValue(2021);

    $(DateQuestionPage.submit()).click();
    $(DaysQuestionBlockPage.submit()).click();

    expect($(RangeQuestionBlockPage.questionText()).getText()).to.contain("Wednesday 1 to Sunday 19 May 2019");
  });

  it("Given a reference date is provided, when I get to the next page, then the placeholder contains a formatted date range where the range spans more than one month", () => {

    $(DateQuestionPage.day()).setValue(15);
    $(DateQuestionPage.month()).setValue(9);
    $(DateQuestionPage.year()).setValue(2021);

    $(DateQuestionPage.submit()).click();
    $(DaysQuestionBlockPage.submit()).click();
    $(RangeQuestionBlockPage.submit()).click();

    expect($(RangeMonthQuestionBlockPage.questionText()).getText()).to.contain("Wednesday 1 May to Saturday 1 June 2019");
  });

  it("Given a reference date is provided, when I get to the next page, then the placeholder contains a formatted date range where the range spans more than one year", () => {

    $(DateQuestionPage.day()).setValue(15);
    $(DateQuestionPage.month()).setValue(9);
    $(DateQuestionPage.year()).setValue(2021);

    $(DateQuestionPage.submit()).click();
    $(DaysQuestionBlockPage.submit()).click();
    $(RangeQuestionBlockPage.submit()).click();
    $(RangeMonthQuestionBlockPage.submit()).click();

    expect($(RangeYearQuestionBlockPage.questionText()).getText()).to.contain("Wednesday 1 May 2019 to Friday 1 May 2020");
  });
});
