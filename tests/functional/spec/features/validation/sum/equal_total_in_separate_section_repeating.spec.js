import ListCollectorPage from "../../../../generated_pages/validation_sum_against_total_repeating_with_dependent_section/list-collector.page";
import ListCollectorAddPage from "../../../../generated_pages/validation_sum_against_total_repeating_with_dependent_section/list-collector-add.page";
import ListCollectorSummaryPage from "../../../../generated_pages/validation_sum_against_total_repeating_with_dependent_section/householders-section-summary.page";

import TotalSpendingPage from "../../../../generated_pages/validation_sum_against_total_repeating_with_dependent_section/total-spending-block.page";
import EntertainmentSpendingPage from "../../../../generated_pages/validation_sum_against_total_repeating_with_dependent_section/entertainment-spending-block.page";
import HouseholdOverviewSectionSummary from "../../../../generated_pages/validation_sum_against_total_repeating_with_dependent_section/household-overview-section-summary.page";

import BreakdownDrivingPage from "../../../../generated_pages/validation_sum_against_total_repeating_with_dependent_section/breakdown-driving-block.page";
import SpendingBreakdownPage from "../../../../generated_pages/validation_sum_against_total_repeating_with_dependent_section/spending-breakdown-block.page";
import EntertainmentBreakdownPage from "../../../../generated_pages/validation_sum_against_total_repeating_with_dependent_section/second-spending-breakdown-block.page";
import BreakdownSectionSummary from "../../../../generated_pages/validation_sum_against_total_repeating_with_dependent_section/breakdown-section-summary.page";

import HubPage from "../../../../base_pages/hub.page";
import ThankYouPage from "../../../../base_pages/thank-you.page";

const householderSectionId = "householders-section";
const householdOverviewSectionId = "household-overview-section";
const repeatingSectionId = async (repeatIndex) => {
  return `breakdown-section-${repeatIndex}`;
};

const addPersonToHousehold = async (firstName, lastName) => {
  await $(await ListCollectorPage.yes()).click();
  await $(await ListCollectorPage.submit()).click();
  await $(await ListCollectorAddPage.firstName()).setValue(firstName);
  await $(await ListCollectorAddPage.lastName()).setValue(lastName);
  await $(await ListCollectorAddPage.submit()).click();
};

const answerAndSubmitTotalSpendingQuestion = async (total) => {
  await $(await TotalSpendingPage.totalSpending()).setValue(total);
  await $(await TotalSpendingPage.submit()).click();
};

const answerAndSubmitEntertainmentSpendingQuestion = async (total) => {
  await $(await EntertainmentSpendingPage.entertainmentSpending()).setValue(total);
  await $(await EntertainmentSpendingPage.submit()).click();
};

const answerAndSubmitSpendingBreakdownQuestion = async (breakdown1, breakdown2, breakdown3) => {
  await $(await SpendingBreakdownPage.spendingBreakdown1()).setValue(breakdown1);
  await $(await SpendingBreakdownPage.spendingBreakdown2()).setValue(breakdown2);
  await $(await SpendingBreakdownPage.spendingBreakdown3()).setValue(breakdown3);
  await $(await SpendingBreakdownPage.submit()).click();
};

const assertSpendingBreakdownAnswer = async (breakdown1, breakdown2, breakdown3) => {
  await expect(await $(await SpendingBreakdownPage.spendingBreakdown1()).getValue()).to.equal(breakdown1);
  await expect(await $(await SpendingBreakdownPage.spendingBreakdown2()).getValue()).to.equal(breakdown2);
  await expect(await $(await SpendingBreakdownPage.spendingBreakdown3()).getValue()).to.equal(breakdown3);
};

const answerAndSubmitEntertainmentBreakdownQuestion = async (breakdown1, breakdown2, breakdown3) => {
  await $(await EntertainmentBreakdownPage.secondSpendingBreakdown1()).setValue(breakdown1);
  await $(await EntertainmentBreakdownPage.secondSpendingBreakdown2()).setValue(breakdown2);
  await $(await EntertainmentBreakdownPage.secondSpendingBreakdown3()).setValue(breakdown3);
  await $(await EntertainmentBreakdownPage.submit()).click();
};

