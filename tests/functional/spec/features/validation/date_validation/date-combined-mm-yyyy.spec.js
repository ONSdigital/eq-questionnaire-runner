import DateRangePage from "../../../../generated_pages/date_validation_mm_yyyy_combined/date-range-block.page";
import SubmitPage from "../../../../generated_pages/date_validation_mm_yyyy_combined/submit.page";
import { click } from "../../../../helpers";
describe("Feature: Combined question level and single validation for MM-YYYY dates", () => {
  before(async () => {
    await browser.openQuestionnaire("test_date_validation_mm_yyyy_combined.json");
  });

  describe("Period Validation", () => {
    describe("Given I enter dates", () => {
      it("When I enter a month but no year, Then I should see only a single invalid date error", async () => {
        await $(DateRangePage.dateRangeFromYear()).setValue(2018);

        await $(DateRangePage.dateRangeToMonth()).setValue(4);
        await $(DateRangePage.dateRangeToYear()).setValue(2017);
        await click(DateRangePage.submit());
        await expect(await $(DateRangePage.errorNumber(1)).getText()).toContain("Enter a valid date");
        await expect(await $(DateRangePage.errorNumber(2)).isExisting()).toBe(false);
      });

      it("When I enter a year but no month, Then I should see only a single invalid date error", async () => {
        await $(DateRangePage.dateRangeFromMonth()).setValue(10);
        await $(DateRangePage.dateRangeFromYear()).setValue("");

        await $(DateRangePage.dateRangeToMonth()).setValue(4);
        await $(DateRangePage.dateRangeToYear()).setValue(2017);
        await click(DateRangePage.submit());
        await expect(await $(DateRangePage.errorNumber(1)).getText()).toContain("Enter a valid date");
        await expect(await $(DateRangePage.errorNumber(2)).isExisting()).toBe(false);
      });

      it("When I enter a year of 0, Then I should see only a single invalid date error", async () => {
        await $(DateRangePage.dateRangeFromMonth()).setValue(10);
        await $(DateRangePage.dateRangeFromYear()).setValue(0);

        await $(DateRangePage.dateRangeToMonth()).setValue(4);
        await $(DateRangePage.dateRangeToYear()).setValue(2017);
        await click(DateRangePage.submit());
        await expect(await $(DateRangePage.errorNumber(1)).getText()).toContain("Enter the year in a valid format. For example, 2023.");
        await expect(await $(DateRangePage.errorNumber(2)).isExisting()).toBe(false);
      });

      it("When I enter a single dates that are too early/late, Then I should see a single validation errors", async () => {
        await $(DateRangePage.dateRangeFromMonth()).setValue(10);
        await $(DateRangePage.dateRangeFromYear()).setValue(2016);

        await $(DateRangePage.dateRangeToMonth()).setValue(6);
        await $(DateRangePage.dateRangeToYear()).setValue(2017);
        await click(DateRangePage.submit());
        await expect(await $(DateRangePage.errorNumber(1)).getText()).toContain("Enter a date after November 2016");
        await expect(await $(DateRangePage.errorNumber(2)).getText()).toContain("Enter a date before June 2017");
      });

      it("When I enter a range too large, Then I should see a range validation error", async () => {
        await $(DateRangePage.dateRangeFromMonth()).setValue(12);
        await $(DateRangePage.dateRangeFromYear()).setValue(2016);

        await $(DateRangePage.dateRangeToMonth()).setValue(5);
        await $(DateRangePage.dateRangeToYear()).setValue(2017);
        await click(DateRangePage.submit());
        await expect(await $(DateRangePage.errorNumber(1)).getText()).toContain("Enter a reporting period less than or equal to 3 months");
      });

      it("When I enter a range too small, Then I should see a range validation error", async () => {
        await $(DateRangePage.dateRangeFromMonth()).setValue(12);
        await $(DateRangePage.dateRangeFromYear()).setValue(2016);

        await $(DateRangePage.dateRangeToMonth()).setValue(1);
        await $(DateRangePage.dateRangeToYear()).setValue(2017);
        await click(DateRangePage.submit());
        await expect(await $(DateRangePage.errorNumber(1)).getText()).toContain("Enter a reporting period greater than or equal to 2 months");
      });

      it("When I enter valid dates, Then I should see the summary page", async () => {
        await $(DateRangePage.dateRangeFromMonth()).setValue(1);
        await $(DateRangePage.dateRangeFromYear()).setValue(2017);

        // Min range
        await $(DateRangePage.dateRangeToMonth()).setValue(3);
        await $(DateRangePage.dateRangeToYear()).setValue(2017);
        await click(DateRangePage.submit());
        await expect(await $(SubmitPage.dateRangeFrom()).getText()).toContain("January 2017 to March 2017");

        // Max range
        await $(SubmitPage.dateRangeFromEdit()).click();
        await $(DateRangePage.dateRangeToMonth()).setValue(4);
        await $(DateRangePage.dateRangeToYear()).setValue(2017);
        await click(DateRangePage.submit());
        await expect(await $(SubmitPage.dateRangeFrom()).getText()).toContain("January 2017 to April 2017");
      });
    });
  });
});
