import AddressBlockPage from "../../../generated_pages/view_submitted_response/address.page.js";
import NameBlockPage from "../../../generated_pages/view_submitted_response/name.page.js";
import SubmitPage from "../../../generated_pages/view_submitted_response/submit.page.js";
import ThankYouPage from "../../../base_pages/thank-you.page";
import ViewSubmittedResponsePage from "../../../generated_pages/view_submitted_response/view-submitted-response.page.js";
import ViewSubmittedResponseRepeatingPage from "../../../generated_pages/view_submitted_response_repeating_sections/view-submitted-response.page.js";
import HubPage from "../../../base_pages/hub.page";
import PrimaryPersonListCollectorPage from "../../../generated_pages/view_submitted_response_repeating_sections/primary-person-list-collector.page";
import PrimaryPersonListCollectorAddPage from "../../../generated_pages/view_submitted_response_repeating_sections/primary-person-list-collector-add.page";
import ListCollectorPage from "../../../generated_pages/view_submitted_response_repeating_sections/list-collector.page";
import SkipFirstNumberBlockPageSectionOne from "../../../generated_pages/view_submitted_response_repeating_sections/skip-first-block.page";
import FirstNumberBlockPageSectionOne from "../../../generated_pages/view_submitted_response_repeating_sections/first-number-block.page";
import FirstAndAHalfNumberBlockPageSectionOne from "../../../generated_pages/view_submitted_response_repeating_sections/first-and-a-half-number-block.page";
import SecondNumberBlockPageSectionOne from "../../../generated_pages/view_submitted_response_repeating_sections/second-number-block.page";
import CalculatedSummarySectionOne from "../../../generated_pages/view_submitted_response_repeating_sections/currency-total-playback-1.page";
import SectionSummarySectionOne from "../../../generated_pages/view_submitted_response_repeating_sections/questions-section-summary.page";
import ThirdNumberBlockPageSectionTwo from "../../../generated_pages/view_submitted_response_repeating_sections/third-number-block.page";
import CalculatedSummarySectionTwo from "../../../generated_pages/view_submitted_response_repeating_sections/currency-total-playback-2.page";
import DependencyQuestionSectionTwo from "../../../generated_pages/view_submitted_response_repeating_sections/mutually-exclusive-checkbox.page";
import SkippableBlockSectionTwo from "../../../generated_pages/view_submitted_response_repeating_sections/skippable-block.page";
import SectionSummarySectionTwo from "../../../generated_pages/new_calculated_summary_cross_section_dependencies_repeating/calculated-summary-section-summary.page";
import ListCollectorAddPage from "../../../generated_pages/view_submitted_response_repeating_sections//list-collector-add.page";

describe("View Submitted Response", () => {
  beforeEach("Load the questionnaire", async () => {
    await browser.openQuestionnaire("test_view_submitted_response.json");
    await $(NameBlockPage.answer()).setValue("John Smith");
    await $(NameBlockPage.submit()).click();
    await $(AddressBlockPage.answer()).setValue("NP10 8XG");
    await $(AddressBlockPage.submit()).click();
    await $(SubmitPage.submit()).click();
    await expect(await browser.getUrl()).to.contain(ThankYouPage.pageName);
    await expect(await $(ThankYouPage.title()).getHTML()).to.contain("Thank you for completing the Test");
    await $(ThankYouPage.savePrintAnswersLink()).click();
    await expect(await browser.getUrl()).to.contain(ViewSubmittedResponsePage.pageName);
  });

  it("Given I have completed a questionnaire with view submitted response enabled, When I am on the view submitted response page within 45 minutes of submission, Then the summary is displayed correctly", async () => {
    await expect(await $(ViewSubmittedResponsePage.informationPanel()).isDisplayed()).to.be.false;
    await expect(await $(ViewSubmittedResponsePage.printButton()).isDisplayed()).to.be.true;
    await expect(await $(ViewSubmittedResponsePage.heading()).getText()).to.equal("Answers submitted for Apple");
    await expect(await $(ViewSubmittedResponsePage.metadataTerm(1)).getText()).to.equal("Submitted on:");
    await expect(await $(ViewSubmittedResponsePage.metadataTerm(2)).getText()).to.equal("Submission reference:");
    await expect(await $(ViewSubmittedResponsePage.personalDetailsGroupTitle()).getText()).to.equal("Personal Details");
    await expect(await $(ViewSubmittedResponsePage.nameQuestion()).getText()).to.equal("What is your name?");
    await expect(await $(ViewSubmittedResponsePage.nameAnswer()).getText()).to.equal("John Smith");
    await expect(await $(ViewSubmittedResponsePage.addressDetailsGroupTitle()).getText()).to.equal("Address Details");
    await expect(await $(ViewSubmittedResponsePage.addressQuestion()).getText()).to.equal("What is your address?");
    await expect(await $(ViewSubmittedResponsePage.addressAnswer()).getText()).to.equal("NP10 8XG");
  });

  describe("Given I am on the view submitted response page and I submitted over 45 minutes ago", () => {
    it("When I click the Download as PDF button, Then I should be redirected to a page informing me that I can no longer view or get a copy of my answers", async () => {
      await browser.pause(40000); // Waiting 40 seconds for the timeout to expire (45 minute timeout changed to 35 seconds by overriding VIEW_SUBMITTED_RESPONSE_EXPIRATION_IN_SECONDS for the purpose of the functional test)
      await $(ViewSubmittedResponsePage.downloadButton()).click();
      await expect(await $(ViewSubmittedResponsePage.informationPanel()).isDisplayed()).to.be.true;
      await expect(await $(ViewSubmittedResponsePage.informationPanel()).getHTML()).to.contain(
        "For security, you can no longer view or get a copy of your answers"
      );
    });
  });
});

