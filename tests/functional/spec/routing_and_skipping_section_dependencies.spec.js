import AgePage from "../generated_pages/routing_and_skipping_section_dependencies/age.page";
import HouseHoldPersonalDetailsSectionSummaryPage from "../generated_pages/routing_and_skipping_section_dependencies/household-personal-details-section-summary.page";
import HouseholdSectionSummaryPage from "../generated_pages/routing_and_skipping_section_dependencies/household-section-summary.page";
import ListCollectorAddPage from "../generated_pages/routing_and_skipping_section_dependencies/list-collector-add.page";
import ListCollectorPage from "../generated_pages/routing_and_skipping_section_dependencies/list-collector.page";
import NamePage from "../generated_pages/routing_and_skipping_section_dependencies/name-block.page";
import PrimaryPersonSummaryPage from "../generated_pages/routing_and_skipping_section_dependencies/primary-person-summary.page";
import ReasonNoConfirmationPage from "../generated_pages/routing_and_skipping_section_dependencies/reason-no-confirmation.page";
import RepeatingAgePage from "../generated_pages/routing_and_skipping_section_dependencies/repeating-age.page";
import RepeatingSexPage from "../generated_pages/routing_and_skipping_section_dependencies/repeating-sex.page";
import SecurityPage from "../generated_pages/routing_and_skipping_section_dependencies/security.page";
import SkipAgePage from "../generated_pages/routing_and_skipping_section_dependencies/skip-age.page";
import SkipEnableSectionPage from "../generated_pages/routing_and_skipping_section_dependencies/skip-household-section.page";
import EnableSectionPage from "../generated_pages/routing_and_skipping_section_dependencies/enable-section.page";
import SkipConfirmationPage from "../generated_pages/routing_and_skipping_section_dependencies/skip-confirmation.page";
import SkipConfirmationSectionSummaryPage from "../generated_pages/routing_and_skipping_section_dependencies/skip-confirmation-section-summary.page";
import SkipSectionSummaryPage from "../generated_pages/routing_and_skipping_section_dependencies/skip-section-summary.page";
import RepeatingIsDependentPage from "../generated_pages/routing_and_skipping_section_dependencies/repeating-is-dependent.page";
import RepeatingIsSmokerPage from "../generated_pages/routing_and_skipping_section_dependencies/repeating-is-smoker.page";

