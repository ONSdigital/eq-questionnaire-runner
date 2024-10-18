import AgePage from "../../../generated_pages/routing_and_skipping_section_dependencies/age.page";
import HouseHoldPersonalDetailsSectionSummaryPage from "../../../generated_pages/routing_and_skipping_section_dependencies/household-personal-details-section-summary.page";
import HouseholdSectionSummaryPage from "../../../generated_pages/routing_and_skipping_section_dependencies/household-section-summary.page";
import ListCollectorAddPage from "../../../generated_pages/routing_and_skipping_section_dependencies/list-collector-add.page";
import ListCollectorPage from "../../../generated_pages/routing_and_skipping_section_dependencies/list-collector.page";
import NamePage from "../../../generated_pages/routing_and_skipping_section_dependencies/name-block.page";
import PrimaryPersonSummaryPage from "../../../generated_pages/routing_and_skipping_section_dependencies/primary-person-summary.page";
import ReasonNoConfirmationPage from "../../../generated_pages/routing_and_skipping_section_dependencies/reason-no-confirmation.page";
import RepeatingAgePage from "../../../generated_pages/routing_and_skipping_section_dependencies/repeating-age.page";
import RepeatingSexPage from "../../../generated_pages/routing_and_skipping_section_dependencies/repeating-sex.page";
import SecurityPage from "../../../generated_pages/routing_and_skipping_section_dependencies/security.page";
import SkipAgePage from "../../../generated_pages/routing_and_skipping_section_dependencies/skip-age.page";
import SkipEnableSectionPage from "../../../generated_pages/routing_and_skipping_section_dependencies/skip-household-section.page";
import EnableSectionPage from "../../../generated_pages/routing_and_skipping_section_dependencies/enable-section.page";
import SkipConfirmationPage from "../../../generated_pages/routing_and_skipping_section_dependencies/skip-confirmation.page";
import SkipConfirmationSectionSummaryPage from "../../../generated_pages/routing_and_skipping_section_dependencies/skip-confirmation-section-summary.page";
import SkipSectionSummaryPage from "../../../generated_pages/routing_and_skipping_section_dependencies/skip-section-summary.page";
import RepeatingIsDependentPage from "../../../generated_pages/routing_and_skipping_section_dependencies/repeating-is-dependent.page";
import RepeatingIsSmokerPage from "../../../generated_pages/routing_and_skipping_section_dependencies/repeating-is-smoker.page";

import HubPage from "../../../base_pages/hub.page";
import { click } from "../../../helpers";

