import CensusThankYouPage from "../base_pages/census-thank-you.page.js";
import HouseholdConfirmationPage from "../base_pages/confirmation.page.js";
import HubPage from "../base_pages/hub.page";

const CENSUS_EN_BASE_URL = "https://census.gov.uk/";

describe("Post submission exit", () => {
  beforeEach("Load the survey", () => {
    browser.openQuestionnaire("test_thank_you_census_household.json");
  });

  it("Given I click the exit button from the thank you page which has no session cookie, When I am redirected, Then I should see the census homepage", () => {
    $(HouseholdConfirmationPage.submit()).click();
    $(HubPage.submit()).click();
    browser.deleteAllCookies();
    $(CensusThankYouPage.exit()).click();
    expect(browser.getUrl()).to.equal(CENSUS_EN_BASE_URL);
  });

  it("Given I click the exit button from the thank you page, When I am redirected, Then I should see the census homepage", () => {
    $(HouseholdConfirmationPage.submit()).click();
    $(HubPage.submit()).click();
    $(CensusThankYouPage.exit()).click();
    expect(browser.getUrl()).to.equal(CENSUS_EN_BASE_URL);
  });

  it("Given I have clicked the exit button, When I navigate back, Then I am taken to the session timed out page", () => {
    $(HouseholdConfirmationPage.submit()).click();
    $(HubPage.submit()).click();
    $(CensusThankYouPage.exit()).click();
    browser.back();
    expect(browser.getUrl()).to.contain("submitted/thank-you");
    expect($("body").getHTML()).to.contain("This page is no longer available");
  });
});
