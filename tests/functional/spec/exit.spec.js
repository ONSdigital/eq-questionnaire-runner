import HouseholdConfirmationPage from "../generated_pages/thank_you_census_household/household-confirmation.page";
import SummaryPage from "../generated_pages/thank_you_census_household/summary.page";
import CensusThankYouPage from "../base_pages/census-thank-you.page.js";

describe("Post submission exit", () => {
  beforeEach("Load the survey", () => {
    browser.openQuestionnaire("test_thank_you_census_household.json");
  });

  it("Given I click the exit button When I am redirected Then I should see the census homepage", () => {
    $(HouseholdConfirmationPage.submit()).click();
    $(SummaryPage.submit()).click();
    $(CensusThankYouPage.exit()).click();
    expect(browser.getUrl()).to.equal("https://census.gov.uk/");
  });

  it("Given I have clicked the exit button When I navigate back Then I am taken to the session timed out page", () => {
    $(HouseholdConfirmationPage.submit()).click();
    $(SummaryPage.submit()).click();
    $(CensusThankYouPage.exit()).click();
    browser.back();
    expect(browser.getUrl()).to.contain("submitted/thank-you");
    expect($("body").getHTML()).to.contain("This page is no longer available");
  });
});
