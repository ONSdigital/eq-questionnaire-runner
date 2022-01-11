import AgeBlockYearPage from "../generated_pages/difference_in_years/age-block.page";
import AgeBlockMonthYearPage from "../generated_pages/difference_in_years_month_year/age-block.page";
import AgeBlockDayMonthYearRangePage from "../generated_pages/difference_in_years_range/date-block.page";
import AgeBlockMonthYearRangePage from "../generated_pages/difference_in_years_month_year_range/date-block.page";

describe("Difference check (years)", () => {
  before("Load the survey", () => {
    browser.openQuestionnaire("test_difference_in_years.json");
  });

  it("Given a day, month and year answer is provided for a date question then the age in years should be calculated and displayed on the page ", () => {
    $(AgeBlockYearPage.day()).setValue(1);
    $(AgeBlockYearPage.month()).setValue(1);
    $(AgeBlockYearPage.year()).setValue(1990);
    $(AgeBlockYearPage.submit()).click();

    const expectedPageTitle = browser.getTitle();
    expect(expectedPageTitle).to.equal("You are … old. Is this correct? - Difference between two dates");
  });
});

describe("Difference check (months and years)", () => {
  before("Load the survey", () => {
    browser.openQuestionnaire("test_difference_in_years_month_year.json");
  });

  it("Given a month and year answer is provided for a date question then the difference in years should be calculated and displayed on the page ", () => {
    $(AgeBlockMonthYearPage.Month()).setValue(1);
    $(AgeBlockMonthYearPage.Year()).setValue(1990);

    $(AgeBlockMonthYearPage.submit()).click();

    const expectedPageTitle = browser.getTitle();
    expect(expectedPageTitle).to.equal("It has been … since you last went on holiday. Is this correct? - Difference between two dates");
  });
});

describe("Difference check (months and years range)", () => {
  before("Load the survey", () => {
    browser.openQuestionnaire("test_difference_in_years_month_year_range.json");
  });

  it("Given a month and year answers 'from' and 'to' are provided for a date question then the difference in years should be calculated and displayed on the page ", () => {
    $(AgeBlockMonthYearRangePage.periodFromMonth()).setValue(1);
    $(AgeBlockMonthYearRangePage.periodFromYear()).setValue(1990);
    $(AgeBlockMonthYearRangePage.periodToMonth()).setValue(1);
    $(AgeBlockMonthYearRangePage.periodToYear()).setValue(1991);

    $(AgeBlockMonthYearRangePage.submit()).click();

    expect($("body").getText()).to.have.string("You were out of the UK for 1 year. Is this correct?");
  });
});

describe("Difference check (years range)", () => {
  before("Load the survey", () => {
    browser.openQuestionnaire("test_difference_in_years_range.json");
  });

  it("Given a day, month and year answers 'from' and 'to' are provided for a date question then the difference in years should be calculated and displayed on the page ", () => {
    $(AgeBlockDayMonthYearRangePage.periodFromday()).setValue(1);
    $(AgeBlockDayMonthYearRangePage.periodFrommonth()).setValue(1);
    $(AgeBlockDayMonthYearRangePage.periodFromyear()).setValue(1990);

    $(AgeBlockDayMonthYearRangePage.periodToday()).setValue(1);
    $(AgeBlockDayMonthYearRangePage.periodTomonth()).setValue(1);
    $(AgeBlockDayMonthYearRangePage.periodToyear()).setValue(1991);

    $(AgeBlockDayMonthYearRangePage.submit()).click();

    expect($("body").getText()).to.have.string("You were out of the UK for 1 year. Is this correct?");
  });
});
