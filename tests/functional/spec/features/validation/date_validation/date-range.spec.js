import DateRangePage from "../../../../generated_pages/date_validation_range/date-range-block.page";
import SubmitPage from "../../../../generated_pages/date_validation_range/submit.page";
import { click } from "../../../../helpers";
describe("Feature: Question level validation for date ranges", () => {
  beforeEach(async () => {
    await browser.openQuestionnaire("test_date_validation_range.json");
  });

  describe("Period Validation", () => {
    describe("Given I enter a date period greater than the max period limit", () => {
      it("When I continue, Then I should see a period validation error", async () => {
        await $(DateRangePage.dateRangeFromday()).setValue(1);
        await $(DateRangePage.dateRangeFrommonth()).setValue(1);
        await $(DateRangePage.dateRangeFromyear()).setValue(2018);

        await $(DateRangePage.dateRangeToday()).setValue(3);
        await $(DateRangePage.dateRangeTomonth()).setValue(3);
        await $(DateRangePage.dateRangeToyear()).setValue(2018);
        await click(DateRangePage.submit());
        await expect(await $(DateRangePage.errorNumber(1)).getText()).toBe("Enter a reporting period less than or equal to 1 month, 20 days");
      });
    });

    describe("Given I enter a date period less than the min period limit", () => {
      it("When I continue, Then I should see a period validation error", async () => {
        await $(DateRangePage.dateRangeFromday()).setValue(1);
        await $(DateRangePage.dateRangeFrommonth()).setValue(1);
        await $(DateRangePage.dateRangeFromyear()).setValue(2018);

        await $(DateRangePage.dateRangeToday()).setValue(3);
        await $(DateRangePage.dateRangeTomonth()).setValue(1);
        await $(DateRangePage.dateRangeToyear()).setValue(2018);
        await click(DateRangePage.submit());
        await expect(await $(DateRangePage.errorNumber(1)).getText()).toBe("Enter a reporting period greater than or equal to 23 days");
      });
    });

    describe("Given I enter a date period within the set period limits", () => {
      it("When I continue, Then I should be able to reach the summary", async () => {
        await $(DateRangePage.dateRangeFromday()).setValue(1);
        await $(DateRangePage.dateRangeFrommonth()).setValue(1);
        await $(DateRangePage.dateRangeFromyear()).setValue(2018);

        await $(DateRangePage.dateRangeToday()).setValue(3);
        await $(DateRangePage.dateRangeTomonth()).setValue(2);
        await $(DateRangePage.dateRangeToyear()).setValue(2018);
        await click(DateRangePage.submit());
        await expect(browser).toHaveUrlContaining(SubmitPage.pageName);
      });
    });
  });

  describe("Date Range Validation", () => {
    describe('Given I enter a "to date" which is earlier than the "from date"', () => {
      it("When I continue, Then I should see a validation error", async () => {
        await $(DateRangePage.dateRangeFromday()).setValue(1);
        await $(DateRangePage.dateRangeFrommonth()).setValue(2);
        await $(DateRangePage.dateRangeFromyear()).setValue(2018);

        await $(DateRangePage.dateRangeToday()).setValue(3);
        await $(DateRangePage.dateRangeTomonth()).setValue(1);
        await $(DateRangePage.dateRangeToyear()).setValue(2018);
        await click(DateRangePage.submit());
        await expect(await $(DateRangePage.errorNumber(1)).getText()).toBe("Enter a 'period to' date later than the 'period from' date");
      });
    });

    describe('Given I enter matching dates for the "from" and "to" dates', () => {
      it("When I continue, Then I should see a validation error", async () => {
        await $(DateRangePage.dateRangeFromday()).setValue(1);
        await $(DateRangePage.dateRangeFrommonth()).setValue(1);
        await $(DateRangePage.dateRangeFromyear()).setValue(2018);

        await $(DateRangePage.dateRangeToday()).setValue(1);
        await $(DateRangePage.dateRangeTomonth()).setValue(1);
        await $(DateRangePage.dateRangeToyear()).setValue(2018);
        await click(DateRangePage.submit());
        await expect(await $(DateRangePage.errorNumber(1)).getText()).toBe("Enter a 'period to' date later than the 'period from' date");
      });
    });

    describe("Given I enter a valid date range", () => {
      it("When I continue, Then I should be able to reach the summary", async () => {
        await $(DateRangePage.dateRangeFromday()).setValue(1);
        await $(DateRangePage.dateRangeFrommonth()).setValue(1);
        await $(DateRangePage.dateRangeFromyear()).setValue(2018);

        await $(DateRangePage.dateRangeToday()).setValue(3);
        await $(DateRangePage.dateRangeTomonth()).setValue(2);
        await $(DateRangePage.dateRangeToyear()).setValue(2018);
        await click(DateRangePage.submit());
        await expect(browser).toHaveUrlContaining(SubmitPage.pageName);
      });
    });
  });
});
