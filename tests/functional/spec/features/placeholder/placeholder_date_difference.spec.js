import AgeBlockYearPage from "../../../generated_pages/placeholder_difference_in_years/age-block.page";
import AgeTestYearPage from "../../../generated_pages/placeholder_difference_in_years/age-test.page";
import AgeBlockMonthYearPage from "../../../generated_pages/placeholder_difference_in_years_month_year/age-block.page";
import AgeTestMonthYearPage from "../../../generated_pages/placeholder_difference_in_years_month_year/age-test.page";
import AgeBlockDayMonthYearRangePage from "../../../generated_pages/placeholder_difference_in_years_range/date-block.page";
import AgeTestDayMonthYearRangePage from "../../../generated_pages/placeholder_difference_in_years_range/age-test.page";
import AgeBlockMonthYearRangePage from "../../../generated_pages/placeholder_difference_in_years_month_year_range/date-block.page";
import AgeTestMonthYearRangePage from "../../../generated_pages/placeholder_difference_in_years_month_year_range/age-test.page";
import { click } from "../../../helpers";
describe("Difference check (years)", () => {
  before("Load the survey", async () => {
    await browser.openQuestionnaire("test_placeholder_difference_in_years.json");
  });

  it("Given a day, month and year answer is provided for a date question then the age in years should be calculated and displayed on the page ", async () => {
    await $(AgeBlockYearPage.day()).setValue(1);
    await $(AgeBlockYearPage.month()).setValue(1);
    await $(AgeBlockYearPage.year()).setValue(1990);
    await click(AgeBlockYearPage.submit());
    await expect(await $(AgeTestYearPage.heading()).getText()).toBe(`You are ${getYears("1990/01/01")} years old. Is this correct?`);
  });
});

describe("Difference check (months and years)", () => {
  before("Load the survey", async () => {
    await browser.openQuestionnaire("test_placeholder_difference_in_years_month_year.json");
  });

  it("Given a month and year answer is provided for a date question then the difference in years should be calculated and displayed on the page ", async () => {
    await $(AgeBlockMonthYearPage.Month()).setValue(1);
    await $(AgeBlockMonthYearPage.Year()).setValue(1990);

    await click(AgeBlockMonthYearPage.submit());

    await expect(await $(AgeTestMonthYearPage.heading()).getText()).toBe(
      `It has been ${getYears("1990/01/01")} years since you last went on holiday. Is this correct?`,
    );
  });
});

describe("Difference check (months and years range)", () => {
  before("Load the survey", async () => {
    await browser.openQuestionnaire("test_placeholder_difference_in_years_month_year_range.json");
  });

  it("Given a month and year answers 'from' and 'to' are provided for a date question then the difference in years should be calculated and displayed on the page ", async () => {
    await $(AgeBlockMonthYearRangePage.periodFromMonth()).setValue(1);
    await $(AgeBlockMonthYearRangePage.periodFromYear()).setValue(1990);
    await $(AgeBlockMonthYearRangePage.periodToMonth()).setValue(1);
    await $(AgeBlockMonthYearRangePage.periodToYear()).setValue(1991);

    await click(AgeBlockMonthYearRangePage.submit());

    await expect(await $(AgeTestMonthYearRangePage.heading()).getText()).toBe("You were out of the UK for 1 year. Is this correct?");
  });
});

describe("Difference check (years range)", () => {
  before("Load the survey", async () => {
    await browser.openQuestionnaire("test_placeholder_difference_in_years_range.json");
  });

  it("Given a day, month and year answers 'from' and 'to' are provided for a date question then the difference in years should be calculated and displayed on the page ", async () => {
    await $(AgeBlockDayMonthYearRangePage.periodFromday()).setValue(1);
    await $(AgeBlockDayMonthYearRangePage.periodFrommonth()).setValue(1);
    await $(AgeBlockDayMonthYearRangePage.periodFromyear()).setValue(1990);

    await $(AgeBlockDayMonthYearRangePage.periodToday()).setValue(1);
    await $(AgeBlockDayMonthYearRangePage.periodTomonth()).setValue(1);
    await $(AgeBlockDayMonthYearRangePage.periodToyear()).setValue(1991);

    await click(AgeBlockDayMonthYearRangePage.submit());

    await expect(await $(AgeTestDayMonthYearRangePage.heading()).getText()).toBe("You were out of the UK for 1 year. Is this correct?");
  });
});

function getYears(date) {
  return new Date(new Date() - new Date(date)).getFullYear() - 1970;
}
