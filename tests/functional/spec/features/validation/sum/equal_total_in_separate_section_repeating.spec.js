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
import { click } from "../../../../helpers";
const householderSectionId = "householders-section";
const householdOverviewSectionId = "household-overview-section";
const repeatingSectionId = (repeatIndex) => {
  return `breakdown-section-${repeatIndex}`;
};

const addPersonToHousehold = async (firstName, lastName) => {
  await $(ListCollectorPage.yes()).click();
  await click(ListCollectorPage.submit());
  await $(ListCollectorAddPage.firstName()).setValue(firstName);
  await $(ListCollectorAddPage.lastName()).setValue(lastName);
  await click(ListCollectorAddPage.submit());
};

const answerAndSubmitTotalSpendingQuestion = async (total) => {
  await $(TotalSpendingPage.totalSpending()).setValue(total);
  await click(TotalSpendingPage.submit());
};

const answerAndSubmitEntertainmentSpendingQuestion = async (total) => {
  await $(EntertainmentSpendingPage.entertainmentSpending()).setValue(total);
  await click(EntertainmentSpendingPage.submit());
};

const answerAndSubmitSpendingBreakdownQuestion = async (breakdown1, breakdown2, breakdown3) => {
  await $(SpendingBreakdownPage.spendingBreakdown1()).setValue(breakdown1);
  await $(SpendingBreakdownPage.spendingBreakdown2()).setValue(breakdown2);
  await $(SpendingBreakdownPage.spendingBreakdown3()).setValue(breakdown3);
  await click(SpendingBreakdownPage.submit());
};

const assertSpendingBreakdownAnswer = async (breakdown1, breakdown2, breakdown3) => {
  await expect(await $(SpendingBreakdownPage.spendingBreakdown1()).getValue()).to.equal(breakdown1);
  await expect(await $(SpendingBreakdownPage.spendingBreakdown2()).getValue()).to.equal(breakdown2);
  await expect(await $(SpendingBreakdownPage.spendingBreakdown3()).getValue()).to.equal(breakdown3);
};

const answerAndSubmitEntertainmentBreakdownQuestion = async (breakdown1, breakdown2, breakdown3) => {
  await $(EntertainmentBreakdownPage.secondSpendingBreakdown1()).setValue(breakdown1);
  await $(EntertainmentBreakdownPage.secondSpendingBreakdown2()).setValue(breakdown2);
  await $(EntertainmentBreakdownPage.secondSpendingBreakdown3()).setValue(breakdown3);
  await click(EntertainmentBreakdownPage.submit());
};

const assertRepeatingSectionOnChange = async (repeatIndex, currentBreakdown1, currentBreakdown2, currentBreakdown3, newTotal) => {
  it(`When I click 'Continue with section' on repeating section ${repeatIndex}, Then I should be taken to the spending breakdown question and my previous answers should be prefilled`, async () => {
    await $(HubPage.summaryRowLink(repeatingSectionId(repeatIndex))).click();

    await assertSpendingBreakdownAnswer(currentBreakdown1, currentBreakdown2, currentBreakdown3);
  });

  it("When I submit the spending breakdown question with no changes, Then I should see a validation error", async () => {
    await click(SpendingBreakdownPage.submit());

    await expect(await $(SpendingBreakdownPage.errorNumber(1)).getText()).to.contain(`Enter answers that add up to £${newTotal}`);
  });

  it("When I update my answers to equal the new total spending, Then I should be able to get to the section summary and the breakdown section should be marked as 'Completed'", async () => {
    await answerAndSubmitSpendingBreakdownQuestion(newTotal, 0, 0);

    await expect(await browser.getUrl()).to.contain(BreakdownSectionSummary.pageName);
    await click(BreakdownSectionSummary.submit());
    await expect(await $(HubPage.summaryRowState(repeatingSectionId(repeatIndex))).getText()).to.equal("Completed");
  });
};

