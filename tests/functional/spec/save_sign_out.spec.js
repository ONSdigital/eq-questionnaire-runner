import SetMinMax from "../generated_pages/numbers/set-min-max-block.page.js";
import TestMinMax from "../generated_pages/numbers/test-min-max-block.page.js";
import DetailAnswer from "../generated_pages/numbers/detail-answer-block.page";
import SubmitPage from "../generated_pages/numbers/submit.page";
import IntroductionPage from "../generated_pages/introduction/introduction.page";
import IntroInterstitialPage from "../generated_pages/introduction/general-business-information-completed.page";
import IntroThankYouPagePage from "../base_pages/thank-you.page";
import HouseHolderConfirmationPage from "../generated_pages/thank_you_census_household/household-confirmation.page";
import currencyBlock from "../generated_pages/variants_question/currency-block.page.js";
import firstNumberBlock from "../generated_pages/variants_question/first-number-block.page.js";
import secondNumberBlock from "../generated_pages/variants_question/second-number-block.page.js";
import currencySectionSummary from "../generated_pages/variants_question/currency-section-summary.page.js";
import { getRandomString } from "../jwt_helper";
import { click } from "../helpers";
describe("Save sign out / Exit", () => {
  const responseId = getRandomString(16);

  it("Given I am on an introduction page, when I click the exit button, then I am redirected to sign out page and my session is cleared", async () => {
    await browser.openQuestionnaire("test_introduction.json");
    await $(IntroductionPage.exitButton()).click();

    await expect(await browser.getUrl()).to.contain("/surveys/todo");

    await browser.back();
    await expect(await $("body").getHTML()).to.contain("Sorry, you need to sign in again");
  });

  it("Given I am completing a questionnaire, when I select save and sign out, then I am redirected to the signed out page", async () => {
    await browser.openQuestionnaire("test_numbers.json", { userId: "test_user", responseId });
    await $(SetMinMax.setMinimum()).setValue("10");
    await $(SetMinMax.setMaximum()).setValue("1020");
    await click(SetMinMax.submit());
    await $(TestMinMax.saveSignOut()).click();

    await expect(await browser.getUrl()).to.contain("/signed-out");

    await browser.back();
    await expect(await $("body").getHTML()).to.contain("Sorry, you need to sign in again");
  });

  it("Given I have started a questionnaire, when I return to the questionnaire, then I am returned to the page I was on and can then complete the questionnaire", async () => {
    await browser.openQuestionnaire("test_numbers.json", { userId: "test_user", responseId });

    await $(TestMinMax.testRange()).setValue("10");
    await $(TestMinMax.testMin()).setValue("123");
    await $(TestMinMax.testMax()).setValue("1000");
    await $(TestMinMax.testPercent()).setValue("100");
    await click(TestMinMax.submit());
    await $(DetailAnswer.answer1()).click();
    await click(DetailAnswer.submit());
    await $(currencyBlock.usDollars()).click();
    await click(currencyBlock.submit());
    await $(firstNumberBlock.firstNumber()).setValue(50);
    await click(firstNumberBlock.submit());
    await $(secondNumberBlock.secondNumber()).setValue(321);
    await click(secondNumberBlock.submit());
    await click(currencySectionSummary.submit());

    await click(SubmitPage.submit());
    await expect(await browser.getUrl()).to.contain("thank-you");
  });

  it("Given a I have started a social questionnaire, when I select save and sign out, then I am redirected to the signed out page and the correct access code link is shown", async () => {
    await browser.openQuestionnaire("test_theme_social.json", { version: "v2", theme: "social" });
    await $(SubmitPage.saveSignOut()).click();
    await expect(await browser.getUrl()).to.contain("/signed-out");
    await expect(await $("body").getHTML()).to.contain("Your progress has been saved");
    await expect(await $("body").getHTML()).to.contain("To resume the survey,");
    await expect(await $("body").getHTML()).to.contain("/en/start");
  });

  it("Given a I have started a business questionnaire, when I select save and sign out, then I am redirected to the signed out page and the correct access code link is shown", async () => {
    await browser.openQuestionnaire("test_introduction.json");
    await $(IntroductionPage.getStarted()).click();
    await $(IntroInterstitialPage.saveSignOut()).click();
    await expect(await browser.getUrl()).to.contain("/signed-out");
    await expect(await $("body").getHTML()).to.contain("Your progress has been saved");
    await expect(await $("body").getHTML()).to.contain("To find further information or resume the survey,");
    await expect(await $("body").getHTML()).to.contain("/surveys/todo");
  });

  it("Given a business questionnaire, when I navigate the questionnaire, then I see the correct sign out buttons", async () => {
    await browser.openQuestionnaire("test_introduction.json");

    await expect(await $(IntroductionPage.exitButton()).getText()).to.contain("Exit");
    await $(IntroductionPage.getStarted()).click();

    await expect(await $(IntroInterstitialPage.saveSignOut()).getText()).to.contain("Save and exit survey");
    await click(IntroInterstitialPage.submit());

    await expect(await $(SubmitPage.saveSignOut()).getText()).to.contain("Save and exit survey");
    await click(SubmitPage.submit());

    await expect(await $(IntroThankYouPagePage.exitButton()).isExisting()).to.be.false;
  });

  it("Given a Census questionnaire, when I navigate the questionnaire, then I see the correct sign out buttons", async () => {
    await browser.openQuestionnaire("test_thank_you_census_household.json");

    await expect(await $(HouseHolderConfirmationPage.saveSignOut()).getText()).to.contain("Save and complete later");
    await click(HouseHolderConfirmationPage.submit());

    await expect(await $(SubmitPage.saveSignOut()).getText()).to.contain("Save and complete later");
  });
});
