import EmployeeNumberBlockPage from "../../../generated_pages/placeholder_default_value/employee-number-block.page";

describe("Placeholder default value check", () => {
  beforeEach("Load the survey", () => {
    browser.openQuestionnaire("test_placeholder_default_value.json");
  });

  it("Given question regarding number of employee, when I do not enter any number and click submit, then the interstitial page shows default employee count value as 0", () => {
    $(EmployeeNumberBlockPage.submit()).click();
    expect($("#main-content > p").getText()).to.contain("The number of employee confirmed are 0 (default value)");
  });

  it("Given question regarding number of employee, when I enter a number of employee and click submit, then the interstitial page shows me the employee count entered", () => {
    $(EmployeeNumberBlockPage.employeeNo()).setValue("54");
    $(EmployeeNumberBlockPage.submit()).click();
    expect($("#main-content > p").getText()).to.contain("The number of employee confirmed are 54");
  });
});