describe("Routing and skipping section dependencies", () => {
  describe("Given the routing and skipping section dependencies questionnaire", () => {
    beforeEach("Load the survey", async () => {
      await browser.openQuestionnaire("test_routing_and_skipping_section_dependencies.json");
    });

    it("When I answer 'No' to skipping the age question, Then in the Primary Person section I am asked my name, age and why I didn't confirm skipping", async () => {
      await answerNoToSkipAgeQuestion();

      await selectPrimaryPerson();
      await answerAndSubmitNameQuestion();
      await answerAndSubmitAgeQuestion();
      await answerAndSubmitReasonForNoConfirmationQuestion();

      await expectPersonalDetailsName();
      await expectPersonalDetailsAge();
      await expectReasonNoConfirmationAnswer();
    });

    it("When I answer 'Yes' to skipping the age question, Then in the Primary Person section I am only asked my name and why I didn't confirm skipping", async () => {
      await answerYesToSkipAgeQuestion();

      await selectPrimaryPerson();
      await answerAndSubmitNameQuestion();
      await answerAndSubmitReasonForNoConfirmationQuestion();

      await expectPersonalDetailsName();
      await expectReasonNoConfirmationAnswer();
      await expectPersonalDetailsAgeExistingFalse();
    });

    it("When I answer 'Yes' to skipping the age question and 'Yes' to are you sure in skip question confirmation section, Then in the Primary Person section I am just asked my name", async () => {
      await answerYesToSkipAgeQuestion();

      await selectConfirmationSectionAndAnswerSecurityQuestion();
      await answerYesToSkipConfirmationQuestion();

      await selectPrimaryPerson();
      await answerAndSubmitNameQuestion();

      await expectPersonalDetailsName();
      await expectPersonalDetailsAgeExistingFalse();
      await expectReasonNoConfirmationExistingFalse();
    });

    it("When I answer 'Yes' to skipping the age question but 'No' to are you sure in skip question confirmation section, Then in the Primary Person section I am only asked my name and age", async () => {
      await answerYesToSkipAgeQuestion();

      await selectConfirmationSectionAndAnswerSecurityQuestion();
      await answerNoToSkipConfirmationQuestion();

      await selectPrimaryPerson();
      await answerAndSubmitNameQuestion();
      await answerAndSubmitAgeQuestion();

      await expectPersonalDetailsName();
      await expectPersonalDetailsAge();
      await expectReasonNoConfirmationExistingFalse();
    });

    it("When I answer 'No' to skipping the age question and populate the household, Then in each repeating section I am not asked their age", async () => {
      await answerNoToSkipAgeQuestion();

      await addHouseholdMembers();

      await $(HubPage.summaryRowLink("household-personal-details-section-1")).click();
      await $(RepeatingSexPage.female()).click();
      await click(RepeatingSexPage.submit());
      await $(RepeatingAgePage.answer()).setValue("45");
      await click(RepeatingAgePage.submit());
      await $(RepeatingIsDependentPage.no()).click();
      await click(RepeatingIsDependentPage.submit());
      await $(RepeatingIsSmokerPage.no()).click();
      await click(RepeatingIsSmokerPage.submit());

      await expect(await $(HouseHoldPersonalDetailsSectionSummaryPage.repeatingSexAnswer()).getText()).toBe("Female");
      await expect(await $(HouseHoldPersonalDetailsSectionSummaryPage.repeatingAgeAnswer()).getText()).toBe("45");

      await click(HouseHoldPersonalDetailsSectionSummaryPage.submit());
      await $(HubPage.summaryRowLink("household-personal-details-section-2")).click();
      await $(RepeatingSexPage.male()).click();
      await click(RepeatingSexPage.submit());
      await $(RepeatingAgePage.answer()).setValue("10");
      await click(RepeatingAgePage.submit());
      await $(RepeatingIsDependentPage.yes()).click();
      await click(RepeatingIsDependentPage.submit());

      await expect(await $(HouseHoldPersonalDetailsSectionSummaryPage.repeatingSexAnswer()).getText()).toBe("Male");
      await expect(await $(HouseHoldPersonalDetailsSectionSummaryPage.repeatingAgeAnswer()).getText()).toBe("10");
    });

    it("When I answer 'Yes' to skipping the age question and populate the household, Then in each repeating section I am not asked their age", async () => {
      await answerYesToSkipAgeQuestion();

      await addHouseholdMembers();

      await $(HubPage.summaryRowLink("household-personal-details-section-1")).click();
      await $(RepeatingSexPage.female()).click();
      await click(RepeatingSexPage.submit());
      await $(RepeatingIsDependentPage.no()).click();
      await click(RepeatingIsDependentPage.submit());
      await expect(await $(HouseHoldPersonalDetailsSectionSummaryPage.repeatingSexAnswer()).getText()).toBe("Female");
      await expect(await $(HouseHoldPersonalDetailsSectionSummaryPage.repeatingAgeAnswer()).isExisting()).toBe(false);

      await click(HouseHoldPersonalDetailsSectionSummaryPage.submit());
      await $(HubPage.summaryRowLink("household-personal-details-section-2")).click();
      await $(RepeatingSexPage.male()).click();
      await click(RepeatingSexPage.submit());
      await $(RepeatingIsDependentPage.yes()).click();
      await click(RepeatingIsDependentPage.submit());

      await expect(await $(HouseHoldPersonalDetailsSectionSummaryPage.repeatingSexAnswer()).getText()).toBe("Male");
      await expect(await $(HouseHoldPersonalDetailsSectionSummaryPage.repeatingAgeAnswer()).isExisting()).toBe(false);
    });
  });

  describe("Given the routing and skipping section dependencies questionnaire", () => {
    beforeEach("Load the survey", async () => {
      await browser.openQuestionnaire("test_routing_and_skipping_section_dependencies.json");
    });
    it("When I answer 'No' to skipping the section question and 'Yes' to enable the section question, Then the household summary will be visible on the hub", async () => {
      await answerNoToSkipEnableQuestionAndYesToEnableSection();

      await expect(await $(HubPage.summaryRowLink("household-section")).isExisting()).toBe(true);
    });
    it("When I answer 'No' to skipping the section question and 'No' to enable the section question, Then the household summary will not be visible on the hub", async () => {
      await answerNoToSkipEnableQuestionAndNoToEnableSection();

      await expect(await $(HubPage.summaryRowLink("household-section")).isExisting()).toBe(false);
    });
  });

  describe("Given the routing and skipping section dependencies questionnaire and I answered 'No' to skipping the section question and 'Yes' to enable the section question", () => {
    before("Load the survey", async () => {
      await browser.openQuestionnaire("test_routing_and_skipping_section_dependencies.json");
    });
    it("When I change my answer to skipping the section question to 'No', Then the household summary will not be visible on the hub", async () => {
      await answerNoToSkipEnableQuestionAndYesToEnableSection();
      await changeSkipEnableQuestionToYes();

      await expect(await $(HubPage.summaryRowLink("household-section")).isExisting()).toBe(false);
    });
  });

  describe("Given the routing and skipping section dependencies questionnaire and I answered 'Yes' to skipping the age question but 'No' to are you sure in skip question confirmation section", () => {
    before("Load the survey", async () => {
      await browser.openQuestionnaire("test_routing_and_skipping_section_dependencies.json");
    });

    it("When I change my answer to skipping age to 'No', removing the 'are you sure' question from the path, Then in the Primary Person section I am asked my name, age and why I didn't confirm skipping", async () => {
      await answerYesToSkipAgeQuestion();

      await selectConfirmationSectionAndAnswerSecurityQuestion();
      await answerNoToSkipConfirmationQuestion();

      await editNoToSkipAgeQuestion();

      await selectPrimaryPerson();
      await answerAndSubmitNameQuestion();
      await answerAndSubmitAgeQuestion();

      await $(ReasonNoConfirmationPage.iDidButItWasRemovedFromThePathAsIChangedMyAnswerToNoOnTheSkipQuestion()).click();
      await click(ReasonNoConfirmationPage.submit());

      await expectPersonalDetailsName();
      await expectPersonalDetailsAge();
      await expect(await $(PrimaryPersonSummaryPage.reasonNoConfirmationAnswer()).getText()).toBe(
        "I did, but it was removed from the path as I changed my answer to No on the skip question",
      );
    });
  });

  describe("Given the routing and skipping section dependencies questionnaire and I answered 'Yes' to skipping the age question and complete the Primary Person section", () => {
    before("Load the survey", async () => {
      await browser.openQuestionnaire("test_routing_and_skipping_section_dependencies.json");
    });

    it("When I change my answer to skipping age to 'No', Then the Primary Person section status is changed to Partially completed", async () => {
      await answerYesToSkipAgeQuestion();
      await selectPrimaryPerson();
      await answerAndSubmitNameQuestion();
      await answerAndSubmitReasonForNoConfirmationQuestion();
      await click(PrimaryPersonSummaryPage.submit());

      await expect(await $(HubPage.summaryRowState("primary-person")).getText()).toBe("Completed");

      await editNoToSkipAgeQuestion();

      await expect(await $(HubPage.summaryRowState("primary-person")).getText()).toBe("Partially completed");
    });

    it("When I change my answer back to skipping age to 'Yes', Then the Primary Person section status is changed back to Completed", async () => {
      await editYesToSkipAgeQuestion();

      await expect(await $(HubPage.summaryRowState("primary-person")).getText()).toBe("Completed");
    });
  });

  describe("Given the routing and skipping section dependencies questionnaire and I answered 'Yes' to skipping the age question and add 2 household members but complete only one", () => {
    before("Load the survey", async () => {
      await browser.openQuestionnaire("test_routing_and_skipping_section_dependencies.json");
    });

    it("When I change my answer to skipping age to 'No', Then the completed household member status is changed to Partially completed and the other stays as not started", async () => {
      await answerYesToSkipAgeQuestion();
      await addHouseholdMembers();
      await $(HubPage.summaryRowLink("household-personal-details-section-1")).click();
      await $(RepeatingSexPage.female()).click();
      await click(RepeatingSexPage.submit());
      await $(RepeatingIsDependentPage.no()).click();
      await click(RepeatingIsDependentPage.submit());
      await click(HouseHoldPersonalDetailsSectionSummaryPage.submit());

      await editNoToSkipAgeQuestion();

      await expect(await $(HubPage.summaryRowState("household-personal-details-section-1")).getText()).toBe("Partially completed");
      await expect(await $(HubPage.summaryRowState("household-personal-details-section-2")).getText()).toBe("Not started");
    });

    it("When I change my answer back to skipping age to 'Yes', Then the Partially completed household member status is changed back to Completed and the other stays as not started", async () => {
      await editYesToSkipAgeQuestion();

      await expect(await $(HubPage.summaryRowState("household-personal-details-section-1")).getText()).toBe("Completed");
      await expect(await $(HubPage.summaryRowState("household-personal-details-section-2")).getText()).toBe("Not started");
    });
  });

  describe("Given the routing and skipping section dependencies questionnaire", () => {
    beforeEach("Load the survey", async () => {
      await browser.openQuestionnaire("test_routing_and_skipping_section_dependencies.json");
    });

    it("When I answer 'No' to skipping the age question and populate the household with Repeating Age > 18, Then in each repeating section I am asked if they are smoker", async () => {
      await answerNoToSkipAgeQuestion();

      await addHouseholdMembers();

      await $(HubPage.summaryRowLink("household-personal-details-section-1")).click();
      await $(RepeatingSexPage.female()).click();
      await click(RepeatingSexPage.submit());
      await $(RepeatingAgePage.answer()).setValue("45");
      await click(RepeatingAgePage.submit());
      await $(RepeatingIsDependentPage.no()).click();
      await click(RepeatingIsDependentPage.submit());
      await $(RepeatingIsSmokerPage.no()).click();
      await click(RepeatingIsSmokerPage.submit());

      await expect(await $(HouseHoldPersonalDetailsSectionSummaryPage.repeatingSexAnswer()).getText()).toBe("Female");
      await expect(await $(HouseHoldPersonalDetailsSectionSummaryPage.repeatingAgeAnswer()).getText()).toBe("45");
      await expect(await $(HouseHoldPersonalDetailsSectionSummaryPage.repeatingIsSmokerAnswer()).getText()).toBe("No");

      await click(HouseHoldPersonalDetailsSectionSummaryPage.submit());
      await $(HubPage.summaryRowLink("household-personal-details-section-2")).click();
      await $(RepeatingSexPage.male()).click();
      await click(RepeatingSexPage.submit());
      await $(RepeatingAgePage.answer()).setValue("19");
      await click(RepeatingAgePage.submit());
      await $(RepeatingIsDependentPage.yes()).click();
      await click(RepeatingIsDependentPage.submit());
      await $(RepeatingIsSmokerPage.no()).click();
      await click(RepeatingIsSmokerPage.submit());

      await expect(await $(HouseHoldPersonalDetailsSectionSummaryPage.repeatingSexAnswer()).getText()).toBe("Male");
      await expect(await $(HouseHoldPersonalDetailsSectionSummaryPage.repeatingAgeAnswer()).getText()).toBe("19");
      await expect(await $(HouseHoldPersonalDetailsSectionSummaryPage.repeatingIsSmokerAnswer()).getText()).toBe("No");
    });

    it("When I answer 'No' to skipping the age question and populate the household with Repeating Age < 18, Then in each repeating section I am not asked if they are smoker", async () => {
      await answerNoToSkipAgeQuestion();

      await addHouseholdMembers();

      await $(HubPage.summaryRowLink("household-personal-details-section-1")).click();
      await $(RepeatingSexPage.female()).click();
      await click(RepeatingSexPage.submit());
      await $(RepeatingAgePage.answer()).setValue("15");
      await click(RepeatingAgePage.submit());
      await $(RepeatingIsDependentPage.yes()).click();
      await click(RepeatingIsDependentPage.submit());

      await expect(await $(HouseHoldPersonalDetailsSectionSummaryPage.repeatingSexAnswer()).getText()).toBe("Female");
      await expect(await $(HouseHoldPersonalDetailsSectionSummaryPage.repeatingAgeAnswer()).getText()).toBe("15");
      await expect(await $(HouseHoldPersonalDetailsSectionSummaryPage.repeatingIsSmokerAnswer()).isExisting()).toBe(false);

      await click(HouseHoldPersonalDetailsSectionSummaryPage.submit());
      await $(HubPage.summaryRowLink("household-personal-details-section-2")).click();
      await $(RepeatingSexPage.male()).click();
      await click(RepeatingSexPage.submit());
      await $(RepeatingAgePage.answer()).setValue("10");
      await click(RepeatingAgePage.submit());
      await $(RepeatingIsDependentPage.yes()).click();
      await click(RepeatingIsDependentPage.submit());

      await expect(await $(HouseHoldPersonalDetailsSectionSummaryPage.repeatingSexAnswer()).getText()).toBe("Male");
      await expect(await $(HouseHoldPersonalDetailsSectionSummaryPage.repeatingAgeAnswer()).getText()).toBe("10");
      await expect(await $(HouseHoldPersonalDetailsSectionSummaryPage.repeatingIsSmokerAnswer()).isExisting()).toBe(false);
    });

    it("When I answer 'Yes' to skipping the age question and populate the household, Then in each repeating section I am not asked if they are smoker", async () => {
      await answerYesToSkipAgeQuestion();

      await addHouseholdMembers();

      await $(HubPage.summaryRowLink("household-personal-details-section-1")).click();
      await $(RepeatingSexPage.female()).click();
      await click(RepeatingSexPage.submit());
      await $(RepeatingIsDependentPage.no()).click();
      await click(RepeatingIsDependentPage.submit());
      await expect(await $(HouseHoldPersonalDetailsSectionSummaryPage.repeatingSexAnswer()).getText()).toBe("Female");
      await expect(await $(HouseHoldPersonalDetailsSectionSummaryPage.repeatingAgeAnswer()).isExisting()).toBe(false);
      await expect(await $(HouseHoldPersonalDetailsSectionSummaryPage.repeatingIsSmokerAnswer()).isExisting()).toBe(false);

      await click(HouseHoldPersonalDetailsSectionSummaryPage.submit());
      await $(HubPage.summaryRowLink("household-personal-details-section-2")).click();
      await $(RepeatingSexPage.male()).click();
      await click(RepeatingSexPage.submit());
      await $(RepeatingIsDependentPage.yes()).click();
      await click(RepeatingIsDependentPage.submit());

      await expect(await $(HouseHoldPersonalDetailsSectionSummaryPage.repeatingSexAnswer()).getText()).toBe("Male");
      await expect(await $(HouseHoldPersonalDetailsSectionSummaryPage.repeatingAgeAnswer()).isExisting()).toBe(false);
      await expect(await $(HouseHoldPersonalDetailsSectionSummaryPage.repeatingIsSmokerAnswer()).isExisting()).toBe(false);
    });
  });
});

