import TotalTurnoverPage from "../../../../generated_pages/validation_sum_against_total_hub_with_dependent_section/total-turnover-block.page";
import TotalEmployeesPage from "../../../../generated_pages/validation_sum_against_total_hub_with_dependent_section/total-employees-block.page";
import CompanySectionSummary from "../../../../generated_pages/validation_sum_against_total_hub_with_dependent_section/company-overview-section-summary.page";

import TurnoverBreakdownPage from "../../../../generated_pages/validation_sum_against_total_hub_with_dependent_section/turnover-breakdown-block.page";
import EmployeesBreakdownPage from "../../../../generated_pages/validation_sum_against_total_hub_with_dependent_section/employees-breakdown-block.page";
import BreakdownSectionSummary from "../../../../generated_pages/validation_sum_against_total_hub_with_dependent_section/breakdown-section-summary.page";

import HubPage from "../../../../base_pages/hub.page";
import ThankYouPage from "../../../../base_pages/thank-you.page";

const companyOverviewSectionID = "company-overview-section";
const breakdownSectionId = "breakdown-section";

const answerAndSubmitTurnoverBreakdownQuestion = (breakdown1, breakdown2, breakdown3) => {
  $(TurnoverBreakdownPage.turnoverBreakdown1()).setValue(breakdown1);
  $(TurnoverBreakdownPage.turnoverBreakdown2()).setValue(breakdown2);
  $(TurnoverBreakdownPage.turnoverBreakdown3()).setValue(breakdown3);
  $(TurnoverBreakdownPage.submit()).click();
};

const answerAndSubmitEmployeeBreakdownQuestion = (breakdown1, breakdown2) => {
  $(EmployeesBreakdownPage.employeesBreakdown1()).setValue(breakdown1);
  $(EmployeesBreakdownPage.employeesBreakdown2()).setValue(breakdown2);
  $(EmployeesBreakdownPage.submit()).click();
};

const answerAndSubmitTotalTurnoverQuestion = (total) => {
  $(TotalTurnoverPage.totalTurnover()).setValue(total);
  $(TotalTurnoverPage.submit()).click();
};

const answerAndSubmitTotalEmployeesQuestion = (total) => {
  $(TotalEmployeesPage.totalEmployees()).setValue(total);
  $(TotalEmployeesPage.submit()).click();
};