import HubPage from "../base_pages/hub.page";

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
      await $(RepeatingSexPage.submit()).click();
      await $(RepeatingAgePage.answer()).setValue("45");
      await $(RepeatingAgePage.submit()).click();
      await $(RepeatingIsDependentPage.no()).click();
      await $(RepeatingIsDependentPage.submit()).click();
      await $(RepeatingIsSmokerPage.no()).click();
      await $(RepeatingIsSmokerPage.submit()).click();

      await expect(await $(HouseHoldPersonalDetailsSectionSummaryPage.repeatingSexAnswer()).getText()).to.contain("Female");
      await expect(await $(HouseHoldPersonalDetailsSectionSummaryPage.repeatingAgeAnswer()).getText()).to.contain("45");

      await $(HouseHoldPersonalDetailsSectionSummaryPage.submit()).click();
      await $(HubPage.summaryRowLink("household-personal-details-section-2")).click();
      await $(RepeatingSexPage.male()).click();
      await $(RepeatingSexPage.submit()).click();
      await $(RepeatingAgePage.answer()).setValue("10");
      await $(RepeatingAgePage.submit()).click();
      await $(RepeatingIsDependentPage.yes()).click();
      await $(RepeatingIsDependentPage.submit()).click();

      await expect(await $(HouseHoldPersonalDetailsSectionSummaryPage.repeatingSexAnswer()).getText()).to.contain("Male");
      await expect(await $(HouseHoldPersonalDetailsSectionSummaryPage.repeatingAgeAnswer()).getText()).to.contain("10");
    });

    it("When I answer 'Yes' to skipping the age question and populate the household, Then in each repeating section I am not asked their age", async () => {
      await answerYesToSkipAgeQuestion();

      await addHouseholdMembers();

      await $(HubPage.summaryRowLink("household-personal-details-section-1")).click();
      await $(RepeatingSexPage.female()).click();
      await $(RepeatingSexPage.submit()).click();
      await $(RepeatingIsDependentPage.no()).click();
      await $(RepeatingIsDependentPage.submit()).click();
      await expect(await $(HouseHoldPersonalDetailsSectionSummaryPage.repeatingSexAnswer()).getText()).to.contain("Female");
      await expect(await $(HouseHoldPersonalDetailsSectionSummaryPage.repeatingAgeAnswer()).isExisting()).to.be.false;

      await $(HouseHoldPersonalDetailsSectionSummaryPage.submit()).click();
      await $(HubPage.summaryRowLink("household-personal-details-section-2")).click();
      await $(RepeatingSexPage.male()).click();
      await $(RepeatingSexPage.submit()).click();
      await $(RepeatingIsDependentPage.yes()).click();
      await $(RepeatingIsDependentPage.submit()).click();

      await expect(await $(HouseHoldPersonalDetailsSectionSummaryPage.repeatingSexAnswer()).getText()).to.contain("Male");
      await expect(await $(HouseHoldPersonalDetailsSectionSummaryPage.repeatingAgeAnswer()).isExisting()).to.be.false;
    });
  });

  describe("Given the routing and skipping section dependencies questionnaire", () => {
    beforeEach("Load the survey", async () => {
      await browser.openQuestionnaire("test_routing_and_skipping_section_dependencies.json");
    });
    it("When I answer 'No' to skipping the section question and 'Yes' to enable the section question, Then the household summary will be visible on the hub", async () => {
      await answerNoToSkipEnableQuestionAndYesToEnableSection();

      await expect(await $(HubPage.summaryRowLink("household-section")).isExisting()).to.be.true;
    });
    it("When I answer 'No' to skipping the section question and 'No' to enable the section question, Then the household summary will not be visible on the hub", async () => {
      await answerNoToSkipEnableQuestionAndNoToEnableSection();

      await expect(await $(HubPage.summaryRowLink("household-section")).isExisting()).to.be.false;
    });
  });

  describe("Given the routing and skipping section dependencies questionnaire and I answered 'No' to skipping the section question and 'Yes' to enable the section question", () => {
    before("Load the survey", async () => {
      await browser.openQuestionnaire("test_routing_and_skipping_section_dependencies.json");
    });
    it("When I change my answer to skipping the section question to 'No', Then the household summary will not be visible on the hub", async () => {
      await answerNoToSkipEnableQuestionAndYesToEnableSection();
      await changeSkipEnableQuestionToYes();

      await expect(await $(HubPage.summaryRowLink("household-section")).isExisting()).to.be.false;
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
      await $(ReasonNoConfirmationPage.submit()).click();

      await expectPersonalDetailsName();
      await expectPersonalDetailsAge();
      await expect(await $(PrimaryPersonSummaryPage.reasonNoConfirmationAnswer()).getText()).to.contain(
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
      await $(PrimaryPersonSummaryPage.submit()).click();

      await expect(await $(HubPage.summaryRowState("primary-person")).getText()).to.equal("Completed");

      await editNoToSkipAgeQuestion();

      await expect(await $(HubPage.summaryRowState("primary-person")).getText()).to.equal("Partially completed");
    });

    it("When I change my answer back to skipping age to 'Yes', Then the Primary Person section status is changed back to Completed", async () => {
      await editYesToSkipAgeQuestion();

      await expect(await $(HubPage.summaryRowState("primary-person")).getText()).to.equal("Completed");
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
      await $(RepeatingSexPage.submit()).click();
      await $(RepeatingIsDependentPage.no()).click();
      await $(RepeatingIsDependentPage.submit()).click();
      await $(HouseHoldPersonalDetailsSectionSummaryPage.submit()).click();

      await editNoToSkipAgeQuestion();

      await expect(await $(HubPage.summaryRowState("household-personal-details-section-1")).getText()).to.equal("Partially completed");
      await expect(await $(HubPage.summaryRowState("household-personal-details-section-2")).getText()).to.equal("Not started");
    });

    it("When I change my answer back to skipping age to 'Yes', Then the Partially completed household member status is changed back to Completed and the other stays as not started", async () => {
      await editYesToSkipAgeQuestion();

      await expect(await $(HubPage.summaryRowState("household-personal-details-section-1")).getText()).to.equal("Completed");
      await expect(await $(HubPage.summaryRowState("household-personal-details-section-2")).getText()).to.equal("Not started");
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
      await $(RepeatingSexPage.submit()).click();
      await $(RepeatingAgePage.answer()).setValue("45");
      await $(RepeatingAgePage.submit()).click();
      await $(RepeatingIsDependentPage.no()).click();
      await $(RepeatingIsDependentPage.submit()).click();
      await $(RepeatingIsSmokerPage.no()).click();
      await $(RepeatingIsSmokerPage.submit()).click();

      await expect(await $(HouseHoldPersonalDetailsSectionSummaryPage.repeatingSexAnswer()).getText()).to.contain("Female");
      await expect(await $(HouseHoldPersonalDetailsSectionSummaryPage.repeatingAgeAnswer()).getText()).to.contain("45");
      await expect(await $(HouseHoldPersonalDetailsSectionSummaryPage.repeatingIsSmokerAnswer()).getText()).to.contain("No");

      await $(HouseHoldPersonalDetailsSectionSummaryPage.submit()).click();
      await $(HubPage.summaryRowLink("household-personal-details-section-2")).click();
      await $(RepeatingSexPage.male()).click();
      await $(RepeatingSexPage.submit()).click();
      await $(RepeatingAgePage.answer()).setValue("19");
      await $(RepeatingAgePage.submit()).click();
      await $(RepeatingIsDependentPage.yes()).click();
      await $(RepeatingIsDependentPage.submit()).click();
      await $(RepeatingIsSmokerPage.no()).click();
      await $(RepeatingIsSmokerPage.submit()).click();

      await expect(await $(HouseHoldPersonalDetailsSectionSummaryPage.repeatingSexAnswer()).getText()).to.contain("Male");
      await expect(await $(HouseHoldPersonalDetailsSectionSummaryPage.repeatingAgeAnswer()).getText()).to.contain("19");
      await expect(await $(HouseHoldPersonalDetailsSectionSummaryPage.repeatingIsSmokerAnswer()).getText()).to.contain("No");
    });

    it("When I answer 'No' to skipping the age question and populate the household with Repeating Age < 18, Then in each repeating section I am not asked if they are smoker", async () => {
      await answerNoToSkipAgeQuestion();

      await addHouseholdMembers();

      await $(HubPage.summaryRowLink("household-personal-details-section-1")).click();
      await $(RepeatingSexPage.female()).click();
      await $(RepeatingSexPage.submit()).click();
      await $(RepeatingAgePage.answer()).setValue("15");
      await $(RepeatingAgePage.submit()).click();
      await $(RepeatingIsDependentPage.yes()).click();
      await $(RepeatingIsDependentPage.submit()).click();

      await expect(await $(HouseHoldPersonalDetailsSectionSummaryPage.repeatingSexAnswer()).getText()).to.contain("Female");
      await expect(await $(HouseHoldPersonalDetailsSectionSummaryPage.repeatingAgeAnswer()).getText()).to.contain("15");
      await expect(await $(HouseHoldPersonalDetailsSectionSummaryPage.repeatingIsSmokerAnswer()).isExisting()).to.be.false;

      await $(HouseHoldPersonalDetailsSectionSummaryPage.submit()).click();
      await $(HubPage.summaryRowLink("household-personal-details-section-2")).click();
      await $(RepeatingSexPage.male()).click();
      await $(RepeatingSexPage.submit()).click();
      await $(RepeatingAgePage.answer()).setValue("10");
      await $(RepeatingAgePage.submit()).click();
      await $(RepeatingIsDependentPage.yes()).click();
      await $(RepeatingIsDependentPage.submit()).click();

      await expect(await $(HouseHoldPersonalDetailsSectionSummaryPage.repeatingSexAnswer()).getText()).to.contain("Male");
      await expect(await $(HouseHoldPersonalDetailsSectionSummaryPage.repeatingAgeAnswer()).getText()).to.contain("10");
      await expect(await $(HouseHoldPersonalDetailsSectionSummaryPage.repeatingIsSmokerAnswer()).isExisting()).to.be.false;
    });

    it("When I answer 'Yes' to skipping the age question and populate the household, Then in each repeating section I am not asked if they are smoker", async () => {
      await answerYesToSkipAgeQuestion();

      await addHouseholdMembers();

      await $(HubPage.summaryRowLink("household-personal-details-section-1")).click();
      await $(RepeatingSexPage.female()).click();
      await $(RepeatingSexPage.submit()).click();
      await $(RepeatingIsDependentPage.no()).click();
      await $(RepeatingIsDependentPage.submit()).click();
      await expect(await $(HouseHoldPersonalDetailsSectionSummaryPage.repeatingSexAnswer()).getText()).to.contain("Female");
      await expect(await $(HouseHoldPersonalDetailsSectionSummaryPage.repeatingAgeAnswer()).isExisting()).to.be.false;
      await expect(await $(HouseHoldPersonalDetailsSectionSummaryPage.repeatingIsSmokerAnswer()).isExisting()).to.be.false;

      await $(HouseHoldPersonalDetailsSectionSummaryPage.submit()).click();
      await $(HubPage.summaryRowLink("household-personal-details-section-2")).click();
      await $(RepeatingSexPage.male()).click();
      await $(RepeatingSexPage.submit()).click();
      await $(RepeatingIsDependentPage.yes()).click();
      await $(RepeatingIsDependentPage.submit()).click();

      await expect(await $(HouseHoldPersonalDetailsSectionSummaryPage.repeatingSexAnswer()).getText()).to.contain("Male");
      await expect(await $(HouseHoldPersonalDetailsSectionSummaryPage.repeatingAgeAnswer()).isExisting()).to.be.false;
      await expect(await $(HouseHoldPersonalDetailsSectionSummaryPage.repeatingIsSmokerAnswer()).isExisting()).to.be.false;
    });
  });
});