const addHouseholdMembers = async () => {
  await $(HubPage.summaryRowLink("household-section")).click();
  await $(ListCollectorPage.yes()).click();
  await click(ListCollectorPage.submit());
  await $(ListCollectorAddPage.firstName()).setValue("Sarah");
  await $(ListCollectorAddPage.lastName()).setValue("Smith");
  await click(ListCollectorAddPage.submit());
  await $(ListCollectorPage.yes()).click();
  await click(ListCollectorPage.submit());
  await $(ListCollectorAddPage.firstName()).setValue("Marcus");
  await $(ListCollectorAddPage.lastName()).setValue("Smith");
  await click(ListCollectorAddPage.submit());
  await $(ListCollectorPage.no()).click();
  await click(ListCollectorPage.submit());
  await click(HouseholdSectionSummaryPage.submit());
};

const selectPrimaryPerson = async () => {
  await $(HubPage.summaryRowLink("primary-person")).click();
};

const selectConfirmationSectionAndAnswerSecurityQuestion = async () => {
  await $(HubPage.summaryRowLink("skip-confirmation-section")).click();
  await $(SecurityPage.yes()).click();
  await click(SecurityPage.submit());
};

const answerYesToSkipAgeQuestion = async () => {
  await $(HubPage.summaryRowLink("skip-section")).click();
  await $(SkipAgePage.yes()).click();
  await click(SkipAgePage.submit());
  await $(SkipEnableSectionPage.no()).click();
  await click(SkipEnableSectionPage.submit());
  await $(EnableSectionPage.yes()).click();
  await click(EnableSectionPage.submit());
  await click(SkipSectionSummaryPage.submit());
};

