import { CalculatedSummaryTestCase } from "./calculated_summary_test_case.js";
//
// describe("Feature: Calculated Summary", () => {
//   describe("Given I have a Calculated Summary", () => {
//     CalculatedSummaryTestCase.testCase("test_calculated_summary.json");
//   });
//   describe("Given I have a Calculated Summary with the new format", () => {
//     CalculatedSummaryTestCase.testCase("test_new_calculated_summary.json");
//   });
//
//   describe("Given I have a Calculated Summary", () => {
//     CalculatedSummaryTestCase.testCrossSectionDependencies("test_calculated_summary_cross_section_dependencies.json");
//   });
//   describe("Given I have a Calculated Summary with the new format", () => {
//     CalculatedSummaryTestCase.testCrossSectionDependencies("test_new_calculated_summary_cross_section_dependencies.json");
//   });
// });

describe("Feature: Calculated Summary with negative values", () => {
  describe("Given I enter a negative value in the first section", () => {
    CalculatedSummaryTestCase.testNegative("test_calculated_summary.json", -1, 2, 3, 0, "£4.00", ["-£1.00", "£2.00", "£3.00", "£0.00"]);
  });
  describe("Given I enter a negative value in the second section ", () => {
    CalculatedSummaryTestCase.testNegative("test_calculated_summary.json", 12, -2, 1, 0, "£11.00", ["£12.00", "-£2.00", "£1.00", "£0.00"]);
  });
  describe("Given I enter a negative value in the third section ", () => {
    CalculatedSummaryTestCase.testNegative("test_calculated_summary.json", 3, 2, -6, 0, "-£1.00", ["£3.00", "£2.00", "-£6.00", "£0.00"]);
  });
  describe("Given I enter negative values in every currency field ", () => {
    CalculatedSummaryTestCase.testNegative("test_calculated_summary.json", -1, -2, -3, 0, "-£6.00", ["-£1.00", "-£2.00", "-£3.00", "£0.00"]);
  });
});