const addHouseholdMembers = async () => {
  await $(HubPage.summaryRowLink("household-section")).click();
  await $(ListCollectorPage.yes()).click();
  await $(ListCollectorPage.submit()).click();
  await $(ListCollectorAddPage.firstName()).setValue("Sarah");
  await $(ListCollectorAddPage.lastName()).setValue("Smith");
  await $(ListCollectorAddPage.submit()).click();
  await $(ListCollectorPage.yes()).click();
  await $(ListCollectorPage.submit()).click();
  await $(ListCollectorAddPage.firstName()).setValue("Marcus");
  await $(ListCollectorAddPage.lastName()).setValue("Smith");
  await $(ListCollectorAddPage.submit()).click();
  await $(ListCollectorPage.no()).click();
  await $(ListCollectorPage.submit()).click();
  await $(HouseholdSectionSummaryPage.submit()).click();
};

const selectPrimaryPerson = async () => {
  await $(HubPage.summaryRowLink("primary-person")).click();
};

const selectConfirmationSectionAndAnswerSecurityQuestion = async () => {
  await $(HubPage.summaryRowLink("skip-confirmation-section")).click();
  await $(SecurityPage.yes()).click();
  await $(SecurityPage.submit()).click();
};

const answerYesToSkipAgeQuestion = async () => {
  await $(HubPage.summaryRowLink("skip-section")).click();
  await $(SkipAgePage.yes()).click();
  await $(SkipAgePage.submit()).click();
  await $(SkipEnableSectionPage.no()).click();
  await $(SkipEnableSectionPage.submit()).click();
  await $(EnableSectionPage.yes()).click();
  await $(EnableSectionPage.submit()).click();
  await $(SkipSectionSummaryPage.submit()).click();
};