const editNoToSkipAgeQuestion = async () => {
  await $(HubPage.summaryRowLink("skip-section")).click();
  await $(SkipSectionSummaryPage.skipAgeAnswerEdit()).click();
  await $(SkipAgePage.no()).click();
  await click(SkipAgePage.submit());
  await click(SkipSectionSummaryPage.submit());
};

const editYesToSkipAgeQuestion = async () => {
  await $(HubPage.summaryRowLink("skip-section")).click();
  await $(SkipSectionSummaryPage.skipAgeAnswerEdit()).click();
  await $(SkipAgePage.yes()).click();
  await click(SkipAgePage.submit());
  await click(SkipSectionSummaryPage.submit());
};

const answerNoToSkipAgeQuestion = async () => {
  await $(HubPage.summaryRowLink("skip-section")).click();
  await $(SkipAgePage.no()).click();
  await click(SkipAgePage.submit());
  await $(SkipEnableSectionPage.no()).click();
  await click(SkipEnableSectionPage.submit());
  await $(EnableSectionPage.yes()).click();
  await click(EnableSectionPage.submit());
  await click(SkipSectionSummaryPage.submit());
};

const answerNoToSkipConfirmationQuestion = async () => {
  await $(SkipConfirmationPage.no()).click();
  await click(SkipConfirmationPage.submit());
  await click(SkipConfirmationSectionSummaryPage.submit());
};