const assertRepeatingSectionOnChange = async (repeatIndex, currentBreakdown1, currentBreakdown2, currentBreakdown3, newTotal) => {
  it(`When I click 'Continue with section' on repeating section ${repeatIndex}, Then I should be taken to the spending breakdown question and my previous answers should be prefilled`, async ()=> {
    await $(await HubPage.summaryRowLink(repeatingSectionId(repeatIndex))).click();

    assertSpendingBreakdownAnswer(currentBreakdown1, currentBreakdown2, currentBreakdown3);
  });

  it("When I submit the spending breakdown question with no changes, Then I should see a validation error", async ()=> {
    await $(await SpendingBreakdownPage.submit()).click();

    await expect(await $(await SpendingBreakdownPage.errorNumber(1)).getText()).to.contain(`Enter answers that add up to £${newTotal}`);
  });

  it("When I update my answers to equal the new total spending, Then I should be able to get to the section summary and the breakdown section should be marked as 'Completed'", async ()=> {
    answerAndSubmitSpendingBreakdownQuestion(newTotal, 0, 0);

    await expect(browser.getUrl()).to.contain(BreakdownSectionSummary.pageName);
    await $(await BreakdownSectionSummary.submit()).click();
    await expect(await $(await HubPage.summaryRowState(repeatingSectionId(repeatIndex))).getText()).to.equal("Completed");
  });
};

