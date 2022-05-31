import EmployeesNumberBlockPage from "../../../generated_pages/placeholder_default_value/employees-number-block.page";
import EmployeesTrainingBlockPage from "../../../generated_pages/placeholder_default_value/employees-training-block.page";
import EmployeesNumberInterstitialPage from "../../../generated_pages/placeholder_default_value/employees-number-interstitial.page";

describe("Placeholder default value check", () => {
  beforeEach("Load the survey", () => {
    browser.openQuestionnaire("test_placeholder_default_value.json");
  });

  it("Given a question with default answer, When I do not enter any number and click submit, Then the interstitial page shows default employees number as 0", () => {
    $(EmployeesNumberBlockPage.submit()).click();
    expect($("#main-content > p").getText()).to.contain("The total number of employees confirmed are 0");
  });

  it("Given a question with default answer, When I enter a number of employee and click submit, Then the interstitial page shows me the employees number entered", () => {
    $(EmployeesNumberBlockPage.employeesNo()).setValue("54");
    $(EmployeesNumberBlockPage.submit()).click();
    expect($("#main-content > p").getText()).to.contain("The total number of employees confirmed are 54");
  });
  it("Given a training budget question with default answer, When I do not enter any amount and click submit, Then the interstitial page shows default amount as 250.00", () => {
    $(EmployeesNumberBlockPage.submit()).click();
    $(EmployeesNumberInterstitialPage.submit()).click();
    $(EmployeesTrainingBlockPage.submit()).click();
    expect($("#main-content > p").getText()).to.contain("The average training budget per employee is £250.00");
  });
  it("Given a training budget question with default answer, When I enter an amount and click submit, Then the interstitial page shows amount entered", () => {
    $(EmployeesNumberBlockPage.submit()).click();
    $(EmployeesNumberInterstitialPage.submit()).click();
    $(EmployeesTrainingBlockPage.employeesAvgTraining()).setValue("100");
    $(EmployeesTrainingBlockPage.submit()).click();
    expect($("#main-content > p").getText()).to.contain("The average training budget per employee is £100.00");
  });
});