const editNoToSkipAgeQuestion = async () => {
  await $(HubPage.summaryRowLink("skip-section")).click();
  await $(SkipSectionSummaryPage.skipAgeAnswerEdit()).click();
  await $(SkipAgePage.no()).click();
  await $(SkipAgePage.submit()).click();
  await $(SkipSectionSummaryPage.submit()).click();
};

const editYesToSkipAgeQuestion = async () => {
  await $(HubPage.summaryRowLink("skip-section")).click();
  await $(SkipSectionSummaryPage.skipAgeAnswerEdit()).click();
  await $(SkipAgePage.yes()).click();
  await $(SkipAgePage.submit()).click();
  await $(SkipSectionSummaryPage.submit()).click();
};

const answerNoToSkipAgeQuestion = async () => {
  await $(HubPage.summaryRowLink("skip-section")).click();
  await $(SkipAgePage.no()).click();
  await $(SkipAgePage.submit()).click();
  await $(SkipEnableSectionPage.no()).click();
  await $(SkipEnableSectionPage.submit()).click();
  await $(EnableSectionPage.yes()).click();
  await $(EnableSectionPage.submit()).click();
  await $(SkipSectionSummaryPage.submit()).click();
};

const answerNoToSkipConfirmationQuestion = async () => {
  await $(SkipConfirmationPage.no()).click();
  await $(SkipConfirmationPage.submit()).click();
  await $(SkipConfirmationSectionSummaryPage.submit()).click();
};

