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

const answerAndSubmitTurnoverBreakdownQuestion = async (breakdown1, breakdown2, breakdown3) => {
  await $(await TurnoverBreakdownPage.turnoverBreakdown1()).setValue(breakdown1);
  await $(await TurnoverBreakdownPage.turnoverBreakdown2()).setValue(breakdown2);
  await $(await TurnoverBreakdownPage.turnoverBreakdown3()).setValue(breakdown3);
  await $(await TurnoverBreakdownPage.submit()).click();
};

const answerAndSubmitEmployeeBreakdownQuestion = async (breakdown1, breakdown2) => {
  await $(await EmployeesBreakdownPage.employeesBreakdown1()).setValue(breakdown1);
  await $(await EmployeesBreakdownPage.employeesBreakdown2()).setValue(breakdown2);
  await $(await EmployeesBreakdownPage.submit()).click();
};

const answerAndSubmitTotalTurnoverQuestion = async (total) => {
  await $(await TotalTurnoverPage.totalTurnover()).setValue(total);
  await $(await TotalTurnoverPage.submit()).click();
};

const answerAndSubmitTotalEmployeesQuestion = async (total) => {
  await $(await TotalEmployeesPage.totalEmployees()).setValue(total);
  await $(await TotalEmployeesPage.submit()).click();
};

describe("Feature: Validation - Sum of grouped answers to equal total (Total in separate section)", () => {
  describe("Given I start a grouped answer validation with dependent sections and complete the total turnover and total employees questions", () => {
    before(async ()=> {
      await browser.openQuestionnaire("test_validation_sum_against_total_hub_with_dependent_section.json");
      answerAndSubmitTotalTurnoverQuestion(1000);
      answerAndSubmitTotalEmployeesQuestion(10);
      await $(await CompanySectionSummary.submit()).click();

      await expect(await $(await HubPage.summaryRowState(companyOverviewSectionID)).getText()).to.equal("Completed");
    });

    it("When I am on the hub, Then the breakdown section should be marked as 'Not Started'", async ()=> {
      await expect(await $(await HubPage.summaryRowState(breakdownSectionId)).getText()).to.equal("Not started");
    });

    it("When I start the breakdown section and enter an answer that is not equal to the total for the turnover question, Then I should see a validation error", async ()=> {
      await $(await HubPage.submit()).click();
      answerAndSubmitTurnoverBreakdownQuestion(1000, 250, 250);

      await expect(await $(await TurnoverBreakdownPage.errorNumber(1)).getText()).to.contain("Enter answers that add up to £1,000.00");
    });

    it("When I start the breakdown section and enter answers that are equal the total, Then I should be able to get to the section summary and the breakdown section should be marked as 'Completed'", async ()=> {
      answerAndSubmitTurnoverBreakdownQuestion(500, 250, 250);
      answerAndSubmitEmployeeBreakdownQuestion(5, 5);

      await expect(browser.getUrl()).to.contain(BreakdownSectionSummary.pageName);
      await $(await BreakdownSectionSummary.submit()).click();

      await expect(await $(await HubPage.summaryRowState(breakdownSectionId)).getText()).to.equal("Completed");
    });
  });

  describe("Given I start a grouped answer validation with dependent sections and complete the overview and breakdown sections", () => {
    before(async ()=> {
      await browser.openQuestionnaire("test_validation_sum_against_total_hub_with_dependent_section.json");

      // Complete overview section
      answerAndSubmitTotalTurnoverQuestion(1000);
      answerAndSubmitTotalEmployeesQuestion(10);
      await $(await CompanySectionSummary.submit()).click();

      // Complete breakdown section
      await $(await HubPage.submit()).click();
      answerAndSubmitTurnoverBreakdownQuestion(500, 250, 250);
      answerAndSubmitEmployeeBreakdownQuestion(5, 5);
      await $(await BreakdownSectionSummary.submit()).click();

      await expect(await $(await HubPage.summaryRowState(breakdownSectionId)).getText()).to.equal("Completed");
    });

    it("When I change my answer for the total turnover question, Then the breakdown section should be marked as 'Partially completed'", async ()=> {
      await $(await HubPage.summaryRowLink(companyOverviewSectionID)).click();
      await $(await CompanySectionSummary.totalTurnoverAnswerEdit()).click();

      answerAndSubmitTotalTurnoverQuestion(1500);
      await $(await CompanySectionSummary.submit()).click();
      await expect(await $(await HubPage.summaryRowState(breakdownSectionId)).getText()).to.equal("Partially completed");
    });

    it("When I click 'Continue with section' on the breakdown section, Then I should be taken to the turnover breakdown question and my previous answers should be prefilled", async ()=> {
      await $(await HubPage.summaryRowLink(breakdownSectionId)).click();

      await expect(await $(await TurnoverBreakdownPage.turnoverBreakdown1()).getValue()).to.equal("500.00");
      await expect(await $(await TurnoverBreakdownPage.turnoverBreakdown2()).getValue()).to.equal("250.00");
      await expect(await $(await TurnoverBreakdownPage.turnoverBreakdown3()).getValue()).to.equal("250.00");
    });

    it("When I submit the turnover breakdown question with no changes, Then I should see a validation error", async ()=> {
      await $(await TurnoverBreakdownPage.submit()).click();

      await expect(await $(await TurnoverBreakdownPage.errorNumber(1)).getText()).to.contain("Enter answers that add up to £1,500.00");
    });

    it("When I update my answers to equal the new total turnover, Then I should be able to get to the section summary and the breakdown section should be marked as 'Completed'", async ()=> {
      answerAndSubmitTurnoverBreakdownQuestion(500, 500, 500);

      await expect(browser.getUrl()).to.contain(BreakdownSectionSummary.pageName);
      await $(await BreakdownSectionSummary.submit()).click();
      await expect(await $(await HubPage.summaryRowState(breakdownSectionId)).getText()).to.equal("Completed");
    });

    it("When I submit the questionnaire, Then I should see the thank you page", async ()=> {
      await $(await HubPage.submit()).click();

      await expect(browser.getUrl()).to.contain(ThankYouPage.pageName);
    });
  });
});
