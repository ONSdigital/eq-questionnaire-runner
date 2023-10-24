import DateRangePage from "../../../../generated_pages/date_validation_yyyy_combined/date-range-block.page";
import SubmitPage from "../../../../generated_pages/date_validation_yyyy_combined/submit.page";
import { click } from "../../../../helpers";
describe("Feature: Combined question level and single validation for MM-YYYY dates", () => {
  before(async () => {
    await browser.openQuestionnaire("test_date_validation_yyyy_combined.json");
  });

  describe("Period Validation", () => {
    describe("Given I enter dates", () => {
      it("When I enter dates that are too early and too late, Then I should see two validation errors", async () => {
        await $(DateRangePage.dateRangeFromYear()).setValue(2015);
        await $(DateRangePage.dateRangeToYear()).setValue(2021);
        await click(DateRangePage.submit());
        await expect(await $(DateRangePage.errorNumber(1)).getText()).toBe("Enter a date after 2015");
        await expect(await $(DateRangePage.errorNumber(2)).getText()).toBe("Enter a date before 2021");
      });

      it("When I enter a range too large, Then I should see a range validation error", async () => {
        await $(DateRangePage.dateRangeFromYear()).setValue(2016);
        await $(DateRangePage.dateRangeToYear()).setValue(2020);
        await click(DateRangePage.submit());
        await expect(await $(DateRangePage.errorNumber(1)).getText()).toBe("Enter a reporting period less than or equal to 3 years");
      });

      it("When I enter a range too small, Then I should see a range validation error", async () => {
        await $(DateRangePage.dateRangeFromYear()).setValue(2016);
        await $(DateRangePage.dateRangeToYear()).setValue(2017);
        await click(DateRangePage.submit());
        await expect(await $(DateRangePage.errorNumber(1)).getText()).toBe("Enter a reporting period greater than or equal to 2 years");
      });

      it("When I enter valid dates, Then I should see the summary page", async () => {
        await $(DateRangePage.dateRangeFromYear()).setValue(2016);
        // Min range
        await $(DateRangePage.dateRangeToYear()).setValue(2018);
        await click(DateRangePage.submit());
        await expect(await $(SubmitPage.dateRangeFrom()).getText()).toBe("2016 to 2018");

        // Max range
        await $(SubmitPage.dateRangeFromEdit()).click();
        await $(DateRangePage.dateRangeToYear()).setValue(2019);
        await click(DateRangePage.submit());
        await expect(await $(SubmitPage.dateRangeFrom()).getText()).toBe("2016 to 2019");
      });
    });
  });
});
