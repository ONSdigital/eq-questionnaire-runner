import SetMinMax from "../generated_pages/numbers/set-min-max-block.page.js";
import TestMinMax from "../generated_pages/numbers/test-min-max-block.page.js";
import SubmitPage from "../generated_pages/numbers/submit.page";
import IntroductionPage from "../generated_pages/introduction/introduction.page";
import IntroInterstitialPage from "../generated_pages/introduction/general-business-information-completed.page";
import IntroThankYouPagePage from "../base_pages/thank-you.page";
import HouseHolderConfirmationPage from "../generated_pages/thank_you_census_household/household-confirmation.page";
import { getRandomString } from "../jwt_helper";

describe("Save sign out / Exit", () => {
  const responseId = getRandomString(16);

  it("Given I am on an introduction page, when I click the exit button, then I am redirected to sign out page and my session is cleared", () => {
    browser.openQuestionnaire("test_introduction.json");
    $(IntroductionPage.exitButton()).click();

    expect(browser.getUrl()).to.contain("/sign-in/logout");

    browser.back();
    expect($("body").getHTML()).to.contain("Sorry, you need to sign in again");
  });

  it("Given I am completing a questionnaire, when I select save and sign out, then I am redirected to sign out page and my session is cleared", () => {
    browser.openQuestionnaire("test_numbers.json", { userId: "test_user", responseId });
    $(SetMinMax.setMinimum()).setValue("10");
    $(SetMinMax.setMaximum()).setValue("1020");
    $(SetMinMax.submit()).click();
    $(TestMinMax.saveSignOut()).click();

    expect(browser.getUrl()).to.contain("/sign-in/logout");

    browser.back();
    expect($("body").getHTML()).to.contain("Sorry, you need to sign in again");
  });

  it("Given I have started a questionnaire, when I return to the questionnaire, then I am returned to the page I was on and can then complete the questionnaire", () => {
    browser.openQuestionnaire("test_numbers.json", { userId: "test_user", responseId });

    $(TestMinMax.testRange()).setValue("10");
    $(TestMinMax.testMin()).setValue("123");
    $(TestMinMax.testMax()).setValue("1000");
    $(TestMinMax.testPercent()).setValue("100");
    $(TestMinMax.submit()).click();

    $(SubmitPage.submit()).click();
    expect(browser.getUrl()).to.contain("thank-you");
  });

  it("Given a business questionnaire, when I navigate the questionnaire, then I see the correct sign out buttons", () => {
    browser.openQuestionnaire("test_introduction.json");

    expect($(IntroductionPage.exitButton()).getText()).to.contain("Exit");
    $(IntroductionPage.getStarted()).click();

    expect($(IntroInterstitialPage.saveSignOut()).getText()).to.contain("Save and sign out");
    $(IntroInterstitialPage.submit()).click();

    expect($(SubmitPage.saveSignOut()).getText()).to.contain("Save and sign out");
    $(SubmitPage.submit()).click();

    expect($(IntroThankYouPagePage.exitButton()).isExisting()).to.be.false;
  });

  it("Given a Census questionnaire, when I navigate the questionnaire, then I see the correct sign out buttons", () => {
    browser.openQuestionnaire("test_thank_you_census_household.json");

    expect($(HouseHolderConfirmationPage.saveSignOut()).getText()).to.contain("Save and complete later");
    $(HouseHolderConfirmationPage.submit()).click();

    expect($(SubmitPage.saveSignOut()).getText()).to.contain("Save and complete later");
  });
});
