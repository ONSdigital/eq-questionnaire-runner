import EmploymentStatusBlockPage from "../../../generated_pages/hub_and_spoke/employment-status.page.js";
import EmploymentTypeBlockPage from "../../../generated_pages/hub_and_spoke/employment-type.page.js";
import HouseholdSummary from "../../../generated_pages/hub_and_spoke/household-section-summary.page.js";
import HowManyPeopleLiveHere from "../../../generated_pages/hub_and_spoke/how-many-people-live-here.page.js";
import ProxyPage from "../../../generated_pages/hub_and_spoke/proxy.page.js";
import AccomodationDetailsSummaryBlockPage from "../../../generated_pages/hub_and_spoke/accommodation-section-summary.page.js";
import DoesAnyoneLiveHere from "../../../generated_pages/hub_and_spoke/does-anyone-live-here.page.js";
import Relationships from "../../../generated_pages/hub_and_spoke/relationships.page.js";
import RelationshipsSummary from "../../../generated_pages/hub_and_spoke/relationships-section-summary.page.js";
import HubPage from "../../../base_pages/hub.page.js";

describe("Feature: Hub and Spoke", () => {
  const hubAndSpokeSchema = "test_hub_and_spoke.json";

  it("When a user first views the Hub, The Hub should be in a continue state", () => {
    browser.openQuestionnaire(hubAndSpokeSchema);
    expect($(HubPage.submit()).getText()).to.contain("Continue");
    expect($(HubPage.displayedName()).getText()).to.contain("Choose another section to complete");
    expect($(HubPage.summaryRowState(1)).getText()).to.contain("Not started");
    expect($(HubPage.summaryRowState(2)).getText()).to.contain("Not started");
  });

  it("When a user views the Hub, any section with show_on_hub set to true should appear", () => {
    browser.openQuestionnaire(hubAndSpokeSchema);
    expect($(HubPage.summaryItems()).getText()).to.contain("Employment");
    expect($(HubPage.summaryItems()).getText()).to.contain("Accommodation");
    expect($(HubPage.summaryItems()).getText()).to.contain("Household residents");
  });

  it("When a user views the Hub, any section with show_on_hub set to false should not appear", () => {
    browser.openQuestionnaire(hubAndSpokeSchema);
    expect($(HubPage.summaryItems()).getText()).not.to.contain("Relationships");
  });

  describe("Given a user is on the Hub page", () => {
    it("When the user click the 'Save and sign out' button then they should be on the signed out page", () => {
      browser.openQuestionnaire(hubAndSpokeSchema);

      $(HubPage.saveSignOut()).click();

      const expectedUrl = browser.getUrl();

      expect(expectedUrl).to.contain("/signed-out");
    });
  });

  describe("Given a user has not started a section", () => {
    beforeEach("Open survey", () => {
      browser.openQuestionnaire(hubAndSpokeSchema);
      expect($(HubPage.summaryRowState(1)).getText()).to.contain("Not started");
      expect($(HubPage.summaryRowState(2)).getText()).to.contain("Not started");
    });

    it("When the user starts a section, Then the first question in the section should be displayed", () => {
      $(HubPage.submit()).click();
      const expectedUrl = browser.getUrl();
      expect(expectedUrl).to.contain(EmploymentStatusBlockPage.url());
    });

    it("When the user starts a section and clicks the Previous link on the first question, Then they should be taken back to the Hub", () => {
      $(HubPage.submit()).click();
      $(EmploymentStatusBlockPage.previous()).click();
      const expectedUrl = browser.getUrl();
      expect(expectedUrl).to.contain(HubPage.url());
    });
  });

  describe("Given a user has started a section", () => {
    before("Start section", () => {
      browser.openQuestionnaire(hubAndSpokeSchema);
      $(HubPage.summaryRowLink(1)).click();
      $(EmploymentStatusBlockPage.exclusiveNoneOfTheseApply()).click();
      $(EmploymentStatusBlockPage.submit()).click();
    });

    it("When the user returns to the Hub, Then the Hub should be in a continue state", () => {
      browser.url(HubPage.url());
      expect($(HubPage.submit()).getText()).to.contain("Continue");
      expect($(HubPage.displayedName()).getText()).to.contain("Choose another section to complete");
    });

    it("When the user returns to the Hub, Then the section should be marked as 'Partially completed'", () => {
      browser.url(HubPage.url());
      expect($(HubPage.summaryRowState(1)).getText()).to.contain("Partially completed");
    });

    it("When the user returns to the Hub and restarts the same section, Then they should be redirected to the first incomplete block", () => {
      browser.url(HubPage.url());
      $(HubPage.summaryRowLink(1)).click();
      const expectedUrl = browser.getUrl();
      expect(expectedUrl).to.contain(EmploymentTypeBlockPage.url());
    });
  });

  describe("Given a user has completed a section", () => {
    beforeEach("Complete section", () => {
      browser.openQuestionnaire(hubAndSpokeSchema);
      $(HubPage.summaryRowLink(1)).click();
      $(EmploymentStatusBlockPage.exclusiveNoneOfTheseApply()).click();
      $(EmploymentStatusBlockPage.submit()).click();
      $(EmploymentTypeBlockPage.studying()).click();
    });

    it("When the user clicks the 'Continue' button, it should return them to the hub", () => {
      $(EmploymentTypeBlockPage.submit()).click();
      const expectedUrl = browser.getUrl();
      expect(expectedUrl).to.contain(HubPage.url());
    });

    it("When the user returns to the Hub, Then the Hub should be in a continue state", () => {
      $(EmploymentTypeBlockPage.submit()).click();
      expect($(HubPage.submit()).getText()).to.contain("Continue");
      expect($(HubPage.displayedName()).getText()).to.contain("Choose another section to complete");
    });

    it("When the user returns to the Hub, Then the section should be marked as 'Completed'", () => {
      $(EmploymentTypeBlockPage.submit()).click();
      expect($(HubPage.summaryRowState(1)).getText()).to.contain("Completed");

      expect($(HubPage.summaryRowTitle(1)).getAttribute("class")).to.contain("summary__item-title--has-icon");
    });

    it("When the user returns to the Hub and clicks the 'View answers' link on the Hub, if this no summary they are returned to the first block", () => {
      $(EmploymentTypeBlockPage.submit()).click();
      $(HubPage.summaryRowLink(1)).click();
      const expectedUrl = browser.getUrl();
      expect(expectedUrl).to.contain(EmploymentStatusBlockPage.url());
    });

    it("When the user returns to the Hub and continues, Then they should progress to the next section", () => {
      $(EmploymentTypeBlockPage.submit()).click();
      expect(browser.getUrl()).to.contain(HubPage.url());
      $(HubPage.submit()).click();
      const expectedUrl = browser.getUrl();
      expect(expectedUrl).to.contain(ProxyPage.url());
    });
  });

  describe("Given a user has completed a section and is on the Hub page", () => {
    beforeEach("Complete section", () => {
      browser.openQuestionnaire(hubAndSpokeSchema);
      $(HubPage.summaryRowLink(1)).click();
      $(EmploymentStatusBlockPage.workingAsAnEmployee()).click();
      $(EmploymentStatusBlockPage.submit()).click();

      expect($(HubPage.summaryRowState(1)).getText()).to.contain("Completed");
      expect($(HubPage.summaryRowTitle(1)).getAttribute("class")).to.contain("summary__item-title--has-icon");
    });

    it("When the user clicks the 'View answers' link and incompletes the section, Then they the should be taken to the next incomplete question on 'Continue", () => {
      $(HubPage.summaryRowLink(1)).click();
      expect(browser.getUrl()).to.contain(EmploymentStatusBlockPage.url());
      $(EmploymentStatusBlockPage.exclusiveNoneOfTheseApply()).click();
      $(EmploymentStatusBlockPage.submit()).click();
      const expectedUrl = browser.getUrl();
      expect(expectedUrl).to.contain(EmploymentTypeBlockPage.url());
    });

    it("When the user clicks the 'View answers' link and incompletes the section and returns to the hub, Then the section should be marked as 'Partially completed'", () => {
      $(HubPage.summaryRowLink(1)).click();
      expect(browser.getUrl()).to.contain(EmploymentStatusBlockPage.url());
      $(EmploymentStatusBlockPage.exclusiveNoneOfTheseApply()).click();
      $(EmploymentStatusBlockPage.submit()).click();
      browser.url(HubPage.url());
      const expectedUrl = browser.getUrl();
      expect(expectedUrl).to.contain(HubPage.url());
      expect($(HubPage.summaryRowState(1)).getText()).to.contain("Partially completed");
      expect($(HubPage.summaryRowTitle(1)).getAttribute("class")).not.to.contain("summary__item-title--has-icon");
    });
  });

  describe("Given a user has completed all sections", () => {
    beforeEach("Complete all sections", () => {
      browser.openQuestionnaire(hubAndSpokeSchema);
      $(HubPage.summaryRowLink(1)).click();
      $(EmploymentStatusBlockPage.exclusiveNoneOfTheseApply()).click();
      $(EmploymentStatusBlockPage.submit()).click();
      $(EmploymentTypeBlockPage.studying()).click();
      $(EmploymentTypeBlockPage.submit()).click();
      $(HubPage.submit()).click();
      $(ProxyPage.yes()).click();
      $(ProxyPage.submit()).click();
      $(AccomodationDetailsSummaryBlockPage.submit()).click();
      $(HubPage.submit()).click();
      $(DoesAnyoneLiveHere.no()).click();
      $(DoesAnyoneLiveHere.submit()).click();
      $(HouseholdSummary.submit()).click();
      $(HubPage.submit()).click();
      $(Relationships.yes()).click();
      $(Relationships.submit()).click();
      $(RelationshipsSummary.submit()).click();
    });

    it("It should return them to the hub", () => {
      const expectedUrl = browser.getUrl();
      expect(expectedUrl).to.contain(HubPage.url());
    });

    it("When the user returns to the Hub, Then the Hub should be in a completed state", () => {
      expect($(HubPage.submit()).getText()).to.contain("Submit survey");
      expect($(HubPage.displayedName()).getText()).to.contain("Submit survey");
    });

    it("When the user submits, it should show the thankyou page", () => {
      $(HubPage.submit()).click();
      const expectedUrl = browser.getUrl();
      expect(expectedUrl).to.contain("thank-you");
    });
  });

  describe("Given a user opens a schema with required sections", () => {
    beforeEach("Load survey", () => {
      browser.openQuestionnaire("test_hub_complete_sections.json");
    });

    it("The hub should not show first of all", () => {
      expect(browser.getUrl()).to.contain(EmploymentStatusBlockPage.url());
    });

    it("The hub should only display when required sections are complete", () => {
      $(EmploymentStatusBlockPage.exclusiveNoneOfTheseApply()).click();
      $(EmploymentStatusBlockPage.submit()).click();
      $(EmploymentTypeBlockPage.studying()).click();
      $(EmploymentTypeBlockPage.submit()).click();
      expect(browser.getUrl()).to.contain(HubPage.url());
    });
  });

  describe("Given a section is complete and the user has been returned to a section summary by clicking the 'View answers' link ", () => {
    beforeEach("Complete section", () => {
      browser.openQuestionnaire(hubAndSpokeSchema);
      $(HubPage.summaryRowLink(3)).click();
      $(DoesAnyoneLiveHere.no()).click();
      $(DoesAnyoneLiveHere.submit()).click();
      $(HouseholdSummary.submit()).click();
    });

    it("When there are no changes, continue returns directly to the hub", () => {
      $(HubPage.summaryRowLink(3)).click();
      $(HouseholdSummary.submit()).click();
      const expectedUrl = browser.getUrl();
      expect(expectedUrl).to.contain(HubPage.url());
    });

    it("When there are changes, which would set the section to in_progress it routes accordingly", () => {
      $(HubPage.summaryRowLink(3)).click();
      $(HouseholdSummary.doesAnyoneLiveHereAnswerEdit()).click();
      $(DoesAnyoneLiveHere.yes()).click();
      $(DoesAnyoneLiveHere.submit()).click();
      $(HouseholdSummary.submit()).click();
      const expectedUrl = browser.getUrl();
      expect(expectedUrl).to.contain(HowManyPeopleLiveHere.url());
    });
  });
});
