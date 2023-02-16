import DateRangePage from "../generated_pages/dates/date-range-block.page";
import DateMonthYearPage from "../generated_pages/dates/date-month-year-block.page";
import DateSinglePage from "../generated_pages/dates/date-single-block.page";
import DateNonMandatoryPage from "../generated_pages/dates/date-non-mandatory-block.page";
import DateYearDatePage from "../generated_pages/dates/date-year-date-block.page";
import SubmitPage from "../generated_pages/dates/submit.page";

describe("Date checks", () => {
  beforeEach("Load the survey", async ()=> {
    await browser.openQuestionnaire("test_dates.json");
  });

  it("Given an answer label is provided for a date question then the label should be displayed ", async ()=> {
    await expect(await $(await DateRangePage.legend()).getText()).to.contain("Period from");
  });

  it("Given an answer label is not provided for a date question then the question title should be used within the legend ", async ()=> {
    await $(await DateRangePage.dateRangeFromday()).setValue(1);
    await $(await DateRangePage.dateRangeFrommonth()).setValue(1);
    await $(await DateRangePage.dateRangeFromyear()).setValue(1901);

    await $(await DateRangePage.dateRangeToday()).setValue(3);
    await $(await DateRangePage.dateRangeTomonth()).setValue(5);
    await $(await DateRangePage.dateRangeToyear()).setValue(2017);

    await $(await DateRangePage.submit()).click();

    await expect(await $(await DateMonthYearPage.legend()).getText()).to.contain("Date with month and year");
  });

  it("Given the test_dates survey is selected when dates are entered then the summary screen shows the dates entered formatted", async ()=> {
    // When dates are entered
    await $(await DateRangePage.dateRangeFromday()).setValue(1);
    await $(await DateRangePage.dateRangeFrommonth()).setValue(1);
    await $(await DateRangePage.dateRangeFromyear()).setValue(1901);

    await $(await DateRangePage.dateRangeToday()).setValue(3);
    await $(await DateRangePage.dateRangeTomonth()).setValue(5);
    await $(await DateRangePage.dateRangeToyear()).setValue(2017);

    await $(await DateRangePage.submit()).click();

    await $(await DateMonthYearPage.Month()).setValue(4);
    await $(await DateMonthYearPage.Year()).setValue(2018);

    await $(await DateMonthYearPage.submit()).click();

    await $(await DateSinglePage.day()).setValue(4);
    await $(await DateSinglePage.month()).setValue(1);
    await $(await DateSinglePage.year()).setValue(1999);

    await $(await DateSinglePage.submit()).click();

    await $(await DateNonMandatoryPage.submit()).click();

    await $(await DateYearDatePage.Year()).setValue(2005);

    await $(await DateYearDatePage.submit()).click();

    await expect(browser.getUrl()).to.contain(SubmitPage.pageName);

    // Then the summary screen shows the dates entered formatted
    await expect(await $(await SubmitPage.dateRangeFromAnswer()).getText()).to.contain("1 January 1901 to 3 May 2017");
    await expect(await $(await SubmitPage.monthYearAnswer()).getText()).to.contain("April 2018");
    await expect(await $(await SubmitPage.singleDateAnswer()).getText()).to.contain("4 January 1999");
    await expect(await $(await SubmitPage.nonMandatoryDateAnswer()).getText()).to.contain("No answer provided");
    await expect(await $(await SubmitPage.yearDateAnswer()).getText()).to.contain("2005");
  });

  it("Given the test_dates survey is selected when the from date is greater than the to date then an error message is shown", async ()=> {
    // When the from date is greater than the to date
    await $(await DateRangePage.dateRangeFromday()).setValue(1);
    await $(await DateRangePage.dateRangeFrommonth()).setValue(1);
    await $(await DateRangePage.dateRangeFromyear()).setValue(2016);

    await $(await DateRangePage.dateRangeToday()).setValue(1);
    await $(await DateRangePage.dateRangeTomonth()).setValue(1);
    await $(await DateRangePage.dateRangeToyear()).setValue(2015);

    await $(await DateRangePage.submit()).click();

    // Then an error message is shown and the question panel is highlighted
    await expect(await $(await DateRangePage.errorNumber(1)).getText()).to.contain("Enter a 'period to' date later than the 'period from' date");
    await expect(await $(await DateRangePage.dateRangeQuestionErrorPanel()).isExisting()).to.be.true;

    // Then clicking error should focus on first input field
    await $(await DateRangePage.errorNumber(1)).click();
    await expect(await $(await DateRangePage.dateRangeFromday()).isFocused()).to.be.true;
  });

  it("Given the test_dates survey is selected when the from date and the to date are the same then an error message is shown", async ()=> {
    // When the from date is greater than the to date
    await $(await DateRangePage.dateRangeFromday()).setValue(1);
    await $(await DateRangePage.dateRangeFrommonth()).setValue(1);
    await $(await DateRangePage.dateRangeFromyear()).setValue(2016);

    await $(await DateRangePage.dateRangeToday()).setValue(1);
    await $(await DateRangePage.dateRangeTomonth()).setValue(1);
    await $(await DateRangePage.dateRangeToyear()).setValue(2016);

    await $(await DateRangePage.submit()).click();

    // Then an error message is shown and the question panel is highlighted
    await expect(await $(await DateRangePage.errorNumber(1)).getText()).to.contain("Enter a 'period to' date later than the 'period from' date");
    await expect(await $(await DateRangePage.dateRangeQuestionErrorPanel()).isExisting()).to.be.true;
  });

  it("Given the test_dates survey is selected when an invalid date is entered in a date range then an error message is shown", async ()=> {
    // When the from date is greater than the to date
    await $(await DateRangePage.dateRangeFromday()).setValue(1);
    await $(await DateRangePage.dateRangeFrommonth()).setValue(1);
    await $(await DateRangePage.dateRangeFromyear()).setValue(2016);

    await $(await DateRangePage.dateRangeToday()).setValue(1);
    await $(await DateRangePage.dateRangeTomonth()).setValue(1);
    await $(await DateRangePage.dateRangeToyear()).setValue("");

    await $(await DateRangePage.submit()).click();

    // Then an error message is shown
    await expect(await $(await DateRangePage.errorNumber(1)).getText()).to.contain("Enter a valid date");
  });

  it("Given the test_dates survey is selected when the year (month year type) is left empty then an error message is shown", async ()=> {
    await $(await DateRangePage.dateRangeFromday()).setValue(1);
    await $(await DateRangePage.dateRangeFrommonth()).setValue(1);
    await $(await DateRangePage.dateRangeFromyear()).setValue(2016);
    await $(await DateRangePage.dateRangeToday()).setValue(1);
    await $(await DateRangePage.dateRangeTomonth()).setValue(1);
    await $(await DateRangePage.dateRangeToyear()).setValue(2017);
    await $(await DateRangePage.submit()).click();

    // When the year (month year type) is left empty
    await $(await DateMonthYearPage.Month()).setValue(4);
    await $(await DateMonthYearPage.Year()).setValue("");

    await $(await DateMonthYearPage.submit()).click();

    // Then an error message is shown
    await expect(await $(await DateMonthYearPage.errorNumber(1)).getText()).to.contain("Enter a valid date");
  });

  it("Given the test_dates survey is selected, " + "When an error message is shown and it is corrected, " + "Then the next question is displayed", async ()=> {
    await $(await DateRangePage.dateRangeFromday()).setValue(1);
    await $(await DateRangePage.dateRangeFrommonth()).setValue(1);
    await $(await DateRangePage.dateRangeFromyear()).setValue(2016);
    await $(await DateRangePage.dateRangeToday()).setValue(1);
    await $(await DateRangePage.dateRangeTomonth()).setValue(1);
    await $(await DateRangePage.dateRangeToyear()).setValue(2017);
    await $(await DateRangePage.submit()).click();

    // When an error message is shown
    await $(await DateMonthYearPage.Month()).setValue(4);
    await $(await DateMonthYearPage.Year()).setValue("");
    await $(await DateMonthYearPage.submit()).click();

    await expect(await $(await DateMonthYearPage.error()).getText()).to.contain("Enter a valid date");

    // Then when it is corrected, it goes to the next question
    await $(await DateMonthYearPage.Year()).setValue(2018);
    await $(await DateMonthYearPage.submit()).click();

    await expect(browser.getUrl()).to.contain(DateSinglePage.url());
  });

  it("Given the test_dates survey is selected when an error message is shown then when it is corrected, it goes to the summary page and the information is correct", async ()=> {
    await $(await DateRangePage.dateRangeFromday()).setValue(1);
    await $(await DateRangePage.dateRangeFrommonth()).setValue(1);
    await $(await DateRangePage.dateRangeFromyear()).setValue(2016);
    await $(await DateRangePage.dateRangeToday()).setValue(1);
    await $(await DateRangePage.dateRangeTomonth()).setValue(1);
    await $(await DateRangePage.dateRangeToyear()).setValue(2017);
    await $(await DateRangePage.submit()).click();

    await $(await DateMonthYearPage.Month()).setValue(1);
    await $(await DateMonthYearPage.Year()).setValue(2016);
    await $(await DateMonthYearPage.submit()).click();

    await $(await DateSinglePage.day()).setValue(1);
    await $(await DateSinglePage.month()).setValue(1);
    await $(await DateSinglePage.year()).setValue(2016);
    await $(await DateMonthYearPage.submit()).click();

    // When non-mandatory is partially completed
    await $(await DateNonMandatoryPage.day()).setValue(4);
    await $(await DateNonMandatoryPage.month()).setValue(1);
    await $(await DateNonMandatoryPage.submit()).click();

    // Then an error message is shown
    await expect(await $(await DateNonMandatoryPage.errorNumber(1)).getText()).to.contain("Enter a valid date");
  });

  it("Given the test_dates survey is selected, when a user clicks the day label then the day subfield should gain the focus", async ()=> {
    await $(await DateRangePage.dateRangeFromday()).setValue(1);
    await $(await DateRangePage.dateRangeFrommonth()).setValue(1);
    await $(await DateRangePage.dateRangeFromyear()).setValue(2016);
    await $(await DateRangePage.dateRangeToday()).setValue(1);
    await $(await DateRangePage.dateRangeTomonth()).setValue(1);
    await $(await DateRangePage.dateRangeToyear()).setValue(2017);
    await $(await DateRangePage.submit()).click();

    await $(await DateMonthYearPage.Month()).setValue(1);
    await $(await DateMonthYearPage.Year()).setValue(2016);
    await $(await DateMonthYearPage.submit()).click();

    // When a user clicks the day label
    await $(await DateSinglePage.dayLabel()).click();

    // Then the day subfield should gain the focus
    await expect(await $(await DateSinglePage.day()).isFocused()).to.be.true;
  });
});
