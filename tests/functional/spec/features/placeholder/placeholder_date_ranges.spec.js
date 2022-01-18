import DateQuestionPage from "../../../generated_pages/placeholder_transform_date_range_bounds/date-question.page";
import DaysQuestionBlockPage from "../../../generated_pages/placeholder_transform_date_range_bounds/days-question-block.page";
import Block0Page from "../../../generated_pages/placeholder_transform_date_range_bounds/block0.page";
import RangeQuestionBlockPage from "../../../generated_pages/placeholder_transform_date_range_bounds/range-question-block.page";

describe("Date checks", () => {
  beforeEach("Load the survey", () => {
    browser.openQuestionnaire("test_placeholder_transform_date_range_bounds.json");
  });

  it("Given a reference date is provided, when I get to the next page, then the placeholder contains a formatted date range based on the reference date", () => {
    $(DateQuestionPage.day()).setValue(8);
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

    $(Block0Page.ref0day()).setValue(1);
    $(Block0Page.ref0month()).setValue(5);
    $(Block0Page.ref0year()).setValue(2019);

    $(Block0Page.ref1day()).setValue(19);
    $(Block0Page.ref1month()).setValue(5);
    $(Block0Page.ref1year()).setValue(2019);

    $(Block0Page.submit()).click();

    expect($(RangeQuestionBlockPage.questionText()).getText()).to.contain("Wednesday 1 to Sunday 19 May 2019");
  });
});
