import DateQuestionPage from "../../../generated_pages/placeholder_transform_date_range_bounds/date-question.page";
import DaysQuestionBlockPage from "../../../generated_pages/placeholder_transform_date_range_bounds/days-question-block.page";
import Block0Page from "../../../generated_pages/placeholder_transform_date_range_bounds/block0.page";
import RangeQuestionBlockPage from "../../../generated_pages/placeholder_transform_date_range_bounds/range-question-block.page";
import { click } from "../../../helpers";
describe("Date checks", () => {
  beforeEach("Load the survey", async () => {
    await browser.openQuestionnaire("test_placeholder_transform_date_range_bounds.json");
  });

  it("Given a reference date is provided, when I get to the next page, then the placeholder contains a formatted date range based on the reference date", async () => {
    await $(DateQuestionPage.day()).setValue(8);
    await $(DateQuestionPage.month()).setValue(9);
    await $(DateQuestionPage.year()).setValue(2021);

    await click(DateQuestionPage.submit());

    await expect(await $(DaysQuestionBlockPage.questionText()).getText()).toContain("Monday 30 August to Monday 13 September 2021");
    await click(DaysQuestionBlockPage.submit());
  });

  it("Given a reference date is provided, when I get to the next page, then the placeholder contains a formatted date range", async () => {
    await $(DateQuestionPage.day()).setValue(15);
    await $(DateQuestionPage.month()).setValue(9);
    await $(DateQuestionPage.year()).setValue(2021);

    await click(DateQuestionPage.submit());
    await click(DaysQuestionBlockPage.submit());

    await $(Block0Page.ref0day()).setValue(1);
    await $(Block0Page.ref0month()).setValue(5);
    await $(Block0Page.ref0year()).setValue(2019);

    await $(Block0Page.ref1day()).setValue(19);
    await $(Block0Page.ref1month()).setValue(5);
    await $(Block0Page.ref1year()).setValue(2019);

    await click(Block0Page.submit());

    await expect(await $(RangeQuestionBlockPage.questionText()).getText()).toContain("Wednesday 1 to Sunday 19 May 2019");
  });
});
