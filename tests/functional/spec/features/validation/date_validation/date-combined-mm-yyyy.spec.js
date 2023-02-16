import DateRangePage from "../../../../generated_pages/date_validation_mm_yyyy_combined/date-range-block.page";
import SubmitPage from "../../../../generated_pages/date_validation_mm_yyyy_combined/submit.page";

describe("Feature: Combined question level and single validation for MM-YYYY dates", () => {
  before(async ()=> {
    await browser.openQuestionnaire("test_date_validation_mm_yyyy_combined.json");
  });

  describe("Period Validation", () => {
    describe("Given I enter dates", () => {
      it("When I enter a month but no year, Then I should see only a single invalid date error", async ()=> {
        await $(await DateRangePage.dateRangeFromYear()).setValue(2018);

        await $(await DateRangePage.dateRangeToMonth()).setValue(4);
        await $(await DateRangePage.dateRangeToYear()).setValue(2017);
        await $(await DateRangePage.submit()).click();
        await expect(await $(await DateRangePage.errorNumber(1)).getText()).to.contain("Enter a valid date");
        await expect(await $(await DateRangePage.errorNumber(2)).isExisting()).to.be.false;
      });

      it("When I enter a year but no month, Then I should see only a single invalid date error", async ()=> {
        await $(await DateRangePage.dateRangeFromMonth()).setValue(10);
        await $(await DateRangePage.dateRangeFromYear()).setValue("");

        await $(await DateRangePage.dateRangeToMonth()).setValue(4);
        await $(await DateRangePage.dateRangeToYear()).setValue(2017);
        await $(await DateRangePage.submit()).click();
        await expect(await $(await DateRangePage.errorNumber(1)).getText()).to.contain("Enter a valid date");
        await expect(await $(await DateRangePage.errorNumber(2)).isExisting()).to.be.false;
      });

      it("When I enter a year of 0, Then I should see only a single invalid date error", async ()=> {
        await $(await DateRangePage.dateRangeFromMonth()).setValue(10);
        await $(await DateRangePage.dateRangeFromYear()).setValue(0);

        await $(await DateRangePage.dateRangeToMonth()).setValue(4);
        await $(await DateRangePage.dateRangeToYear()).setValue(2017);
        await $(await DateRangePage.submit()).click();
        await expect(await $(await DateRangePage.errorNumber(1)).getText()).to.contain("Enter the year in a valid format. For example, 2023.");
        await expect(await $(await DateRangePage.errorNumber(2)).isExisting()).to.be.false;
      });

      it("When I enter a single dates that are too early/late, Then I should see a single validation errors", async ()=> {
        await $(await DateRangePage.dateRangeFromMonth()).setValue(10);
        await $(await DateRangePage.dateRangeFromYear()).setValue(2016);

        await $(await DateRangePage.dateRangeToMonth()).setValue(6);
        await $(await DateRangePage.dateRangeToYear()).setValue(2017);
        await $(await DateRangePage.submit()).click();
        await expect(await $(await DateRangePage.errorNumber(1)).getText()).to.contain("Enter a date after November 2016");
        await expect(await $(await DateRangePage.errorNumber(2)).getText()).to.contain("Enter a date before June 2017");
      });

      it("When I enter a range too large, Then I should see a range validation error", async ()=> {
        await $(await DateRangePage.dateRangeFromMonth()).setValue(12);
        await $(await DateRangePage.dateRangeFromYear()).setValue(2016);

        await $(await DateRangePage.dateRangeToMonth()).setValue(5);
        await $(await DateRangePage.dateRangeToYear()).setValue(2017);
        await $(await DateRangePage.submit()).click();
        await expect(await $(await DateRangePage.errorNumber(1)).getText()).to.contain("Enter a reporting period less than or equal to 3 months");
      });

      it("When I enter a range too small, Then I should see a range validation error", async ()=> {
        await $(await DateRangePage.dateRangeFromMonth()).setValue(12);
        await $(await DateRangePage.dateRangeFromYear()).setValue(2016);

        await $(await DateRangePage.dateRangeToMonth()).setValue(1);
        await $(await DateRangePage.dateRangeToYear()).setValue(2017);
        await $(await DateRangePage.submit()).click();
        await expect(await $(await DateRangePage.errorNumber(1)).getText()).to.contain("Enter a reporting period greater than or equal to 2 months");
      });

      it("When I enter valid dates, Then I should see the summary page", async ()=> {
        await $(await DateRangePage.dateRangeFromMonth()).setValue(1);
        await $(await DateRangePage.dateRangeFromYear()).setValue(2017);

        // Min range
        await $(await DateRangePage.dateRangeToMonth()).setValue(3);
        await $(await DateRangePage.dateRangeToYear()).setValue(2017);
        await $(await DateRangePage.submit()).click();
        await expect(await $(await SubmitPage.dateRangeFrom()).getText()).to.contain("January 2017 to March 2017");

        // Max range
        await $(await SubmitPage.dateRangeFromEdit()).click();
        await $(await DateRangePage.dateRangeToMonth()).setValue(4);
        await $(await DateRangePage.dateRangeToYear()).setValue(2017);
        await $(await DateRangePage.submit()).click();
        await expect(await $(await SubmitPage.dateRangeFrom()).getText()).to.contain("January 2017 to April 2017");
      });
    });
  });
});
