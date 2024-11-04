import TotalTurnoverPage from "../../../../generated_pages/validation_sum_against_total_hub_with_dependent_section/total-turnover-block.page";
import TotalEmployeesPage from "../../../../generated_pages/validation_sum_against_total_hub_with_dependent_section/total-employees-block.page";
import CompanySectionSummary from "../../../../generated_pages/validation_sum_against_total_hub_with_dependent_section/company-overview-section-summary.page";

import TurnoverBreakdownPage from "../../../../generated_pages/validation_sum_against_total_hub_with_dependent_section/turnover-breakdown-block.page";
import EmployeesBreakdownPage from "../../../../generated_pages/validation_sum_against_total_hub_with_dependent_section/employees-breakdown-block.page";
import BreakdownSectionSummary from "../../../../generated_pages/validation_sum_against_total_hub_with_dependent_section/breakdown-section-summary.page";

import HubPage from "../../../../base_pages/hub.page";
import ThankYouPage from "../../../../base_pages/thank-you.page";
import { click, verifyUrlContains } from "../../../../helpers";
const companyOverviewSectionID = "company-overview-section";
const breakdownSectionId = "breakdown-section";

const answerAndSubmitTurnoverBreakdownQuestion = async (breakdown1, breakdown2, breakdown3) => {
  await $(TurnoverBreakdownPage.turnoverBreakdown1()).setValue(breakdown1);
  await $(TurnoverBreakdownPage.turnoverBreakdown2()).setValue(breakdown2);
  await $(TurnoverBreakdownPage.turnoverBreakdown3()).setValue(breakdown3);
  await click(TurnoverBreakdownPage.submit());
};

const answerAndSubmitEmployeeBreakdownQuestion = async (breakdown1, breakdown2) => {
  await $(EmployeesBreakdownPage.employeesBreakdown1()).setValue(breakdown1);
  await $(EmployeesBreakdownPage.employeesBreakdown2()).setValue(breakdown2);
  await click(EmployeesBreakdownPage.submit());
};

const answerAndSubmitTotalTurnoverQuestion = async (total) => {
  await $(TotalTurnoverPage.totalTurnover()).setValue(total);
  await click(TotalTurnoverPage.submit());
};

const answerAndSubmitTotalEmployeesQuestion = async (total) => {
  await $(TotalEmployeesPage.totalEmployees()).setValue(total);
  await click(TotalEmployeesPage.submit());
};

describe("Feature: Validation - Sum of grouped answers to equal total (Total in separate section)", () => {
  describe("Given I start a grouped answer validation with dependent sections and complete the total turnover and total employees questions", () => {
    before(async () => {
      await browser.openQuestionnaire("test_validation_sum_against_total_hub_with_dependent_section.json");
      await answerAndSubmitTotalTurnoverQuestion(1000);
      await answerAndSubmitTotalEmployeesQuestion(10);
      await click(CompanySectionSummary.submit());

      await expect(await $(HubPage.summaryRowState(companyOverviewSectionID)).getText()).toBe("Completed");
    });

    it("When I am on the hub, Then the breakdown section should be marked as 'Not Started'", async () => {
      await expect(await $(HubPage.summaryRowState(breakdownSectionId)).getText()).toBe("Not started");
    });

    it("When I start the breakdown section and enter an answer that is not equal to the total for the turnover question, Then I should see a validation error", async () => {
      await click(HubPage.submit());
      await answerAndSubmitTurnoverBreakdownQuestion(1000, 250, 250);

      await expect(await $(TurnoverBreakdownPage.errorNumber(1)).getText()).toBe("Enter answers that add up to £1,000.00");
    });

    it("When I start the breakdown section and enter answers that are equal the total, Then I should be able to get to the section summary and the breakdown section should be marked as 'Completed'", async () => {
      await answerAndSubmitTurnoverBreakdownQuestion(500, 250, 250);
      await answerAndSubmitEmployeeBreakdownQuestion(5, 5);

      await verifyUrlContains(BreakdownSectionSummary.pageName);
      await click(BreakdownSectionSummary.submit());

      await expect(await $(HubPage.summaryRowState(breakdownSectionId)).getText()).toBe("Completed");
    });
  });

  describe("Given I start a grouped answer validation with dependent sections and complete the overview and breakdown sections", () => {
    before(async () => {
      await browser.openQuestionnaire("test_validation_sum_against_total_hub_with_dependent_section.json");

      // Complete overview section
      await answerAndSubmitTotalTurnoverQuestion(1000);
      await answerAndSubmitTotalEmployeesQuestion(10);
      await click(CompanySectionSummary.submit());

      // Complete breakdown section
      await click(HubPage.submit());
      await answerAndSubmitTurnoverBreakdownQuestion(500, 250, 250);
      await answerAndSubmitEmployeeBreakdownQuestion(5, 5);
      await click(BreakdownSectionSummary.submit());

      await expect(await $(HubPage.summaryRowState(breakdownSectionId)).getText()).toBe("Completed");
    });

    it("When I change my answer for the total turnover question, Then the breakdown section should be marked as 'Partially completed'", async () => {
      await $(HubPage.summaryRowLink(companyOverviewSectionID)).click();
      await $(CompanySectionSummary.totalTurnoverAnswerEdit()).click();

      await answerAndSubmitTotalTurnoverQuestion(1500);
      await click(CompanySectionSummary.submit());
      await expect(await $(HubPage.summaryRowState(breakdownSectionId)).getText()).toBe("Partially completed");
    });

    it("When I click 'Continue with section' on the breakdown section, Then I should be taken to the turnover breakdown question and my previous answers should be prefilled", async () => {
      await $(HubPage.summaryRowLink(breakdownSectionId)).click();

      await expect(await $(TurnoverBreakdownPage.turnoverBreakdown1()).getValue()).toBe("500.00");
      await expect(await $(TurnoverBreakdownPage.turnoverBreakdown2()).getValue()).toBe("250.00");
      await expect(await $(TurnoverBreakdownPage.turnoverBreakdown3()).getValue()).toBe("250.00");
    });

    it("When I submit the turnover breakdown question with no changes, Then I should see a validation error", async () => {
      await click(TurnoverBreakdownPage.submit());

      await expect(await $(TurnoverBreakdownPage.errorNumber(1)).getText()).toBe("Enter answers that add up to £1,500.00");
    });

    it("When I update my answers to equal the new total turnover, Then I should be able to get to the section summary and the breakdown section should be marked as 'Completed'", async () => {
      await answerAndSubmitTurnoverBreakdownQuestion(500, 500, 500);

      await verifyUrlContains(BreakdownSectionSummary.pageName);
      await click(BreakdownSectionSummary.submit());
      await expect(await $(HubPage.summaryRowState(breakdownSectionId)).getText()).toBe("Completed");
    });

    it("When I submit the questionnaire, Then I should see the thank you page", async () => {
      await $(HubPage.submit()).scrollIntoView();
      await click(HubPage.submit());
      await verifyUrlContains(ThankYouPage.pageName);
    });
  });
});