describe("Feature: Validation - Sum of grouped answers to equal total (Total in separate section)", () => {
  describe("Given I start a grouped answer validation with dependent sections and complete the total turnover and total employees questions", () => {
    beforeEach(() => {
      browser.openQuestionnaire("test_validation_sum_against_total_hub_with_dependent_section.json");
      answerAndSubmitTotalTurnoverQuestion(1000);
      answerAndSubmitTotalEmployeesQuestion(10);
      $(CompanySectionSummary.submit()).click();

      expect($(HubPage.summaryRowState(companyOverviewSectionID)).getText()).to.equal("Completed");
    });

    it("When I am on the hub, Then the breakdown section should be marked as 'Not Started'", () => {
      expect($(HubPage.summaryRowState(breakdownSectionId)).getText()).to.equal("Not started");
    });

    it("When I start the breakdown section and enter answers that are equal the total, Then I should be able to get to the section summary and the breakdown section should be marked as 'Completed'", () => {
      $(HubPage.submit()).click();
      answerAndSubmitTurnoverBreakdownQuestion(500, 250, 250);
      answerAndSubmitEmployeeBreakdownQuestion(5, 5);

      expect(browser.getUrl()).to.contain(BreakdownSectionSummary.pageName);
      $(BreakdownSectionSummary.submit()).click();

      expect($(HubPage.summaryRowState(breakdownSectionId)).getText()).to.equal("Completed");
    });

    it("When I start the breakdown section and enter an answer that is not equal to the total for the turnover question, Then I should see a validation error", () => {
      $(HubPage.submit()).click();
      answerAndSubmitTurnoverBreakdownQuestion(1000, 250, 250);

      expect($(TurnoverBreakdownPage.errorNumber(1)).getText()).to.contain("Enter answers that add up to £1,000.00");
    });

    it("When I start the breakdown section and enter an answer that is not equal to the total for the employees question, Then I should see a validation error", () => {
      $(HubPage.submit()).click();
      // Answer turnover question
      answerAndSubmitTurnoverBreakdownQuestion(500, 250, 250);

      expect(browser.getUrl()).to.contain(EmployeesBreakdownPage.pageName);
      answerAndSubmitEmployeeBreakdownQuestion(10, 5);

      expect($(EmployeesBreakdownPage.errorNumber(1)).getText()).to.contain("Enter answers that add up to 10");
    });
  });

  describe("Given I start a grouped answer validation with dependent sections and complete the overview and breakdown sections", () => {
    before(() => {
      browser.openQuestionnaire("test_validation_sum_against_total_hub_with_dependent_section.json");

      // Complete overview section
      answerAndSubmitTotalTurnoverQuestion(1000);
      answerAndSubmitTotalEmployeesQuestion(10);
      $(CompanySectionSummary.submit()).click();

      // Complete breakdown section
      $(HubPage.submit()).click();
      answerAndSubmitTurnoverBreakdownQuestion(500, 250, 250);
      answerAndSubmitEmployeeBreakdownQuestion(5, 5);
      $(BreakdownSectionSummary.submit()).click();

      expect($(HubPage.summaryRowState(breakdownSectionId)).getText()).to.equal("Completed");
    });

    it("When I change my answer for the total turnover question, Then the breakdown section should be marked as 'Partially completed'", () => {
      $(HubPage.summaryRowLink(companyOverviewSectionID)).click();
      $(CompanySectionSummary.totalTurnoverAnswerEdit()).click();

      answerAndSubmitTotalTurnoverQuestion(1500);
      $(CompanySectionSummary.submit()).click();
      expect($(HubPage.summaryRowState(breakdownSectionId)).getText()).to.equal("Partially completed");
    });

    it("When I click 'Continue with section' on the breakdown section, Then I should be taken to the turnover breakdown question and my previous answers should be prefilled", () => {
      $(HubPage.summaryRowLink(breakdownSectionId)).click();

      expect($(TurnoverBreakdownPage.turnoverBreakdown1()).getValue()).to.equal("500.00");
      expect($(TurnoverBreakdownPage.turnoverBreakdown2()).getValue()).to.equal("250.00");
      expect($(TurnoverBreakdownPage.turnoverBreakdown3()).getValue()).to.equal("250.00");
    });

    it("When I submit the turnover breakdown question with no changes, Then I should see a validation error", () => {
      $(TurnoverBreakdownPage.submit()).click();

      expect($(TurnoverBreakdownPage.errorNumber(1)).getText()).to.contain("Enter answers that add up to £1,500.00");
    });

    it("When I update my answers to equal the new total turnover, Then I should be able to get to the section summary and the breakdown section should be marked as 'Completed'", () => {
      answerAndSubmitTurnoverBreakdownQuestion(500, 500, 500);

      expect(browser.getUrl()).to.contain(BreakdownSectionSummary.pageName);
      $(BreakdownSectionSummary.submit()).click();
      expect($(HubPage.summaryRowState(breakdownSectionId)).getText()).to.equal("Completed");
    });

    it("When I change my answer for the total employees question, Then the breakdown section should be marked as 'Partially completed'", () => {
      $(HubPage.summaryRowLink(companyOverviewSectionID)).click();
      $(CompanySectionSummary.totalEmployeesAnswerEdit()).click();

      answerAndSubmitTotalEmployeesQuestion(15);
      $(CompanySectionSummary.submit()).click();
      expect($(HubPage.summaryRowState(breakdownSectionId)).getText()).to.equal("Partially completed");
    });

    it("When I click 'Continue with section' on the breakdown section, Then I should be taken to the employee breakdown question and my previous answers should be prefilled", () => {
      $(HubPage.summaryRowLink(breakdownSectionId)).click();

      expect($(EmployeesBreakdownPage.employeesBreakdown1()).getValue()).to.equal("5");
      expect($(EmployeesBreakdownPage.employeesBreakdown2()).getValue()).to.equal("5");
    });

    it("When I submit the employee breakdown question with no changes, Then I should see a validation error", () => {
      $(TurnoverBreakdownPage.submit()).click();

      expect($(EmployeesBreakdownPage.errorNumber(1)).getText()).to.contain("Enter answers that add up to 15");
    });

    it("When I update my answers to equal the new total employees, Then I should be able to get to the section summary and the breakdown section should be marked as 'Completed'", () => {
      answerAndSubmitEmployeeBreakdownQuestion(10, 5);

      expect(browser.getUrl()).to.contain(BreakdownSectionSummary.pageName);
      $(BreakdownSectionSummary.submit()).click();
      expect($(HubPage.summaryRowState(breakdownSectionId)).getText()).to.equal("Completed");
    });

    it("When I edit and resubmit the total employees question without changing the value, Then the breakdown section should stay marked as 'Completed'", () => {
      $(HubPage.summaryRowLink(companyOverviewSectionID)).click();
      $(CompanySectionSummary.totalTurnoverAnswerEdit()).click();

      expect($(TotalTurnoverPage.totalTurnover()).getValue()).to.equal("1500.00");
      $(TotalTurnoverPage.submit()).click();
      $(CompanySectionSummary.submit()).click();

      expect($(HubPage.summaryRowState(breakdownSectionId)).getText()).to.equal("Completed");
    });

    it("When I submit the questionnaire, Then I should see the thank you page", () => {
      $(HubPage.submit()).click();

      expect(browser.getUrl()).to.contain(ThankYouPage.pageName);
    });
  });
});
