import ListCollectorPage from "../../../../generated_pages/validation_sum_against_total_repeating_with_dependent_section/list-collector.page";
import ListCollectorAddPage from "../../../../generated_pages/validation_sum_against_total_repeating_with_dependent_section/list-collector-add.page";
import ListCollectorSummaryPage from "../../../../generated_pages/validation_sum_against_total_repeating_with_dependent_section/householders-section-summary.page";

import TotalSpendingPage from "../../../../generated_pages/validation_sum_against_total_repeating_with_dependent_section/total-spending-block.page";
import HouseholdOverviewSectionSummary from "../../../../generated_pages/validation_sum_against_total_repeating_with_dependent_section/household-overview-section-summary.page";

import BreakdownDrivingPage from "../../../../generated_pages/validation_sum_against_total_repeating_with_dependent_section/breakdown-driving-block.page";
import SpendingBreakdownPage from "../../../../generated_pages/validation_sum_against_total_repeating_with_dependent_section/spending-breakdown-block.page";
import BreakdownSectionSummary from "../../../../generated_pages/validation_sum_against_total_repeating_with_dependent_section/breakdown-section-summary.page";

import HubPage from "../../../../base_pages/hub.page";
import ThankYouPage from "../../../../base_pages/thank-you.page";

const householderSectionId = "householders-section";
const householdOverviewSectionId = "household-overview-section";
const repeatingSectionId = (repeatIndex) => {
  return `breakdown-section-${repeatIndex}`;
};

const addPersonToHousehold = (firstName, lastName) => {
  $(ListCollectorPage.yes()).click();
  $(ListCollectorPage.submit()).click();
  $(ListCollectorAddPage.firstName()).setValue(firstName);
  $(ListCollectorAddPage.lastName()).setValue(lastName);
  $(ListCollectorAddPage.submit()).click();
};

const answerAndSubmitTotalSpendingQuestion = (total) => {
  $(TotalSpendingPage.totalSpending()).setValue(total);
  $(TotalSpendingPage.submit()).click();
};

const answerAndSubmitSpendingBreakdownQuestion = (breakdown1, breakdown2, breakdown3) => {
  $(SpendingBreakdownPage.spendingBreakdown1()).setValue(breakdown1);
  $(SpendingBreakdownPage.spendingBreakdown2()).setValue(breakdown2);
  $(SpendingBreakdownPage.spendingBreakdown3()).setValue(breakdown3);
  $(SpendingBreakdownPage.submit()).click();
};

const assertSpendingBreakdownAnswer = (breakdown1, breakdown2, breakdown3) => {
  expect($(SpendingBreakdownPage.spendingBreakdown1()).getValue()).to.equal(breakdown1);
  expect($(SpendingBreakdownPage.spendingBreakdown2()).getValue()).to.equal(breakdown2);
  expect($(SpendingBreakdownPage.spendingBreakdown3()).getValue()).to.equal(breakdown3);
};

const assertRepeatingSectionOnChange = (repeatIndex, currentBreakdown1, currentBreakdown2, currentBreakdown3, newTotal) => {
  it(`When I click 'Continue with section' on repeating section ${repeatIndex}, Then I should be taken to the spending breakdown question and my previous answers should be prefilled`, () => {
    $(HubPage.summaryRowLink(repeatingSectionId(repeatIndex))).click();

    assertSpendingBreakdownAnswer(currentBreakdown1, currentBreakdown2, currentBreakdown3);
  });

  it("When I submit the spending breakdown question with no changes, Then I should see a validation error", () => {
    $(SpendingBreakdownPage.submit()).click();

    expect($(SpendingBreakdownPage.errorNumber(1)).getText()).to.contain(`Enter answers that add up to £${newTotal}`);
  });

  it("When I update my answers to equal the new total spending, Then I should be able to get to the section summary and the breakdown section should be marked as 'Completed'", () => {
    answerAndSubmitSpendingBreakdownQuestion(newTotal, 0, 0);

    expect(browser.getUrl()).to.contain(BreakdownSectionSummary.pageName);
    $(BreakdownSectionSummary.submit()).click();
    expect($(HubPage.summaryRowState(repeatingSectionId(repeatIndex))).getText()).to.equal("Completed");
  });
};