const answerYesToSkipConfirmationQuestion = async () => {
  await $(SkipConfirmationPage.yes()).click();
  await $(SkipConfirmationPage.submit()).click();
  await $(SkipConfirmationSectionSummaryPage.submit()).click();
};

const answerNoToSkipEnableQuestionAndYesToEnableSection = async () => {
  await $(HubPage.summaryRowLink("skip-section")).click();
  await $(SkipAgePage.no()).click();
  await $(SkipAgePage.submit()).click();
  await $(SkipEnableSectionPage.no()).click();
  await $(SkipEnableSectionPage.submit()).click();
  await $(EnableSectionPage.yes()).click();
  await $(EnableSectionPage.submit()).click();
  await $(SkipSectionSummaryPage.submit()).click();
};

const answerNoToSkipEnableQuestionAndNoToEnableSection = async () => {
  await $(HubPage.summaryRowLink("skip-section")).click();
  await $(SkipAgePage.no()).click();
  await $(SkipAgePage.submit()).click();
  await $(SkipEnableSectionPage.no()).click();
  await $(SkipEnableSectionPage.submit()).click();
  await $(EnableSectionPage.no()).click();
  await $(EnableSectionPage.submit()).click();
  await $(SkipSectionSummaryPage.submit()).click();
};

const changeSkipEnableQuestionToYes = async () => {
  await $(HubPage.summaryRowLink("skip-section")).click();
  await $(SkipSectionSummaryPage.skipHouseholdSectionAnswerEdit()).click();
  await $(SkipEnableSectionPage.yes()).click();
  await $(SkipEnableSectionPage.submit()).click();
  await $(SkipSectionSummaryPage.submit()).click();
};

const answerAndSubmitNameQuestion = async () => {
  await $(NamePage.name()).setValue("John Smith");
  await $(NamePage.submit()).click();
};

const answerAndSubmitAgeQuestion = async () => {
  await $(AgePage.answer()).setValue("50");
  await $(AgePage.submit()).click();
};

const answerAndSubmitReasonForNoConfirmationQuestion = async () => {
  await $(ReasonNoConfirmationPage.iDidNotVisitSection2SoConfirmationWasNotNeeded()).click();
  await $(ReasonNoConfirmationPage.submit()).click();
};

const expectPersonalDetailsName = async () => {
  await expect(await $(PrimaryPersonSummaryPage.nameAnswer()).getText()).to.contain("John Smith");
};

const expectPersonalDetailsAge = async () => {
  await expect(await $(PrimaryPersonSummaryPage.ageAnswer()).getText()).to.contain("50");
};

const expectReasonNoConfirmationAnswer = async () => {
  await expect(await $(PrimaryPersonSummaryPage.reasonNoConfirmationAnswer()).getText()).to.contain(
    "I did not visit section 2, so confirmation was not needed",
  );
};

const expectPersonalDetailsAgeExistingFalse = async () => {
  await expect(await $(PrimaryPersonSummaryPage.ageAnswer()).isExisting()).to.be.false;
};

const expectReasonNoConfirmationExistingFalse = async () => {
  await expect(await $(PrimaryPersonSummaryPage.reasonNoConfirmationAnswer()).isExisting()).to.be.false;
};
