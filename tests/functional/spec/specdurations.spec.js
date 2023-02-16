import DurationPage from "../generated_pages/durations/duration-block.page.js";
import SubmitPage from "../generated_pages/durations/submit.page.js";

describe("Durations", () => {
  beforeEach("Load the survey", async ()=> {
    await browser.openQuestionnaire("test_durations.json");
  });

  it("Given the test_durations survey is selected durations suffixes are visible", async ()=> {
    await expect(await $(await DurationPage.yearMonthYearsSuffix()).getText()).to.contain("Years");
    await expect(await $(await DurationPage.mandatoryYearMonthMonthsSuffix()).getText()).to.contain("Months");
    await expect(await $(await DurationPage.yearYearsSuffix()).getText()).to.contain("Years");
    await expect(await $(await DurationPage.mandatoryMonthMonthsSuffix()).getText()).to.contain("Months");
  });

  it("Given the test_durations survey is selected when durations are entered then the summary screen shows the durations entered formatted", async ()=> {
    await $(await DurationPage.yearMonthYears()).setValue(1);
    await $(await DurationPage.yearMonthMonths()).setValue(2);
    await $(await DurationPage.mandatoryYearMonthYears()).setValue(1);
    await $(await DurationPage.mandatoryYearMonthMonths()).setValue(2);
    await $(await DurationPage.mandatoryYearYears()).setValue(1);
    await $(await DurationPage.mandatoryMonthMonths()).setValue(1);
    await $(await DurationPage.submit()).click();

    await expect(browser.getUrl()).to.contain(SubmitPage.pageName);
    await expect(await $(await SubmitPage.yearMonthAnswer()).getText()).to.equal("1 year 2 months");
    await $(await SubmitPage.submit()).click();
  });

  it("Given the test_durations survey is selected when one of the units is 0 it is excluded from the summary", async ()=> {
    await $(await DurationPage.yearMonthYears()).setValue(0);
    await $(await DurationPage.yearMonthMonths()).setValue(2);
    await $(await DurationPage.mandatoryYearMonthYears()).setValue(1);
    await $(await DurationPage.mandatoryYearMonthMonths()).setValue(2);
    await $(await DurationPage.mandatoryYearYears()).setValue(1);
    await $(await DurationPage.mandatoryMonthMonths()).setValue(1);
    await $(await DurationPage.submit()).click();

    await expect(browser.getUrl()).to.contain(SubmitPage.pageName);
    await expect(await $(await SubmitPage.yearMonthAnswer()).getText()).to.equal("2 months");
    await $(await SubmitPage.submit()).click();
  });

  it("Given the test_durations survey is selected when no duration is entered the summary shows no answer provided", async ()=> {
    await $(await DurationPage.mandatoryYearMonthYears()).setValue(1);
    await $(await DurationPage.mandatoryYearMonthMonths()).setValue(2);
    await $(await DurationPage.mandatoryYearYears()).setValue(1);
    await $(await DurationPage.mandatoryMonthMonths()).setValue(1);
    await $(await DurationPage.submit()).click();

    await expect(browser.getUrl()).to.contain(SubmitPage.pageName);
    await expect(await $(await SubmitPage.yearMonthAnswer()).getText()).to.equal("No answer provided");
    await $(await SubmitPage.submit()).click();
  });

  it("Given the test_durations survey is selected when one of the units is missing an error is shown", async ()=> {
    await $(await DurationPage.yearMonthMonths()).setValue(2);
    await $(await DurationPage.mandatoryYearMonthMonths()).setValue(2);
    await $(await DurationPage.mandatoryYearYears()).setValue(1);
    await $(await DurationPage.mandatoryMonthMonths()).setValue(1);
    await $(await DurationPage.submit()).click();

    await expect(await $(await DurationPage.errorNumber(1)).getText()).to.contain("Enter a valid duration");
    await expect(await $(await DurationPage.errorNumber(2)).getText()).to.contain("Enter a valid duration");
  });

  it("Given the test_durations survey is selected when one of the units not a number an error is shown", async ()=> {
    await $(await DurationPage.yearMonthYears()).setValue("word");
    await $(await DurationPage.yearMonthMonths()).setValue(2);
    await $(await DurationPage.mandatoryYearMonthYears()).setValue("word");
    await $(await DurationPage.mandatoryYearMonthMonths()).setValue(2);
    await $(await DurationPage.mandatoryYearYears()).setValue(1);
    await $(await DurationPage.mandatoryMonthMonths()).setValue(1);
    await $(await DurationPage.submit()).click();

    await expect(await $(await DurationPage.errorNumber(1)).getText()).to.contain("Enter a valid duration");
    await expect(await $(await DurationPage.errorNumber(2)).getText()).to.contain("Enter a valid duration");
  });

  it("Given the test_durations survey is selected when the number of months is more than 11 an error is shown", async ()=> {
    await $(await DurationPage.yearMonthYears()).setValue(1);
    await $(await DurationPage.yearMonthMonths()).setValue(12);
    await $(await DurationPage.mandatoryYearMonthYears()).setValue(1);
    await $(await DurationPage.mandatoryYearMonthMonths()).setValue(12);
    await $(await DurationPage.mandatoryYearYears()).setValue(1);
    await $(await DurationPage.mandatoryMonthMonths()).setValue(1);
    await $(await DurationPage.submit()).click();

    await expect(await $(await DurationPage.errorNumber(1)).getText()).to.contain("Enter a valid duration");
    await expect(await $(await DurationPage.errorNumber(2)).getText()).to.contain("Enter a valid duration");
  });

  it("Given the test_durations survey is selected when the mandatory duration is missing an error is shown", async ()=> {
    await $(await DurationPage.mandatoryYearYears()).setValue(1);
    await $(await DurationPage.mandatoryMonthMonths()).setValue(1);
    await $(await DurationPage.submit()).click();

    await expect(await $(await DurationPage.errorNumber(1)).getText()).to.contain("Enter a duration");
  });
});