describe("Feature: Validation - Sum of grouped answers to equal total (Repeating section) (Total in separate section)", () => {
  describe("Given I start a repeating grouped answer validation with dependent sections and add 2 householders and complete the household overview section", () => {
    before(() => {
      browser.openQuestionnaire("test_validation_sum_against_total_repeating_with_dependent_section.json");

      // Add 2 householders
      addPersonToHousehold("John", "Doe");
      addPersonToHousehold("Jane", "Doe");
      $(ListCollectorPage.no()).click();
      $(ListCollectorPage.submit()).click();
      $(ListCollectorSummaryPage.submit()).click();

      // Complete household overview section
      answerAndSubmitTotalSpendingQuestion(1000);
      $(HouseholdOverviewSectionSummary.submit()).click();

      expect($(HubPage.summaryRowState(householderSectionId)).getText()).to.equal("Completed");
      expect($(HubPage.summaryRowState(householdOverviewSectionId)).getText()).to.equal("Completed");
    });

    it("When I am on the hub, Then the two repeating breakdown sections should be marked as 'Not Started'", () => {
      expect($(HubPage.summaryRowState(repeatingSectionId(1))).getText()).to.equal("Not started");
      expect($(HubPage.summaryRowState(repeatingSectionId(2))).getText()).to.equal("Not started");
    });

    it("When I start a repeating section and don't skip the calculated question, and enter an answer that is not equal to the total for the spending question, Then I should see a validation error", () => {
      $(HubPage.summaryRowLink(repeatingSectionId(1))).click();
      $(BreakdownDrivingPage.yes()).click();
      $(BreakdownDrivingPage.submit()).click();

      answerAndSubmitSpendingBreakdownQuestion(500, 500, 500);

      expect($(SpendingBreakdownPage.errorNumber(1)).getText()).to.contain("Enter answers that add up to £1,000.00");
    });

    it("When I enter an answer that is equal to the total for the spending question, Then I should be able to get to the section summary and the repeating section should be marked as 'Completed'", () => {
      answerAndSubmitSpendingBreakdownQuestion(500, 250, 250);

      expect(browser.getUrl()).to.contain(BreakdownSectionSummary.pageName);
      $(BreakdownSectionSummary.submit()).click();

      expect($(HubPage.summaryRowState(repeatingSectionId(1))).getText()).to.equal("Completed");
    });

    it("When I start another repeating section and answer 'No' to the driving question, Then I should not have to answer the breakdown question and the section is marked as 'Completed'", () => {
      $(HubPage.summaryRowLink(repeatingSectionId(2))).click();
      $(BreakdownDrivingPage.no()).click();
      $(BreakdownDrivingPage.submit()).click();

      expect(browser.getUrl()).to.contain(BreakdownSectionSummary.pageName);
      $(BreakdownSectionSummary.submit()).click();

      expect($(HubPage.summaryRowState(repeatingSectionId(2))).getText()).to.equal("Completed");
    });

    it("When I change my answer for the total spending question, Then the first repeating section should be marked as 'Partially completed' and section repeating section should stay as 'Completed'", () => {
      $(HubPage.summaryRowLink(householdOverviewSectionId)).click();
      $(HouseholdOverviewSectionSummary.totalSpendingAnswerEdit()).click();

      answerAndSubmitTotalSpendingQuestion(1500);
      $(HouseholdOverviewSectionSummary.submit()).click();
      expect($(HubPage.summaryRowState(repeatingSectionId(1))).getText()).to.equal("Partially completed");

      // The 2nd repeating section skipped the breakdown question, therefore progress should updated for sections that have
      // calculated questions on the path.
      expect($(HubPage.summaryRowState(repeatingSectionId(2))).getText()).to.equal("Completed");
    });

    assertRepeatingSectionOnChange(1, "500.00", "250.00", "250.00", "1,500.00");

    it("When I change my answer to the driving question to 'Yes' for the 2nd repeating section, Then I am able to answer the breakdown question and complete the section", () => {
      $(HubPage.summaryRowLink(repeatingSectionId(2))).click();
      $(BreakdownSectionSummary.breakdownDrivingAnswerEdit()).click();
      $(BreakdownDrivingPage.yes()).click();
      $(BreakdownDrivingPage.submit()).click();

      answerAndSubmitSpendingBreakdownQuestion(1000, 500, 0);
      $(BreakdownSectionSummary.submit()).click();
      expect($(HubPage.summaryRowState(repeatingSectionId(2))).getText()).to.equal("Completed");
    });

    it("When I change my answer for the total spending question, Then both repeating section should be marked as 'Partially completed'", () => {
      $(HubPage.summaryRowLink(householdOverviewSectionId)).click();
      $(HouseholdOverviewSectionSummary.totalSpendingAnswerEdit()).click();

      answerAndSubmitTotalSpendingQuestion(2500);
      $(HouseholdOverviewSectionSummary.submit()).click();
      expect($(HubPage.summaryRowState(repeatingSectionId(1))).getText()).to.equal("Partially completed");

      // The 2nd repeating section is now on the path, therefore, its status should have been updated.
      expect($(HubPage.summaryRowState(repeatingSectionId(2))).getText()).to.equal("Partially completed");
    });

    assertRepeatingSectionOnChange(1, "1500.00", "0.00", "0.00", "2,500.00");
    assertRepeatingSectionOnChange(2, "1000.00", "500.00", "0.00", "2,500.00");

    it("When I edit and resubmit the total spending question without changing the value, Then the repeating section's status should stay as 'Completed'", () => {
      $(HubPage.summaryRowLink(householdOverviewSectionId)).click();
      $(HouseholdOverviewSectionSummary.totalSpendingAnswerEdit()).click();

      expect($(TotalSpendingPage.totalSpending()).getValue()).to.equal("2500.00");
      $(TotalSpendingPage.submit()).click();
      $(HouseholdOverviewSectionSummary.submit()).click();

      expect($(HubPage.summaryRowState(repeatingSectionId(1))).getText()).to.equal("Completed");
      expect($(HubPage.summaryRowState(repeatingSectionId(2))).getText()).to.equal("Completed");
    });

    it("When I submit the questionnaire, Then I should see the thank you page", () => {
      $(HubPage.submit()).click();

      expect(browser.getUrl()).to.contain(ThankYouPage.pageName);
    });
  });
});
