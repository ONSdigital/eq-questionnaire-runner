import DurationPage from "../generated_pages/durations/duration-block.page.js";
import SubmitPage from "../generated_pages/durations/submit.page.js";
import { click } from "../helpers";

describe("Durations", () => {
  beforeEach("Load the survey", async () => {
    await browser.openQuestionnaire("test_durations.json");
  });

  it("Given the test_durations survey is selected durations suffixes are visible", async () => {
    await expect(await $(DurationPage.yearMonthYearsSuffix()).getText()).to.contain("Years");
    await expect(await $(DurationPage.mandatoryYearMonthMonthsSuffix()).getText()).to.contain("Months");
    await expect(await $(DurationPage.yearYearsSuffix()).getText()).to.contain("Years");
    await expect(await $(DurationPage.mandatoryMonthMonthsSuffix()).getText()).to.contain("Months");
  });

  it("Given the test_durations survey is selected when durations are entered then the summary screen shows the durations entered formatted", async () => {
    await $(DurationPage.yearMonthYears()).setValue(1);
    await $(DurationPage.yearMonthMonths()).setValue(2);
    await $(DurationPage.mandatoryYearMonthYears()).setValue(1);
    await $(DurationPage.mandatoryYearMonthMonths()).setValue(2);
    await $(DurationPage.mandatoryYearYears()).setValue(1);
    await $(DurationPage.mandatoryMonthMonths()).setValue(1);
    await click(DurationPage.submit());

    await expect(await browser.getUrl()).to.contain(SubmitPage.pageName);
    await expect(await $(SubmitPage.yearMonthAnswer()).getText()).to.equal("1 year 2 months");
    await click(SubmitPage.submit());
  });

  it("Given the test_durations survey is selected when one of the units is 0 it is excluded from the summary", async () => {
    await $(DurationPage.yearMonthYears()).setValue(0);
    await $(DurationPage.yearMonthMonths()).setValue(2);
    await $(DurationPage.mandatoryYearMonthYears()).setValue(1);
    await $(DurationPage.mandatoryYearMonthMonths()).setValue(2);
    await $(DurationPage.mandatoryYearYears()).setValue(1);
    await $(DurationPage.mandatoryMonthMonths()).setValue(1);
    await click(DurationPage.submit());

    await expect(await browser.getUrl()).to.contain(SubmitPage.pageName);
    await expect(await $(SubmitPage.yearMonthAnswer()).getText()).to.equal("2 months");
    await click(SubmitPage.submit());
  });

  it("Given the test_durations survey is selected when no duration is entered the summary shows no answer provided", async () => {
    await $(DurationPage.mandatoryYearMonthYears()).setValue(1);
    await $(DurationPage.mandatoryYearMonthMonths()).setValue(2);
    await $(DurationPage.mandatoryYearYears()).setValue(1);
    await $(DurationPage.mandatoryMonthMonths()).setValue(1);
    await click(DurationPage.submit());

    await expect(await browser.getUrl()).to.contain(SubmitPage.pageName);
    await expect(await $(SubmitPage.yearMonthAnswer()).getText()).to.equal("No answer provided");
    await click(SubmitPage.submit());
  });

  it("Given the test_durations survey is selected when one of the units is missing an error is shown", async () => {
    await $(DurationPage.yearMonthMonths()).setValue(2);
    await $(DurationPage.mandatoryYearMonthMonths()).setValue(2);
    await $(DurationPage.mandatoryYearYears()).setValue(1);
    await $(DurationPage.mandatoryMonthMonths()).setValue(1);
    await click(DurationPage.submit());

    await expect(await $(DurationPage.errorNumber(1)).getText()).to.contain("Enter a valid duration");
    await expect(await $(DurationPage.errorNumber(2)).getText()).to.contain("Enter a valid duration");
  });

  it("Given the test_durations survey is selected when one of the units not a number an error is shown", async () => {
    await $(DurationPage.yearMonthYears()).setValue("word");
    await $(DurationPage.yearMonthMonths()).setValue(2);
    await $(DurationPage.mandatoryYearMonthYears()).setValue("word");
    await $(DurationPage.mandatoryYearMonthMonths()).setValue(2);
    await $(DurationPage.mandatoryYearYears()).setValue(1);
    await $(DurationPage.mandatoryMonthMonths()).setValue(1);
    await click(DurationPage.submit());

    await expect(await $(DurationPage.errorNumber(1)).getText()).to.contain("Enter a valid duration");
    await expect(await $(DurationPage.errorNumber(2)).getText()).to.contain("Enter a valid duration");
  });

  it("Given the test_durations survey is selected when the number of months is more than 11 an error is shown", async () => {
    await $(DurationPage.yearMonthYears()).setValue(1);
    await $(DurationPage.yearMonthMonths()).setValue(12);
    await $(DurationPage.mandatoryYearMonthYears()).setValue(1);
    await $(DurationPage.mandatoryYearMonthMonths()).setValue(12);
    await $(DurationPage.mandatoryYearYears()).setValue(1);
    await $(DurationPage.mandatoryMonthMonths()).setValue(1);
    await click(DurationPage.submit());

    await expect(await $(DurationPage.errorNumber(1)).getText()).to.contain("Enter a valid duration");
    await expect(await $(DurationPage.errorNumber(2)).getText()).to.contain("Enter a valid duration");
  });

  it("Given the test_durations survey is selected when the mandatory duration is missing an error is shown", async () => {
    await $(DurationPage.mandatoryYearYears()).setValue(1);
    await $(DurationPage.mandatoryMonthMonths()).setValue(1);
    await click(DurationPage.submit());

    await expect(await $(DurationPage.errorNumber(1)).getText()).to.contain("Enter a duration");
  });
});
