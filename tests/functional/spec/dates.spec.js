import DateRangePage from "../generated_pages/dates/date-range-block.page";
import DateMonthYearPage from "../generated_pages/dates/date-month-year-block.page";
import DateSinglePage from "../generated_pages/dates/date-single-block.page";
import DateNonMandatoryPage from "../generated_pages/dates/date-non-mandatory-block.page";
import DateYearDatePage from "../generated_pages/dates/date-year-date-block.page";
import SubmitPage from "../generated_pages/dates/submit.page";

describe("Date checks", () => {
  beforeEach("Load the survey", async () => {
    await browser.openQuestionnaire("test_dates.json");
  });

  it("Given an answer label is provided for a date question then the label should be displayed ", async () => {
    await expect(await $(DateRangePage.legend()).getText()).to.contain("Period from");
  });

  it("Given an answer label is not provided for a date question then the question title should be used within the legend ", async () => {
    await $(DateRangePage.dateRangeFromday()).setValue(1);
    await $(DateRangePage.dateRangeFrommonth()).setValue(1);
    await $(DateRangePage.dateRangeFromyear()).setValue(1901);

    await $(DateRangePage.dateRangeToday()).setValue(3);
    await $(DateRangePage.dateRangeTomonth()).setValue(5);
    await $(DateRangePage.dateRangeToyear()).setValue(2017);

    await $(DateRangePage.submit()).click();

    await expect(await $(DateMonthYearPage.legend()).getText()).to.contain("Date with month and year");
  });

  it("Given the test_dates survey is selected when dates are entered then the summary screen shows the dates entered formatted", async () => {
    // When dates are entered
    await $(DateRangePage.dateRangeFromday()).setValue(1);
    await $(DateRangePage.dateRangeFrommonth()).setValue(1);
    await $(DateRangePage.dateRangeFromyear()).setValue(1901);

    await $(DateRangePage.dateRangeToday()).setValue(3);
    await $(DateRangePage.dateRangeTomonth()).setValue(5);
    await $(DateRangePage.dateRangeToyear()).setValue(2017);

    await $(DateRangePage.submit()).click();

    await $(DateMonthYearPage.Month()).setValue(4);
    await $(DateMonthYearPage.Year()).setValue(2018);

    await $(DateMonthYearPage.submit()).click();

    await $(DateSinglePage.day()).setValue(4);
    await $(DateSinglePage.month()).setValue(1);
    await $(DateSinglePage.year()).setValue(1999);

    await $(DateSinglePage.submit()).click();

    await $(DateNonMandatoryPage.submit()).click();

    await $(DateYearDatePage.Year()).setValue(2005);

    await $(DateYearDatePage.submit()).click();

    await expect(await browser.getUrl()).to.contain(SubmitPage.pageName);

    // Then the summary screen shows the dates entered formatted
    await expect(await $(SubmitPage.dateRangeFromAnswer()).getText()).to.contain("1 January 1901 to 3 May 2017");
    await expect(await $(SubmitPage.monthYearAnswer()).getText()).to.contain("April 2018");
    await expect(await $(SubmitPage.singleDateAnswer()).getText()).to.contain("4 January 1999");
    await expect(await $(SubmitPage.nonMandatoryDateAnswer()).getText()).to.contain("No answer provided");
    await expect(await $(SubmitPage.yearDateAnswer()).getText()).to.contain("2005");
  });

  it("Given the test_dates survey is selected when the from date is greater than the to date then an error message is shown", async () => {
    // When the from date is greater than the to date
    await $(DateRangePage.dateRangeFromday()).setValue(1);
    await $(DateRangePage.dateRangeFrommonth()).setValue(1);
    await $(DateRangePage.dateRangeFromyear()).setValue(2016);

    await $(DateRangePage.dateRangeToday()).setValue(1);
    await $(DateRangePage.dateRangeTomonth()).setValue(1);
    await $(DateRangePage.dateRangeToyear()).setValue(2015);

    await $(DateRangePage.submit()).click();

    // Then an error message is shown and the question panel is highlighted
    await expect(await $(DateRangePage.errorNumber(1)).getText()).to.contain("Enter a 'period to' date later than the 'period from' date");
    await expect(await $(DateRangePage.dateRangeQuestionErrorPanel()).isExisting()).to.be.true;

    // Then clicking error should focus on first input field
    await $(DateRangePage.errorNumber(1)).click();
    await expect(await $(DateRangePage.dateRangeFromday()).isFocused()).to.be.true;
  });

  it("Given the test_dates survey is selected when the from date and the to date are the same then an error message is shown", async () => {
    // When the from date is greater than the to date
    await $(DateRangePage.dateRangeFromday()).setValue(1);
    await $(DateRangePage.dateRangeFrommonth()).setValue(1);
    await $(DateRangePage.dateRangeFromyear()).setValue(2016);

    await $(DateRangePage.dateRangeToday()).setValue(1);
    await $(DateRangePage.dateRangeTomonth()).setValue(1);
    await $(DateRangePage.dateRangeToyear()).setValue(2016);

    await $(DateRangePage.submit()).click();

    // Then an error message is shown and the question panel is highlighted
    await expect(await $(DateRangePage.errorNumber(1)).getText()).to.contain("Enter a 'period to' date later than the 'period from' date");
    await expect(await $(DateRangePage.dateRangeQuestionErrorPanel()).isExisting()).to.be.true;
  });

  it("Given the test_dates survey is selected when an invalid date is entered in a date range then an error message is shown", async () => {
    // When the from date is greater than the to date
    await $(DateRangePage.dateRangeFromday()).setValue(1);
    await $(DateRangePage.dateRangeFrommonth()).setValue(1);
    await $(DateRangePage.dateRangeFromyear()).setValue(2016);

    await $(DateRangePage.dateRangeToday()).setValue(1);
    await $(DateRangePage.dateRangeTomonth()).setValue(1);
    await $(DateRangePage.dateRangeToyear()).setValue("");

    await $(DateRangePage.submit()).click();

    // Then an error message is shown
    await expect(await $(DateRangePage.errorNumber(1)).getText()).to.contain("Enter a valid date");
  });

  it("Given the test_dates survey is selected when the year (month year type) is left empty then an error message is shown", async () => {
    await $(DateRangePage.dateRangeFromday()).setValue(1);
    await $(DateRangePage.dateRangeFrommonth()).setValue(1);
    await $(DateRangePage.dateRangeFromyear()).setValue(2016);
    await $(DateRangePage.dateRangeToday()).setValue(1);
    await $(DateRangePage.dateRangeTomonth()).setValue(1);
    await $(DateRangePage.dateRangeToyear()).setValue(2017);
    await $(DateRangePage.submit()).click();

    // When the year (month year type) is left empty
    await $(DateMonthYearPage.Month()).setValue(4);
    await $(DateMonthYearPage.Year()).setValue("");

    await $(DateMonthYearPage.submit()).click();

    // Then an error message is shown
    await expect(await $(DateMonthYearPage.errorNumber(1)).getText()).to.contain("Enter a valid date");
  });

  it("Given the test_dates survey is selected, " + "When an error message is shown and it is corrected, " + "Then the next question is displayed", async () => {
    await $(DateRangePage.dateRangeFromday()).setValue(1);
    await $(DateRangePage.dateRangeFrommonth()).setValue(1);
    await $(DateRangePage.dateRangeFromyear()).setValue(2016);
    await $(DateRangePage.dateRangeToday()).setValue(1);
    await $(DateRangePage.dateRangeTomonth()).setValue(1);
    await $(DateRangePage.dateRangeToyear()).setValue(2017);
    await $(DateRangePage.submit()).click();

    // When an error message is shown
    await $(DateMonthYearPage.Month()).setValue(4);
    await $(DateMonthYearPage.Year()).setValue("");
    await $(DateMonthYearPage.submit()).click();

    await expect(await $(DateMonthYearPage.error()).getText()).to.contain("Enter a valid date");

    // Then when it is corrected, it goes to the next question
    await $(DateMonthYearPage.Year()).setValue(2018);
    await $(DateMonthYearPage.submit()).click();

    await expect(await browser.getUrl()).to.contain(DateSinglePage.url());
  });

  it("Given the test_dates survey is selected when an error message is shown then when it is corrected, it goes to the summary page and the information is correct", async () => {
    await $(DateRangePage.dateRangeFromday()).setValue(1);
    await $(DateRangePage.dateRangeFrommonth()).setValue(1);
    await $(DateRangePage.dateRangeFromyear()).setValue(2016);
    await $(DateRangePage.dateRangeToday()).setValue(1);
    await $(DateRangePage.dateRangeTomonth()).setValue(1);
    await $(DateRangePage.dateRangeToyear()).setValue(2017);
    await $(DateRangePage.submit()).click();

    await $(DateMonthYearPage.Month()).setValue(1);
    await $(DateMonthYearPage.Year()).setValue(2016);
    await $(DateMonthYearPage.submit()).click();

    await $(DateSinglePage.day()).setValue(1);
    await $(DateSinglePage.month()).setValue(1);
    await $(DateSinglePage.year()).setValue(2016);
    await $(DateMonthYearPage.submit()).click();

    // When non-mandatory is partially completed
    await $(DateNonMandatoryPage.day()).setValue(4);
    await $(DateNonMandatoryPage.month()).setValue(1);
    await $(DateNonMandatoryPage.submit()).click();

    // Then an error message is shown
    await expect(await $(DateNonMandatoryPage.errorNumber(1)).getText()).to.contain("Enter a valid date");
  });

  it("Given the test_dates survey is selected, when a user clicks the day label then the day subfield should gain the focus", async () => {
    await $(DateRangePage.dateRangeFromday()).setValue(1);
    await $(DateRangePage.dateRangeFrommonth()).setValue(1);
    await $(DateRangePage.dateRangeFromyear()).setValue(2016);
    await $(DateRangePage.dateRangeToday()).setValue(1);
    await $(DateRangePage.dateRangeTomonth()).setValue(1);
    await $(DateRangePage.dateRangeToyear()).setValue(2017);
    await $(DateRangePage.submit()).click();

    await $(DateMonthYearPage.Month()).setValue(1);
    await $(DateMonthYearPage.Year()).setValue(2016);
    await $(DateMonthYearPage.submit()).click();

    // When a user clicks the day label
    await $(DateSinglePage.dayLabel()).click();

    // Then the day subfield should gain the focus
    await expect(await $(DateSinglePage.day()).isFocused()).to.be.true;
  });
});