const firstGroup = 'div[id="calculated-summary-0"]';
const secondGroup = 'div[id="calculated-summary-0-1"]';
const groupTitle = 'h3[class="ons-summary__group-title"]';
const repeatingSectionAnswer = '[data-qa="checkbox-answer"]';
const skippableRepeatingSectionAnswer = '[data-qa="skippable-answer"]';

describe("View Submitted Response Summary Page With Repeating Sections", () => {
  beforeEach("Load the questionnaire", async () => {
    await browser.openQuestionnaire("test_view_submitted_response_repeating_sections.json");
    await $(HubPage.submit()).click();

    await $(NameBlockPage.answer()).setValue("John Smith");
    await $(NameBlockPage.submit()).click();
    await $(AddressBlockPage.answer()).setValue("NP10 8XG");
    await $(AddressBlockPage.submit()).click();

    await $(HubPage.submit()).click();
    await $(PrimaryPersonListCollectorPage.yes()).click();
    await $(PrimaryPersonListCollectorPage.submit()).click();
    await $(PrimaryPersonListCollectorAddPage.firstName()).setValue("Marcus");
    await $(PrimaryPersonListCollectorAddPage.lastName()).setValue("Twin");
    await $(PrimaryPersonListCollectorAddPage.submit()).click();
    await $(ListCollectorPage.yes()).click();
    await $(ListCollectorPage.submit()).click();
    await $(ListCollectorAddPage.firstName()).setValue("John");
    await $(ListCollectorAddPage.lastName()).setValue("Doe");
    await $(ListCollectorAddPage.submit()).click();
    await $(ListCollectorPage.no()).click();
    await $(ListCollectorPage.submit()).click();
    await $(HubPage.submit()).click();

    await $(SkipFirstNumberBlockPageSectionOne.no()).click();
    await $(SkipFirstNumberBlockPageSectionOne.submit()).click();
    await $(FirstNumberBlockPageSectionOne.firstNumber()).setValue(10);
    await $(FirstNumberBlockPageSectionOne.submit()).click();
    await $(FirstAndAHalfNumberBlockPageSectionOne.firstAndAHalfNumberAlsoInTotal()).setValue(20);
    await $(FirstAndAHalfNumberBlockPageSectionOne.submit()).click();
    await $(SecondNumberBlockPageSectionOne.secondNumberAlsoInTotal()).setValue(30);
    await $(SecondNumberBlockPageSectionOne.submit()).click();
    await $(CalculatedSummarySectionOne.submit()).click();
    await $(SectionSummarySectionOne.submit()).click();
    await $(HubPage.submit()).click();
    await $(ThirdNumberBlockPageSectionTwo.thirdNumber()).setValue(20);
    await $(ThirdNumberBlockPageSectionTwo.thirdNumberAlsoInTotal()).setValue(20);
    await $(ThirdNumberBlockPageSectionTwo.submit()).click();
    await $(CalculatedSummarySectionTwo.submit()).click();
    await $(DependencyQuestionSectionTwo.checkboxAnswerCalcValue2()).click();
    await $(DependencyQuestionSectionTwo.submit()).click();
    await $(SkippableBlockSectionTwo.skippable()).setValue(100);
    await $(SkippableBlockSectionTwo.submit()).click();
    await $(SectionSummarySectionTwo.submit()).click();
    await $(HubPage.submit()).click();
    await $(ThirdNumberBlockPageSectionTwo.thirdNumber()).setValue(40);
    await $(ThirdNumberBlockPageSectionTwo.thirdNumberAlsoInTotal()).setValue(40);
    await $(ThirdNumberBlockPageSectionTwo.submit()).click();
    await $(CalculatedSummarySectionTwo.submit()).click();
    await $(DependencyQuestionSectionTwo.checkboxAnswerCalcValue2()).click();
    await $(DependencyQuestionSectionTwo.submit()).click();
    await $(SectionSummarySectionTwo.submit()).click();

    await $(HubPage.submit()).click();
    await expect(await browser.getUrl()).to.contain(ThankYouPage.pageName);
    await expect(await $(ThankYouPage.title()).getHTML()).to.contain("Thank you for completing the Test");
    await $(ThankYouPage.savePrintAnswersLink()).click();
    await expect(await browser.getUrl()).to.contain(ViewSubmittedResponsePage.pageName);
  });

  it("Given I have completed a questionnaire with a repeating section and view submitted response enabled, When I am on the view submitted response page within 45 minutes of submission, Then the summary is displayed correctly", async () => {
    await expect(await $(ViewSubmittedResponseRepeatingPage.informationPanel()).isDisplayed()).to.be.false;
    await expect(await $(ViewSubmittedResponseRepeatingPage.printButton()).isDisplayed()).to.be.true;
    await expect(await $(ViewSubmittedResponseRepeatingPage.heading()).getText()).to.equal("Answers submitted for Apple");
    await expect(await $(ViewSubmittedResponseRepeatingPage.metadataTerm(1)).getText()).to.equal("Submitted on:");
    await expect(await $(ViewSubmittedResponseRepeatingPage.metadataTerm(2)).getText()).to.equal("Submission reference:");
    await expect(await $(ViewSubmittedResponseRepeatingPage.personalDetailsGroupTitle()).getText()).to.equal("Personal Details");
    await expect(await $(ViewSubmittedResponseRepeatingPage.nameQuestion()).getText()).to.equal("What is your name?");
    await expect(await $(ViewSubmittedResponseRepeatingPage.nameAnswer()).getText()).to.equal("John Smith");
    await expect(await $(ViewSubmittedResponseRepeatingPage.addressDetailsGroupTitle()).getText()).to.equal("Address Details");
    await expect(await $(ViewSubmittedResponseRepeatingPage.addressQuestion()).getText()).to.equal("What is your address?");
    await expect(await $(ViewSubmittedResponseRepeatingPage.addressAnswer()).getText()).to.equal("NP10 8XG");
    await expect(await $("body").getHTML()).to.contain("Marcus Twin");
    await expect(await $(firstGroup).$$(groupTitle)[0].getText()).to.equal("Calculated Summary Group");
    await expect(await $(firstGroup).$$(repeatingSectionAnswer)[0].getText()).to.equal("40 - calculated summary answer (current section)");
    await expect(await $("body").getHTML()).to.contain("How much did Marcus Twin spend on fruit?");
    await expect(await $(firstGroup).$$(skippableRepeatingSectionAnswer)[0].getText()).to.equal("£100.00");
    await expect(await $("body").getHTML()).to.contain("John Doe");
    await expect(await $(secondGroup).$$(groupTitle)[0].getText()).to.equal("Calculated Summary Group");
    await expect(await $(secondGroup).$$(repeatingSectionAnswer)[0].getText()).to.equal("80 - calculated summary answer (current section)");
    await expect(await $("body").getHTML()).to.not.contain("How much did John Doe spend on fruit?");
  });
});
