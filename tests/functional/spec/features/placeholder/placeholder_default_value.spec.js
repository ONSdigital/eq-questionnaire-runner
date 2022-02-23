import EmployeesNumberBlockPage from "../../../generated_pages/placeholder_default_value/employees-number-block.page";

describe("Placeholder default value check", () => {
  beforeEach("Load the survey", () => {
    browser.openQuestionnaire("test_placeholder_default_value.json");
  });

  it("Given a question with default answer, When I do not enter any number and click submit, Then the interstitial page shows default employees number as 0", () => {
    $(EmployeesNumberBlockPage.submit()).click();
    expect($("#main-content > p").getText()).to.contain("The total number of employees confirmed are 0 (default value)");
  });

  it("Given a question with default answer, When I enter a number of employee and click submit, Then the interstitial page shows me the employees number entered", () => {
    $(EmployeesNumberBlockPage.employeesNo()).setValue("54");
    $(EmployeesNumberBlockPage.submit()).click();
    expect($("#main-content > p").getText()).to.contain("The total number of employees confirmed are 54");
  });
});
