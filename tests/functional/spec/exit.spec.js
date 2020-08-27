import HouseholdConfirmationPage from "../generated_pages/thank_you_census_household/household-confirmation.page";
import SummaryPage from "../generated_pages/thank_you_census_household/summary.page";
import CensusThankYouPage from "../base_pages/census-thank-you.js";

describe("Post submission exit", () => {
  beforeEach("Load the survey", () => {
    browser.openQuestionnaire("test_thank_you_census_household.json");
  });

  it("Given the survey is submitted, when I view the thank you page, the exit button should contain a log_out_url query param containing the census homepage url", () => {
    $(HouseholdConfirmationPage.submit()).click();
    $(SummaryPage.submit()).click();
    expect($(CensusThankYouPage.exit()).getHTML()).to.contain("sign_out_url=https%3A%2F%2Fcensus.gov.uk%2F");
  });

  it("Given I click the exit button, when I am redirected I should see the census homepage", () => {
    $(HouseholdConfirmationPage.submit()).click();
    $(SummaryPage.submit()).click();
    $(CensusThankYouPage.exit()).click();
    expect(browser.getUrl()).to.equal("https://census.gov.uk/");
  });

  it("Given I have clicked the exit button, when I navigate back I am taken to the session expired page", () => {
    $(HouseholdConfirmationPage.submit()).click();
    $(SummaryPage.submit()).click();
    $(CensusThankYouPage.exit()).click();
    browser.back();
    expect(browser.getUrl()).to.contain("submitted/thank-you");
    expect($("body").getHTML()).to.contain("Your session has expired");
  });
});
