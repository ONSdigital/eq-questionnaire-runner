import CensusThankYouPage from "../base_pages/census-thank-you.page.js";
import HubPage from "../base_pages/hub.page";
import { SubmitPage } from "../base_pages/submit.page.js";
import { click } from "../helpers";

describe("Post submission exit", () => {
  beforeEach("Load the survey", async () => {
    await browser.openQuestionnaire("test_thank_you_census_household.json");
  });

  it("Given I click the exit button from the thank you page which has no session cookie, When I am redirected, Then I should be redirected to the correct log out url", async () => {
    await click(SubmitPage.submit());
    await click(HubPage.submit());
    await browser.deleteAllCookies();
    await $(CensusThankYouPage.exit()).click();
    await expect(await browser.getUrl()).toBe("https://surveys.ons.gov.uk/sign-in/");
  });

  it("Given I click the exit button from the thank you page, When I am redirected, Then I should be redirected to the correct log out url", async () => {
    await click(SubmitPage.submit());
    await click(HubPage.submit());
    await $(CensusThankYouPage.exit()).click();
    await expect(await browser.getUrl()).toBe("https://www.ons.gov.uk/census");
  });

  it("Given I have clicked the exit button, When I navigate back, Then I am taken to the session timed out page", async () => {
    await click(SubmitPage.submit());
    await click(HubPage.submit());
    await $(CensusThankYouPage.exit()).click();
    await browser.back();
    await expect(await browser.getUrl()).toContain("submitted/thank-you");
    await expect(await $("body").getHTML()).toContain("Sorry, you need to sign in again");
  });
});
