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
import { click } from "../../../helpers";

describe("View Submitted Response", () => {
  beforeEach("Load the questionnaire", async () => {
    await browser.openQuestionnaire("test_view_submitted_response.json");
    await $(NameBlockPage.answer()).setValue("John Smith");
    await click(NameBlockPage.submit());
    await $(AddressBlockPage.answer()).setValue("NP10 8XG");
    await click(AddressBlockPage.submit());
    await click(SubmitPage.submit());
    await expect(await browser.getUrl()).toContain(ThankYouPage.pageName);
    await expect(await $(ThankYouPage.title()).getHTML()).toContain("Thank you for completing the Test");
    await $(ThankYouPage.savePrintAnswersLink()).click();
    await expect(await browser.getUrl()).toContain(ViewSubmittedResponsePage.pageName);
  });

  it("Given I have completed a questionnaire with view submitted response enabled, When I am on the view submitted response page within 45 minutes of submission, Then the summary is displayed correctly", async () => {
    await expect(await $(ViewSubmittedResponsePage.informationPanel()).isDisplayed()).toBe(false);
    await expect(await $(ViewSubmittedResponsePage.printButton()).isDisplayed()).toBe(true);
    await expect(await $(ViewSubmittedResponsePage.heading()).getText()).toBe("Answers submitted for Apple");
    await expect(await $(ViewSubmittedResponsePage.metadataTerm(1)).getText()).toBe("Submitted on:");
    await expect(await $(ViewSubmittedResponsePage.metadataTerm(2)).getText()).toBe("Submission reference:");
    await expect(await $(ViewSubmittedResponsePage.personalDetailsGroupTitle()).getText()).toBe("Personal Details");
    await expect(await $(ViewSubmittedResponsePage.nameQuestion()).getText()).toBe("What is your name?");
    await expect(await $(ViewSubmittedResponsePage.nameAnswer()).getText()).toBe("John Smith");
    await expect(await $(ViewSubmittedResponsePage.addressDetailsGroupTitle()).getText()).toBe("Address Details");
    await expect(await $(ViewSubmittedResponsePage.addressQuestion()).getText()).toBe("What is your address?");
    await expect(await $(ViewSubmittedResponsePage.addressAnswer()).getText()).toBe("NP10 8XG");
  });

  describe("Given I am on the view submitted response page and I submitted over 45 minutes ago", () => {
    it("When I click the Download as PDF button, Then I should be redirected to a page informing me that I can no longer view or get a copy of my answers", async () => {
      await browser.pause(40000); // Waiting 40 seconds for the timeout to expire (45 minute timeout changed to 35 seconds by overriding VIEW_SUBMITTED_RESPONSE_EXPIRATION_IN_SECONDS for the purpose of the functional test)
      await $(ViewSubmittedResponsePage.downloadButton()).click();
      await expect(await $(ViewSubmittedResponsePage.informationPanel()).isDisplayed()).toBe(true);
      await expect(await $(ViewSubmittedResponsePage.informationPanel()).getHTML()).toContain(
        "For security, you can no longer view or get a copy of your answers",
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
    await click(HubPage.submit());

    await $(NameBlockPage.answer()).setValue("John Smith");
    await click(NameBlockPage.submit());
    await $(AddressBlockPage.answer()).setValue("NP10 8XG");
    await click(AddressBlockPage.submit());

    await click(HubPage.submit());
    await $(PrimaryPersonListCollectorPage.yes()).click();
    await click(PrimaryPersonListCollectorPage.submit());
    await $(PrimaryPersonListCollectorAddPage.firstName()).setValue("Marcus");
    await $(PrimaryPersonListCollectorAddPage.lastName()).setValue("Twin");
    await click(PrimaryPersonListCollectorAddPage.submit());
    await $(ListCollectorPage.yes()).click();
    await click(ListCollectorPage.submit());
    await $(ListCollectorAddPage.firstName()).setValue("John");
    await $(ListCollectorAddPage.lastName()).setValue("Doe");
    await click(ListCollectorAddPage.submit());
    await $(ListCollectorPage.no()).click();
    await click(ListCollectorPage.submit());
    await click(HubPage.submit());

    await $(SkipFirstNumberBlockPageSectionOne.no()).click();
    await click(SkipFirstNumberBlockPageSectionOne.submit());
    await $(FirstNumberBlockPageSectionOne.firstNumber()).setValue(10);
    await click(FirstNumberBlockPageSectionOne.submit());
    await $(FirstAndAHalfNumberBlockPageSectionOne.firstAndAHalfNumberAlsoInTotal()).setValue(20);
    await click(FirstAndAHalfNumberBlockPageSectionOne.submit());
    await $(SecondNumberBlockPageSectionOne.secondNumberAlsoInTotal()).setValue(30);
    await click(SecondNumberBlockPageSectionOne.submit());
    await click(CalculatedSummarySectionOne.submit());
    await click(SectionSummarySectionOne.submit());
    await click(HubPage.submit());
    await $(ThirdNumberBlockPageSectionTwo.thirdNumber()).setValue(20);
    await $(ThirdNumberBlockPageSectionTwo.thirdNumberAlsoInTotal()).setValue(20);
    await click(ThirdNumberBlockPageSectionTwo.submit());
    await click(CalculatedSummarySectionTwo.submit());
    await $(DependencyQuestionSectionTwo.checkboxAnswerCalcValue2()).click();
    await click(DependencyQuestionSectionTwo.submit());
    await $(SkippableBlockSectionTwo.skippable()).setValue(100);
    await click(SkippableBlockSectionTwo.submit());
    await click(SectionSummarySectionTwo.submit());
    await click(HubPage.submit());
    await $(ThirdNumberBlockPageSectionTwo.thirdNumber()).setValue(40);
    await $(ThirdNumberBlockPageSectionTwo.thirdNumberAlsoInTotal()).setValue(40);
    await click(ThirdNumberBlockPageSectionTwo.submit());
    await click(CalculatedSummarySectionTwo.submit());
    await $(DependencyQuestionSectionTwo.checkboxAnswerCalcValue2()).click();
    await click(DependencyQuestionSectionTwo.submit());
    await click(SectionSummarySectionTwo.submit());

    await click(HubPage.submit());
    await expect(await browser.getUrl()).toContain(ThankYouPage.pageName);
    await expect(await $(ThankYouPage.title()).getHTML()).toContain("Thank you for completing the Test");
    await $(ThankYouPage.savePrintAnswersLink()).click();
    await expect(await browser.getUrl()).toContain(ViewSubmittedResponsePage.pageName);
  });

  it("Given I have completed a questionnaire with a repeating section and view submitted response enabled, When I am on the view submitted response page within 45 minutes of submission, Then the summary is displayed correctly", async () => {
    await expect(await $(ViewSubmittedResponseRepeatingPage.informationPanel()).isDisplayed()).toBe(false);
    await expect(await $(ViewSubmittedResponseRepeatingPage.printButton()).isDisplayed()).toBe(true);
    await expect(await $(ViewSubmittedResponseRepeatingPage.heading()).getText()).toBe("Answers submitted for Apple");
    await expect(await $(ViewSubmittedResponseRepeatingPage.metadataTerm(1)).getText()).toBe("Submitted on:");
    await expect(await $(ViewSubmittedResponseRepeatingPage.metadataTerm(2)).getText()).toBe("Submission reference:");
    await expect(await $(ViewSubmittedResponseRepeatingPage.personalDetailsGroupTitle()).getText()).toBe("Personal Details");
    await expect(await $(ViewSubmittedResponseRepeatingPage.nameQuestion()).getText()).toBe("What is your name?");
    await expect(await $(ViewSubmittedResponseRepeatingPage.nameAnswer()).getText()).toBe("John Smith");
    await expect(await $(ViewSubmittedResponseRepeatingPage.addressDetailsGroupTitle()).getText()).toBe("Address Details");
    await expect(await $(ViewSubmittedResponseRepeatingPage.addressQuestion()).getText()).toBe("What is your address?");
    await expect(await $(ViewSubmittedResponseRepeatingPage.addressAnswer()).getText()).toBe("NP10 8XG");
    await expect(await $("body").getHTML()).toContain("Marcus Twin");
    await expect(await $(firstGroup).$$(groupTitle)[0].getText()).toBe("Calculated Summary Group");
    await expect(await $(firstGroup).$$(repeatingSectionAnswer)[0].getText()).toBe("40 - calculated summary answer (current section)");
    await expect(await $("body").getHTML()).toContain("How much did Marcus Twin spend on fruit?");
    await expect(await $(firstGroup).$$(skippableRepeatingSectionAnswer)[0].getText()).toBe("£100");
    await expect(await $("body").getHTML()).toContain("John Doe");
    await expect(await $(secondGroup).$$(groupTitle)[0].getText()).toBe("Calculated Summary Group");
    await expect(await $(secondGroup).$$(repeatingSectionAnswer)[0].getText()).toBe("80 - calculated summary answer (current section)");
    await expect(await $("body").getHTML()).not.toContain("How much did John Doe spend on fruit?");
  });
});