const answerYesToSkipConfirmationQuestion = async () => {
  await $(SkipConfirmationPage.yes()).click();
  await click(SkipConfirmationPage.submit());
  await click(SkipConfirmationSectionSummaryPage.submit());
};

const answerNoToSkipEnableQuestionAndYesToEnableSection = async () => {
  await $(HubPage.summaryRowLink("skip-section")).click();
  await $(SkipAgePage.no()).click();
  await click(SkipAgePage.submit());
  await $(SkipEnableSectionPage.no()).click();
  await click(SkipEnableSectionPage.submit());
  await $(EnableSectionPage.yes()).click();
  await click(EnableSectionPage.submit());
  await click(SkipSectionSummaryPage.submit());
};

const answerNoToSkipEnableQuestionAndNoToEnableSection = async () => {
  await $(HubPage.summaryRowLink("skip-section")).click();
  await $(SkipAgePage.no()).click();
  await click(SkipAgePage.submit());
  await $(SkipEnableSectionPage.no()).click();
  await click(SkipEnableSectionPage.submit());
  await $(EnableSectionPage.no()).click();
  await click(EnableSectionPage.submit());
  await click(SkipSectionSummaryPage.submit());
};

const changeSkipEnableQuestionToYes = async () => {
  await $(HubPage.summaryRowLink("skip-section")).click();
  await $(SkipSectionSummaryPage.skipHouseholdSectionAnswerEdit()).click();
  await $(SkipEnableSectionPage.yes()).click();
  await click(SkipEnableSectionPage.submit());
  await click(SkipSectionSummaryPage.submit());
};

