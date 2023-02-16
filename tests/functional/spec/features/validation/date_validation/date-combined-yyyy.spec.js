import DateRangePage from "../../../../generated_pages/date_validation_yyyy_combined/date-range-block.page";
import SubmitPage from "../../../../generated_pages/date_validation_yyyy_combined/submit.page";

describe("Feature: Combined question level and single validation for MM-YYYY dates", () => {
  before(async ()=> {
    await browser.openQuestionnaire("test_date_validation_yyyy_combined.json");
  });

  describe("Period Validation", () => {
    describe("Given I enter dates", () => {
      it("When I enter dates that are too early and too late, Then I should see two validation errors", async ()=> {
        await $(await DateRangePage.dateRangeFromYear()).setValue(2015);
        await $(await DateRangePage.dateRangeToYear()).setValue(2021);
        await $(await DateRangePage.submit()).click();
        await expect(await $(await DateRangePage.errorNumber(1)).getText()).to.contain("Enter a date after 2015");
        await expect(await $(await DateRangePage.errorNumber(2)).getText()).to.contain("Enter a date before 2021");
      });

      it("When I enter a range too large, Then I should see a range validation error", async ()=> {
        await $(await DateRangePage.dateRangeFromYear()).setValue(2016);
        await $(await DateRangePage.dateRangeToYear()).setValue(2020);
        await $(await DateRangePage.submit()).click();
        await expect(await $(await DateRangePage.errorNumber(1)).getText()).to.contain("Enter a reporting period less than or equal to 3 years");
      });

      it("When I enter a range too small, Then I should see a range validation error", async ()=> {
        await $(await DateRangePage.dateRangeFromYear()).setValue(2016);
        await $(await DateRangePage.dateRangeToYear()).setValue(2017);
        await $(await DateRangePage.submit()).click();
        await expect(await $(await DateRangePage.errorNumber(1)).getText()).to.contain("Enter a reporting period greater than or equal to 2 years");
      });

      it("When I enter valid dates, Then I should see the summary page", async ()=> {
        await $(await DateRangePage.dateRangeFromYear()).setValue(2016);
        // Min range
        await $(await DateRangePage.dateRangeToYear()).setValue(2018);
        await $(await DateRangePage.submit()).click();
        await expect(await $(await SubmitPage.dateRangeFrom()).getText()).to.contain("2016 to 2018");

        // Max range
        await $(await SubmitPage.dateRangeFromEdit()).click();
        await $(await DateRangePage.dateRangeToYear()).setValue(2019);
        await $(await DateRangePage.submit()).click();
        await expect(await $(await SubmitPage.dateRangeFrom()).getText()).to.contain("2016 to 2019");
      });
    });
  });
});
