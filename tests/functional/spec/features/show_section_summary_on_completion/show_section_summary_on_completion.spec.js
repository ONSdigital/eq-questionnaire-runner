import employmentStatusBlockPage from "../../../generated_pages/show_section_summary_on_completion/employment-status.page";
import employmentSectionSummary from "../../../generated_pages/show_section_summary_on_completion/employment-section-summary.page";

import proxyQuestionPage from "../../../generated_pages/show_section_summary_on_completion/proxy.page";
import accommodationSectionSummary from "../../../generated_pages/show_section_summary_on_completion/accommodation-section-summary.page";

import hubPage from "../../../base_pages/hub.page.js";

describe("Feature: Show section summary on completion", () => {
  before("Launch survey", () => {
    browser.openQuestionnaire("test_show_section_summary_on_completion.json");
  });

  describe("Given I am completing a section with the summary turned off for the forward journey", () => {
    it("When I reach the end of that section, Then I go straight to the hub", () => {
      $(employmentStatusBlockPage.workingAsAnEmployee()).click();
      $(employmentStatusBlockPage.submit()).click();

      expect(browser.getUrl()).to.contain(hubPage.url());
    });
  });

  describe("Given I have completed a section with the summary turned off for the forward journey", () => {
    it("When I return to a completed section from the hub, Then I am returned to that section summary", () => {
      $(hubPage.summaryRowLink("employment-section")).click();

      expect(browser.getUrl()).to.contain(employmentSectionSummary.url());
    });
  });

  describe("Given I am completing a section with the summary turned on for the forward journey", () => {
    before("Get to hub", () => {
      browser.url(hubPage.url());
    });

    it("When I reach the end of that section, Then I will be taken to the section summary to enable me to amend an answer", () => {
      $(hubPage.summaryRowLink("accommodation-section")).click();
      $(proxyQuestionPage.noIMAnsweringForMyself()).click();
      $(proxyQuestionPage.submit()).click();

      expect(browser.getUrl()).to.contain(accommodationSectionSummary.url());
    });
  });

  describe("Given I have completed a section with the summary turned on for the forward journey", () => {
    before("Get to hub", () => {
      browser.url(hubPage.url());
    });

    it("When I return to a completed section from the hub, Then I am returned to the correct section summary", () => {
      $(hubPage.summaryRowLink("accommodation-section")).click();

      expect(browser.getUrl()).to.contain(accommodationSectionSummary.url());
    });
  });
});
