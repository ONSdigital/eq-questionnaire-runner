import DurationPage from "../generated_pages/durations/duration-block.page.js";
import SummaryPage from "../generated_pages/durations/summary.page.js";

describe("Durations", () => {
  beforeEach("Load the survey", () => {
    browser.openQuestionnaire("test_durations.json");
  });

  it("Given the test_durations survey is selected when durations are entered then the summary screen shows the durations entered formatted", () => {
    $(DurationPage.yearMonthYears()).setValue(1);
    $(DurationPage.yearMonthMonths()).setValue(2);
    $(DurationPage.mandatoryYearMonthYears()).setValue(1);
    $(DurationPage.mandatoryYearMonthMonths()).setValue(2);
    $(DurationPage.mandatoryYearYears()).setValue(1);
    $(DurationPage.mandatoryMonthMonths()).setValue(1);
    $(DurationPage.submit()).click();

    expect(browser.getUrl()).to.contain(SummaryPage.pageName);
    expect($(SummaryPage.yearMonthAnswer()).getText()).to.equal("1 year 2 months");
    $(SummaryPage.submit()).click();
  });

  it("Given the test_durations survey is selected when one of the units is 0 it is excluded from the summary", () => {
    $(DurationPage.yearMonthYears()).setValue(0);
    $(DurationPage.yearMonthMonths()).setValue(2);
    $(DurationPage.mandatoryYearMonthYears()).setValue(1);
    $(DurationPage.mandatoryYearMonthMonths()).setValue(2);
    $(DurationPage.mandatoryYearYears()).setValue(1);
    $(DurationPage.mandatoryMonthMonths()).setValue(1);
    $(DurationPage.submit()).click();

    expect(browser.getUrl()).to.contain(SummaryPage.pageName);
    expect($(SummaryPage.yearMonthAnswer()).getText()).to.equal("2 months");
    $(SummaryPage.submit()).click();
  });

  it("Given the test_durations survey is selected when no duration is entered the summary shows no answer provided", () => {
    $(DurationPage.mandatoryYearMonthYears()).setValue(1);
    $(DurationPage.mandatoryYearMonthMonths()).setValue(2);
    $(DurationPage.mandatoryYearYears()).setValue(1);
    $(DurationPage.mandatoryMonthMonths()).setValue(1);
    $(DurationPage.submit()).click();

    expect(browser.getUrl()).to.contain(SummaryPage.pageName);
    expect($(SummaryPage.yearMonthAnswer()).getText()).to.equal("No answer provided");
    $(SummaryPage.submit()).click();
  });

  it("Given the test_durations survey is selected when one of the units is missing an error is shown", () => {
    $(DurationPage.yearMonthMonths()).setValue(2);
    $(DurationPage.mandatoryYearMonthMonths()).setValue(2);
    $(DurationPage.mandatoryYearYears()).setValue(1);
    $(DurationPage.mandatoryMonthMonths()).setValue(1);
    $(DurationPage.submit()).click();

    expect($(DurationPage.errorNumber(1)).getText()).to.contain("Enter a valid duration");
    expect($(DurationPage.errorNumber(2)).getText()).to.contain("Enter a valid duration");
  });

  it("Given the test_durations survey is selected when one of the units not a number an error is shown", () => {
    $(DurationPage.yearMonthYears()).setValue("word");
    $(DurationPage.yearMonthMonths()).setValue(2);
    $(DurationPage.mandatoryYearMonthYears()).setValue("word");
    $(DurationPage.mandatoryYearMonthMonths()).setValue(2);
    $(DurationPage.mandatoryYearYears()).setValue(1);
    $(DurationPage.mandatoryMonthMonths()).setValue(1);
    $(DurationPage.submit()).click();

    expect($(DurationPage.errorNumber(1)).getText()).to.contain("Enter a valid duration");
    expect($(DurationPage.errorNumber(2)).getText()).to.contain("Enter a valid duration");
  });

  it("Given the test_durations survey is selected when the number of months is more than 11 an error is shown", () => {
    $(DurationPage.yearMonthYears()).setValue(1);
    $(DurationPage.yearMonthMonths()).setValue(12);
    $(DurationPage.mandatoryYearMonthYears()).setValue(1);
    $(DurationPage.mandatoryYearMonthMonths()).setValue(12);
    $(DurationPage.mandatoryYearYears()).setValue(1);
    $(DurationPage.mandatoryMonthMonths()).setValue(1);
    $(DurationPage.submit()).click();

    expect($(DurationPage.errorNumber(1)).getText()).to.contain("Enter a valid duration");
    expect($(DurationPage.errorNumber(2)).getText()).to.contain("Enter a valid duration");
  });

  it("Given the test_durations survey is selected when the mandatory duration is missing an error is shown", () => {
    $(DurationPage.mandatoryYearYears()).setValue(1);
    $(DurationPage.mandatoryMonthMonths()).setValue(1);
    $(DurationPage.submit()).click();

    expect($(DurationPage.errorNumber(1)).getText()).to.contain("Enter a duration");
  });
});