describe("Feature: Validation - Sum of grouped answers to equal total (Repeating section) (Total in separate section)", () => {
  describe("Given I start a repeating grouped answer validation with dependent sections and add 2 householders and complete the household overview section", () => {
    before(async () => {
      await browser.openQuestionnaire("test_validation_sum_against_total_repeating_with_dependent_section.json");

      // Add 2 householders
      await addPersonToHousehold("John", "Doe");
      await addPersonToHousehold("Jane", "Doe");
      await $(ListCollectorPage.no()).click();
      await $(ListCollectorPage.submit()).scrollIntoView();
      await click(ListCollectorPage.submit());
      await click(ListCollectorSummaryPage.submit());

      // Complete household overview section
      await answerAndSubmitTotalSpendingQuestion(1000);
      await answerAndSubmitEntertainmentSpendingQuestion(500);
      await click(HouseholdOverviewSectionSummary.submit());

      await expect(await $(HubPage.summaryRowState(householderSectionId)).getText()).to.equal("Completed");
      await expect(await $(HubPage.summaryRowState(householdOverviewSectionId)).getText()).to.equal("Completed");
    });

    it("When I am on the hub, Then the two repeating breakdown sections should be marked as 'Not Started'", async () => {
      await expect(await $(HubPage.summaryRowState(repeatingSectionId(1))).getText()).to.equal("Not started");
      await expect(await $(HubPage.summaryRowState(repeatingSectionId(2))).getText()).to.equal("Not started");
    });

    it("When I start a repeating section and don't skip the calculated question, and enter an answer that is not equal to the total for the spending question, Then I should see a validation error", async () => {
      await $(HubPage.summaryRowLink(repeatingSectionId(1))).click();
      await $(BreakdownDrivingPage.yes()).click();
      await click(BreakdownDrivingPage.submit());

      await answerAndSubmitSpendingBreakdownQuestion(500, 500, 500);

      await expect(await $(SpendingBreakdownPage.errorNumber(1)).getText()).to.contain("Enter answers that add up to £1,000.00");
    });

    it("When I enter an answer that is equal to the total for the spending question, Then I should be able to get to the section summary and the repeating section should be marked as 'Completed'", async () => {
      await answerAndSubmitSpendingBreakdownQuestion(500, 250, 250);
      await answerAndSubmitEntertainmentBreakdownQuestion(250, 150, 100);

      await expect(await browser.getUrl()).to.contain(BreakdownSectionSummary.pageName);
      await click(BreakdownSectionSummary.submit());

      await expect(await $(HubPage.summaryRowState(repeatingSectionId(1))).getText()).to.equal("Completed");
    });

    it("When I start another repeating section and answer 'No' to the driving question, Then I should not have to answer the breakdown question and the section is marked as 'Completed'", async () => {
      await $(HubPage.summaryRowLink(repeatingSectionId(2))).click();
      await $(BreakdownDrivingPage.no()).click();
      await click(BreakdownDrivingPage.submit());

      await expect(await browser.getUrl()).to.contain(BreakdownSectionSummary.pageName);
      await click(BreakdownSectionSummary.submit());

      await expect(await $(HubPage.summaryRowState(repeatingSectionId(2))).getText()).to.equal("Completed");
    });

    it("When I change my answer for the total spending question, Then the first repeating section should be marked as 'Partially completed' and section repeating section should stay as 'Completed'", async () => {
      await $(HubPage.summaryRowLink(householdOverviewSectionId)).click();
      await $(HouseholdOverviewSectionSummary.totalSpendingAnswerEdit()).click();

      await answerAndSubmitTotalSpendingQuestion(1500);
      await click(HouseholdOverviewSectionSummary.submit());
      await expect(await $(HubPage.summaryRowState(repeatingSectionId(1))).getText()).to.equal("Partially completed");

      // The 2nd repeating section skipped the breakdown question, therefore progress should updated for sections that have
      // calculated questions on the path.
      await expect(await $(HubPage.summaryRowState(repeatingSectionId(2))).getText()).to.equal("Completed");
    });

    assertRepeatingSectionOnChange(1, "500.00", "250.00", "250.00", "1,500.00");

    it("When I change my answer to the driving question to 'Yes' for the 2nd repeating section, Then I am able to answer the breakdown question and complete the section", async () => {
      await $(HubPage.summaryRowLink(repeatingSectionId(2))).click();
      await $(BreakdownSectionSummary.breakdownDrivingAnswerEdit()).click();
      await $(BreakdownDrivingPage.yes()).click();
      await click(BreakdownDrivingPage.submit());

      await answerAndSubmitSpendingBreakdownQuestion(1000, 500, 0);
      await answerAndSubmitEntertainmentBreakdownQuestion(250, 150, 100);
      await click(BreakdownSectionSummary.submit());
      await expect(await $(HubPage.summaryRowState(repeatingSectionId(2))).getText()).to.equal("Completed");
    });

    it("When I change my answer for the total spending question, Then both repeating section should be marked as 'Partially completed'", async () => {
      await $(HubPage.summaryRowLink(householdOverviewSectionId)).click();
      await $(HouseholdOverviewSectionSummary.totalSpendingAnswerEdit()).click();

      await answerAndSubmitTotalSpendingQuestion(2500);
      await click(HouseholdOverviewSectionSummary.submit());
      await expect(await $(HubPage.summaryRowState(repeatingSectionId(1))).getText()).to.equal("Partially completed");

      // The 2nd repeating section is now on the path, therefore, its status should have been updated.
      await expect(await $(HubPage.summaryRowState(repeatingSectionId(2))).getText()).to.equal("Partially completed");
    });

    assertRepeatingSectionOnChange(1, "1500.00", "0.00", "0.00", "2,500.00");
    assertRepeatingSectionOnChange(2, "1000.00", "500.00", "0.00", "2,500.00");

    it("When I edit and resubmit the total spending question without changing the value, Then the repeating section's status should stay as 'Completed'", async () => {
      await $(HubPage.summaryRowLink(householdOverviewSectionId)).click();
      await $(HouseholdOverviewSectionSummary.totalSpendingAnswerEdit()).click();

      await expect(await $(TotalSpendingPage.totalSpending()).getValue()).to.equal("2500.00");
      await click(TotalSpendingPage.submit());
      await click(HouseholdOverviewSectionSummary.submit());

      await expect(await $(HubPage.summaryRowState(repeatingSectionId(1))).getText()).to.equal("Completed");
      await expect(await $(HubPage.summaryRowState(repeatingSectionId(2))).getText()).to.equal("Completed");
    });

    it("When I submit the questionnaire, Then I should see the thank you page", async () => {
      await click(HubPage.submit());

      await expect(await browser.getUrl()).to.contain(ThankYouPage.pageName);
    });
  });
});