const answerAndSubmitNameQuestion = async () => {
  await $(NamePage.name()).setValue("John Smith");
  await click(NamePage.submit());
};

const answerAndSubmitAgeQuestion = async () => {
  await $(AgePage.answer()).setValue("50");
  await click(AgePage.submit());
};

const answerAndSubmitReasonForNoConfirmationQuestion = async () => {
  await $(ReasonNoConfirmationPage.iDidNotVisitSection2SoConfirmationWasNotNeeded()).click();
  await click(ReasonNoConfirmationPage.submit());
};

const expectPersonalDetailsName = async () => {
  await expect(await $(PrimaryPersonSummaryPage.nameAnswer()).getText()).toBe("John Smith");
};

const expectPersonalDetailsAge = async () => {
  await expect(await $(PrimaryPersonSummaryPage.ageAnswer()).getText()).toBe("50");
};

const expectReasonNoConfirmationAnswer = async () => {
  await expect(await $(PrimaryPersonSummaryPage.reasonNoConfirmationAnswer()).getText()).toBe("I did not visit section 2, so confirmation was not needed");
};

const expectPersonalDetailsAgeExistingFalse = async () => {
  await expect(await $(PrimaryPersonSummaryPage.ageAnswer()).isExisting()).toBe(false);
};

const expectReasonNoConfirmationExistingFalse = async () => {
  await expect(await $(PrimaryPersonSummaryPage.reasonNoConfirmationAnswer()).isExisting()).toBe(false);
};
