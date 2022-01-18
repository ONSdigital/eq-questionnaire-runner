import AgeBlockYearPage from "../../../generated_pages/placeholder_difference_in_years/age-block.page";
import AgeTestYearPage from "../../../generated_pages/placeholder_difference_in_years/age-test.page";
import AgeBlockMonthYearPage from "../../../generated_pages/placeholder_difference_in_years_month_year/age-block.page";
import AgeTestMonthYearPage from "../../../generated_pages/placeholder_difference_in_years_month_year/age-test.page";
import AgeBlockDayMonthYearRangePage from "../../../generated_pages/placeholder_difference_in_years_range/date-block.page";
import AgeTestDayMonthYearRangePage from "../../../generated_pages/placeholder_difference_in_years_range/age-test.page";
import AgeBlockMonthYearRangePage from "../../../generated_pages/placeholder_difference_in_years_month_year_range/date-block.page";
import AgeTestMonthYearRangePage from "../../../generated_pages/placeholder_difference_in_years_month_year_range/age-test.page";

describe("Difference check (years)", () => {
  before("Load the survey", () => {
    browser.openQuestionnaire("test_placeholder_difference_in_years.json");
  });

  it("Given a day, month and year answer is provided for a date question then the age in years should be calculated and displayed on the page ", () => {
    $(AgeBlockYearPage.day()).setValue(1);
    $(AgeBlockYearPage.month()).setValue(1);
    $(AgeBlockYearPage.year()).setValue(1990);
    $(AgeBlockYearPage.submit()).click();
    expect($(AgeTestYearPage.heading()).getText()).to.equal(`You are ${getYears("1990/01/01")} years old. Is this correct?`);
  });
});

describe("Difference check (months and years)", () => {
  before("Load the survey", () => {
    browser.openQuestionnaire("test_placeholder_difference_in_years_month_year.json");
  });

  it("Given a month and year answer is provided for a date question then the difference in years should be calculated and displayed on the page ", () => {
    $(AgeBlockMonthYearPage.Month()).setValue(1);
    $(AgeBlockMonthYearPage.Year()).setValue(1990);

    $(AgeBlockMonthYearPage.submit()).click();

    expect($(AgeTestMonthYearPage.heading()).getText()).to.equal(
      `It has been ${getYears("1990/01/01")} years since you last went on holiday. Is this correct?`
    );
  });
});

describe("Difference check (months and years range)", () => {
  before("Load the survey", () => {
    browser.openQuestionnaire("test_placeholder_difference_in_years_month_year_range.json");
  });

  it("Given a month and year answers 'from' and 'to' are provided for a date question then the difference in years should be calculated and displayed on the page ", () => {
    $(AgeBlockMonthYearRangePage.periodFromMonth()).setValue(1);
    $(AgeBlockMonthYearRangePage.periodFromYear()).setValue(1990);
    $(AgeBlockMonthYearRangePage.periodToMonth()).setValue(1);
    $(AgeBlockMonthYearRangePage.periodToYear()).setValue(1991);

    $(AgeBlockMonthYearRangePage.submit()).click();

    expect($(AgeTestMonthYearRangePage.heading()).getText()).to.have.string("You were out of the UK for 1 year. Is this correct?");
  });
});

describe("Difference check (years range)", () => {
  before("Load the survey", () => {
    browser.openQuestionnaire("test_placeholder_difference_in_years_range.json");
  });

  it("Given a day, month and year answers 'from' and 'to' are provided for a date question then the difference in years should be calculated and displayed on the page ", () => {
    $(AgeBlockDayMonthYearRangePage.periodFromday()).setValue(1);
    $(AgeBlockDayMonthYearRangePage.periodFrommonth()).setValue(1);
    $(AgeBlockDayMonthYearRangePage.periodFromyear()).setValue(1990);

    $(AgeBlockDayMonthYearRangePage.periodToday()).setValue(1);
    $(AgeBlockDayMonthYearRangePage.periodTomonth()).setValue(1);
    $(AgeBlockDayMonthYearRangePage.periodToyear()).setValue(1991);

    $(AgeBlockDayMonthYearRangePage.submit()).click();

    expect($(AgeTestDayMonthYearRangePage.heading()).getText()).to.have.string("You were out of the UK for 1 year. Is this correct?");
  });
});

function getYears(date) {
  return new Date(new Date() - new Date(date)).getFullYear() - 1970;
}
