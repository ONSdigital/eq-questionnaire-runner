import DateRangePage from "../generated_pages/dates/date-range-block.page";
import DateMonthYearPage from "../generated_pages/dates/date-month-year-block.page";
import DateSinglePage from "../generated_pages/dates/date-single-block.page";
import DateNonMandatoryPage from "../generated_pages/dates/date-non-mandatory-block.page";
import DateYearDatePage from "../generated_pages/dates/date-year-date-block.page";
import SubmitPage from "../generated_pages/dates/submit.page";
import { click, verifyUrlContains } from "../helpers";

describe("Date checks", () => {
  beforeEach("Load the survey", async () => {
    await browser.openQuestionnaire("test_dates.json");
  });

  it("Given an answer label is provided for a date question then the label should be displayed ", async () => {
    await expect(await $(DateRangePage.legend()).getText()).toBe("Period from");
  });

  it("Given an answer label is not provided for a date question then the question title should be used within the legend ", async () => {
    await $(DateRangePage.dateRangeFromday()).setValue(1);
    await $(DateRangePage.dateRangeFrommonth()).setValue(1);
    await $(DateRangePage.dateRangeFromyear()).setValue(1901);

    await $(DateRangePage.dateRangeToday()).setValue(3);
    await $(DateRangePage.dateRangeTomonth()).setValue(5);
    await $(DateRangePage.dateRangeToyear()).setValue(2017);

    await click(DateRangePage.submit());

    await expect(await $(DateMonthYearPage.legend()).getText()).toBe("Date with month and year");
  });

  it("Given the test_dates survey is selected when dates are entered then the summary screen shows the dates entered formatted", async () => {
    // When dates are entered
    await $(DateRangePage.dateRangeFromday()).setValue(1);
    await $(DateRangePage.dateRangeFrommonth()).setValue(1);
    await $(DateRangePage.dateRangeFromyear()).setValue(1901);

    await $(DateRangePage.dateRangeToday()).setValue(3);
    await $(DateRangePage.dateRangeTomonth()).setValue(5);
    await $(DateRangePage.dateRangeToyear()).setValue(2017);

    await click(DateRangePage.submit());

    await $(DateMonthYearPage.Month()).setValue(4);
    await $(DateMonthYearPage.Year()).setValue(2018);

    await click(DateMonthYearPage.submit());

    await $(DateSinglePage.day()).setValue(4);
    await $(DateSinglePage.month()).setValue(1);
    await $(DateSinglePage.year()).setValue(1999);

    await click(DateSinglePage.submit());

    await click(DateNonMandatoryPage.submit());

    await $(DateYearDatePage.Year()).setValue(2005);

    await click(DateYearDatePage.submit());

    await verifyUrlContains(SubmitPage.pageName);

    // Then the summary screen shows the dates entered formatted
    await expect(await $(SubmitPage.dateRangeFromAnswer()).getText()).toBe("1 January 1901 to 3 May 2017");
    await expect(await $(SubmitPage.monthYearAnswer()).getText()).toBe("April 2018");
    await expect(await $(SubmitPage.singleDateAnswer()).getText()).toBe("4 January 1999");
    await expect(await $(SubmitPage.nonMandatoryDateAnswer()).getText()).toBe("No answer provided");
    await expect(await $(SubmitPage.yearDateAnswer()).getText()).toBe("2005");
  });

  it("Given the test_dates survey is selected when the from date is greater than the to date then an error message is shown", async () => {
    // When the from date is greater than the to date
    await $(DateRangePage.dateRangeFromday()).setValue(1);
    await $(DateRangePage.dateRangeFrommonth()).setValue(1);
    await $(DateRangePage.dateRangeFromyear()).setValue(2016);

    await $(DateRangePage.dateRangeToday()).setValue(1);
    await $(DateRangePage.dateRangeTomonth()).setValue(1);
    await $(DateRangePage.dateRangeToyear()).setValue(2015);

    await click(DateRangePage.submit());

    // Then an error message is shown and the question panel is highlighted
    await expect(await $(DateRangePage.errorNumber(1)).getText()).toBe("Enter a 'period to' date later than the 'period from' date");
    await expect(await $(DateRangePage.dateRangeQuestionErrorPanel()).isExisting()).toBe(true);

    // Then clicking error should focus on first input field
    await $(DateRangePage.errorNumber(1)).click();
    await expect(await $(DateRangePage.dateRangeFromday()).isFocused()).toBe(true);
  });

  it("Given the test_dates survey is selected when the from date and the to date are the same then an error message is shown", async () => {
    // When the from date is greater than the to date
    await $(DateRangePage.dateRangeFromday()).setValue(1);
    await $(DateRangePage.dateRangeFrommonth()).setValue(1);
    await $(DateRangePage.dateRangeFromyear()).setValue(2016);

    await $(DateRangePage.dateRangeToday()).setValue(1);
    await $(DateRangePage.dateRangeTomonth()).setValue(1);
    await $(DateRangePage.dateRangeToyear()).setValue(2016);

    await click(DateRangePage.submit());

    // Then an error message is shown and the question panel is highlighted
    await expect(await $(DateRangePage.errorNumber(1)).getText()).toBe("Enter a 'period to' date later than the 'period from' date");
    await expect(await $(DateRangePage.dateRangeQuestionErrorPanel()).isExisting()).toBe(true);
  });

  it("Given the test_dates survey is selected when an invalid date is entered in a date range then an error message is shown", async () => {
    // When the from date is greater than the to date
    await $(DateRangePage.dateRangeFromday()).setValue(1);
    await $(DateRangePage.dateRangeFrommonth()).setValue(1);
    await $(DateRangePage.dateRangeFromyear()).setValue(2016);

    await $(DateRangePage.dateRangeToday()).setValue(1);
    await $(DateRangePage.dateRangeTomonth()).setValue(1);
    await $(DateRangePage.dateRangeToyear()).setValue("");

    await click(DateRangePage.submit());

    // Then an error message is shown
    await expect(await $(DateRangePage.errorNumber(1)).getText()).toBe("Enter a valid date");
  });

  it("Given the test_dates survey is selected when the year (month year type) is left empty then an error message is shown", async () => {
    await $(DateRangePage.dateRangeFromday()).setValue(1);
    await $(DateRangePage.dateRangeFrommonth()).setValue(1);
    await $(DateRangePage.dateRangeFromyear()).setValue(2016);
    await $(DateRangePage.dateRangeToday()).setValue(1);
    await $(DateRangePage.dateRangeTomonth()).setValue(1);
    await $(DateRangePage.dateRangeToyear()).setValue(2017);
    await click(DateRangePage.submit());

    // When the year (month year type) is left empty
    await $(DateMonthYearPage.Month()).setValue(4);
    await $(DateMonthYearPage.Year()).setValue("");

    await click(DateMonthYearPage.submit());

    // Then an error message is shown
    await expect(await $(DateMonthYearPage.errorNumber(1)).getText()).toBe("Enter a valid date");
  });

  it("Given the test_dates survey is selected, " + "When an error message is shown and it is corrected, " + "Then the next question is displayed", async () => {
    await $(DateRangePage.dateRangeFromday()).setValue(1);
    await $(DateRangePage.dateRangeFrommonth()).setValue(1);
    await $(DateRangePage.dateRangeFromyear()).setValue(2016);
    await $(DateRangePage.dateRangeToday()).setValue(1);
    await $(DateRangePage.dateRangeTomonth()).setValue(1);
    await $(DateRangePage.dateRangeToyear()).setValue(2017);
    await click(DateRangePage.submit());

    // When an error message is shown
    await $(DateMonthYearPage.Month()).setValue(4);
    await $(DateMonthYearPage.Year()).setValue("");
    await click(DateMonthYearPage.submit());

    await expect(await $(DateMonthYearPage.error()).getText()).toBe("Enter a valid date");

    // Then when it is corrected, it goes to the next question
    await $(DateMonthYearPage.Year()).setValue(2018);
    await click(DateMonthYearPage.submit());

    await verifyUrlContains(DateSinglePage.url());
  });

  it("Given the test_dates survey is selected when an error message is shown then when it is corrected, it goes to the summary page and the information is correct", async () => {
    await $(DateRangePage.dateRangeFromday()).setValue(1);
    await $(DateRangePage.dateRangeFrommonth()).setValue(1);
    await $(DateRangePage.dateRangeFromyear()).setValue(2016);
    await $(DateRangePage.dateRangeToday()).setValue(1);
    await $(DateRangePage.dateRangeTomonth()).setValue(1);
    await $(DateRangePage.dateRangeToyear()).setValue(2017);
    await click(DateRangePage.submit());

    await $(DateMonthYearPage.Month()).setValue(1);
    await $(DateMonthYearPage.Year()).setValue(2016);
    await click(DateMonthYearPage.submit());

    await $(DateSinglePage.day()).setValue(1);
    await $(DateSinglePage.month()).setValue(1);
    await $(DateSinglePage.year()).setValue(2016);
    await click(DateMonthYearPage.submit());

    // When non-mandatory is partially completed
    await $(DateNonMandatoryPage.day()).setValue(4);
    await $(DateNonMandatoryPage.month()).setValue(1);
    await click(DateNonMandatoryPage.submit());

    // Then an error message is shown
    await expect(await $(DateNonMandatoryPage.errorNumber(1)).getText()).toBe("Enter a valid date");
  });

  it("Given the test_dates survey is selected, when a user clicks the day label then the day subfield should gain the focus", async () => {
    await $(DateRangePage.dateRangeFromday()).setValue(1);
    await $(DateRangePage.dateRangeFrommonth()).setValue(1);
    await $(DateRangePage.dateRangeFromyear()).setValue(2016);
    await $(DateRangePage.dateRangeToday()).setValue(1);
    await $(DateRangePage.dateRangeTomonth()).setValue(1);
    await $(DateRangePage.dateRangeToyear()).setValue(2017);
    await click(DateRangePage.submit());

    await $(DateMonthYearPage.Month()).setValue(1);
    await $(DateMonthYearPage.Year()).setValue(2016);
    await click(DateMonthYearPage.submit());

    // When a user clicks the day label
    await $(DateSinglePage.dayLabel()).click();

    // Then the day subfield should gain the focus
    await expect(await $(DateSinglePage.day()).isFocused()).toBe(true);
  });
});