describe("Feature: Validation - Sum of grouped answers to equal total (Repeating section) (Total in separate section)", () => {
  describe("Given I start a repeating grouped answer validation with dependent sections and add 2 householders and complete the household overview section", () => {
    before(async ()=> {
      await browser.openQuestionnaire("test_validation_sum_against_total_repeating_with_dependent_section.json");

      // Add 2 householders
      addPersonToHousehold("John", "Doe");
      addPersonToHousehold("Jane", "Doe");
      await $(await ListCollectorPage.no()).click();
      await $(await ListCollectorPage.submit()).click();
      await $(await ListCollectorSummaryPage.submit()).click();

      // Complete household overview section
      answerAndSubmitTotalSpendingQuestion(1000);
      answerAndSubmitEntertainmentSpendingQuestion(500);
      await $(await HouseholdOverviewSectionSummary.submit()).click();

      await expect(await $(await HubPage.summaryRowState(householderSectionId)).getText()).to.equal("Completed");
      await expect(await $(await HubPage.summaryRowState(householdOverviewSectionId)).getText()).to.equal("Completed");
    });

    it("When I am on the hub, Then the two repeating breakdown sections should be marked as 'Not Started'", async ()=> {
      await expect(await $(await HubPage.summaryRowState(repeatingSectionId(1))).getText()).to.equal("Not started");
      await expect(await $(await HubPage.summaryRowState(repeatingSectionId(2))).getText()).to.equal("Not started");
    });

    it("When I start a repeating section and don't skip the calculated question, and enter an answer that is not equal to the total for the spending question, Then I should see a validation error", async ()=> {
      await $(await HubPage.summaryRowLink(repeatingSectionId(1))).click();
      await $(await BreakdownDrivingPage.yes()).click();
      await $(await BreakdownDrivingPage.submit()).click();

      answerAndSubmitSpendingBreakdownQuestion(500, 500, 500);

      await expect(await $(await SpendingBreakdownPage.errorNumber(1)).getText()).to.contain("Enter answers that add up to £1,000.00");
    });

    it("When I enter an answer that is equal to the total for the spending question, Then I should be able to get to the section summary and the repeating section should be marked as 'Completed'", async ()=> {
      answerAndSubmitSpendingBreakdownQuestion(500, 250, 250);
      answerAndSubmitEntertainmentBreakdownQuestion(250, 150, 100);

      await expect(browser.getUrl()).to.contain(BreakdownSectionSummary.pageName);
      await $(await BreakdownSectionSummary.submit()).click();

      await expect(await $(await HubPage.summaryRowState(repeatingSectionId(1))).getText()).to.equal("Completed");
    });

    it("When I start another repeating section and answer 'No' to the driving question, Then I should not have to answer the breakdown question and the section is marked as 'Completed'", async ()=> {
      await $(await HubPage.summaryRowLink(repeatingSectionId(2))).click();
      await $(await BreakdownDrivingPage.no()).click();
      await $(await BreakdownDrivingPage.submit()).click();

      await expect(browser.getUrl()).to.contain(BreakdownSectionSummary.pageName);
      await $(await BreakdownSectionSummary.submit()).click();

      await expect(await $(await HubPage.summaryRowState(repeatingSectionId(2))).getText()).to.equal("Completed");
    });

    it("When I change my answer for the total spending question, Then the first repeating section should be marked as 'Partially completed' and section repeating section should stay as 'Completed'", async ()=> {
      await $(await HubPage.summaryRowLink(householdOverviewSectionId)).click();
      await $(await HouseholdOverviewSectionSummary.totalSpendingAnswerEdit()).click();

      answerAndSubmitTotalSpendingQuestion(1500);
      await $(await HouseholdOverviewSectionSummary.submit()).click();
      await expect(await $(await HubPage.summaryRowState(repeatingSectionId(1))).getText()).to.equal("Partially completed");

      // The 2nd repeating section skipped the breakdown question, therefore progress should updated for sections that have
      // calculated questions on the path.
      await expect(await $(await HubPage.summaryRowState(repeatingSectionId(2))).getText()).to.equal("Completed");
    });

    assertRepeatingSectionOnChange(1, "500.00", "250.00", "250.00", "1,500.00");

    it("When I change my answer to the driving question to 'Yes' for the 2nd repeating section, Then I am able to answer the breakdown question and complete the section", async ()=> {
      await $(await HubPage.summaryRowLink(repeatingSectionId(2))).click();
      await $(await BreakdownSectionSummary.breakdownDrivingAnswerEdit()).click();
      await $(await BreakdownDrivingPage.yes()).click();
      await $(await BreakdownDrivingPage.submit()).click();

      answerAndSubmitSpendingBreakdownQuestion(1000, 500, 0);
      answerAndSubmitEntertainmentBreakdownQuestion(250, 150, 100);
      await $(await BreakdownSectionSummary.submit()).click();
      await expect(await $(await HubPage.summaryRowState(repeatingSectionId(2))).getText()).to.equal("Completed");
    });

    it("When I change my answer for the total spending question, Then both repeating section should be marked as 'Partially completed'", async ()=> {
      await $(await HubPage.summaryRowLink(householdOverviewSectionId)).click();
      await $(await HouseholdOverviewSectionSummary.totalSpendingAnswerEdit()).click();

      answerAndSubmitTotalSpendingQuestion(2500);
      await $(await HouseholdOverviewSectionSummary.submit()).click();
      await expect(await $(await HubPage.summaryRowState(repeatingSectionId(1))).getText()).to.equal("Partially completed");

      // The 2nd repeating section is now on the path, therefore, its status should have been updated.
      await expect(await $(await HubPage.summaryRowState(repeatingSectionId(2))).getText()).to.equal("Partially completed");
    });

    assertRepeatingSectionOnChange(1, "1500.00", "0.00", "0.00", "2,500.00");
    assertRepeatingSectionOnChange(2, "1000.00", "500.00", "0.00", "2,500.00");

    it("When I edit and resubmit the total spending question without changing the value, Then the repeating section's status should stay as 'Completed'", async ()=> {
      await $(await HubPage.summaryRowLink(householdOverviewSectionId)).click();
      await $(await HouseholdOverviewSectionSummary.totalSpendingAnswerEdit()).click();

      await expect(await $(await TotalSpendingPage.totalSpending()).getValue()).to.equal("2500.00");
      await $(await TotalSpendingPage.submit()).click();
      await $(await HouseholdOverviewSectionSummary.submit()).click();

      await expect(await $(await HubPage.summaryRowState(repeatingSectionId(1))).getText()).to.equal("Completed");
      await expect(await $(await HubPage.summaryRowState(repeatingSectionId(2))).getText()).to.equal("Completed");
    });

    it("When I submit the questionnaire, Then I should see the thank you page", async ()=> {
      await $(await HubPage.submit()).click();

      await expect(browser.getUrl()).to.contain(ThankYouPage.pageName);
    });
  });
});
