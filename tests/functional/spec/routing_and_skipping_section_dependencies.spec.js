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

import HubPage from "../base_pages/hub.page";

describe("Routing and skipping section dependencies", () => {
  describe("Given the routing and skipping section dependencies questionnaire", () => {
    beforeEach("Load the survey", () => {
      browser.openQuestionnaire("test_routing_and_skipping_section_dependencies.json");
    });

    it("When I answer 'No' to skipping the age question, Then in the Primary Person section I am asked my name, age and why I didn't confirm skipping", () => {
      answerNoToSkipAgeQuestion();

      selectPrimaryPerson();
      answerAndSubmitNameQuestion();
      answerAndSubmitAgeQuestion();
      answerAndSubmitReasonForNoConfirmationQuestion();

      expectPersonalDetailsName();
      expectPersonalDetailsAge();
      expectReasonNoConfirmationAnswer();
    });

    it("When I answer 'Yes' to skipping the age question, Then in the Primary Person section I am only asked my name and why I didn't confirm skipping", () => {
      answerYesToSkipAgeQuestion();

      selectPrimaryPerson();
      answerAndSubmitNameQuestion();
      answerAndSubmitReasonForNoConfirmationQuestion();

      expectPersonalDetailsName();
      expectReasonNoConfirmationAnswer();
      expectPersonalDetailsAgeExistingFalse();
    });

    it("When I answer 'Yes' to skipping the age question and 'Yes' to are you sure in skip question confirmation section, Then in the Primary Person section I am just asked my name", () => {
      answerYesToSkipAgeQuestion();

      selectConfirmationSectionAndAnswerSecurityQuestion();
      answerYesToSkipConfirmationQuestion();

      selectPrimaryPerson();
      answerAndSubmitNameQuestion();

      expectPersonalDetailsName();
      expectPersonalDetailsAgeExistingFalse();
      expectReasonNoConfirmationExistingFalse();
    });

    it("When I answer 'Yes' to skipping the age question but 'No' to are you sure in skip question confirmation section, Then in the Primary Person section I am only asked my name and age", () => {
      answerYesToSkipAgeQuestion();

      selectConfirmationSectionAndAnswerSecurityQuestion();
      answerNoToSkipConfirmationQuestion();

      selectPrimaryPerson();
      answerAndSubmitNameQuestion();
      answerAndSubmitAgeQuestion();

      expectPersonalDetailsName();
      expectPersonalDetailsAge();
      expectReasonNoConfirmationExistingFalse();
    });

    it("When I answer 'No' to skipping the age question and populate the household, Then in each repeating section I am not asked their age", () => {
      answerNoToSkipAgeQuestion();

      addHouseholdMembers();

      $(HubPage.summaryRowLink("household-personal-details-section-1")).click();
      $(RepeatingSexPage.female()).click();
      $(RepeatingSexPage.submit()).click();
      $(RepeatingAgePage.answer()).setValue("45");
      $(RepeatingAgePage.submit()).click();

      expect($(HouseHoldPersonalDetailsSectionSummaryPage.repeatingSexAnswer()).getText()).to.contain("Female");
      expect($(HouseHoldPersonalDetailsSectionSummaryPage.repeatingAgeAnswer()).getText()).to.contain("45");

      $(HouseHoldPersonalDetailsSectionSummaryPage.submit()).click();
      $(HubPage.summaryRowLink("household-personal-details-section-2")).click();
      $(RepeatingSexPage.male()).click();
      $(RepeatingSexPage.submit()).click();
      $(RepeatingAgePage.answer()).setValue("10");
      $(RepeatingAgePage.submit()).click();

      expect($(HouseHoldPersonalDetailsSectionSummaryPage.repeatingSexAnswer()).getText()).to.contain("Male");
      expect($(HouseHoldPersonalDetailsSectionSummaryPage.repeatingAgeAnswer()).getText()).to.contain("10");
    });

    it("When I answer 'Yes' to skipping the age question and populate the household, Then in each repeating section I am not asked their age", () => {
      answerYesToSkipAgeQuestion();

      addHouseholdMembers();

      $(HubPage.summaryRowLink("household-personal-details-section-1")).click();
      $(RepeatingSexPage.female()).click();
      $(RepeatingSexPage.submit()).click();
      expect($(HouseHoldPersonalDetailsSectionSummaryPage.repeatingSexAnswer()).getText()).to.contain("Female");
      expect($(HouseHoldPersonalDetailsSectionSummaryPage.repeatingAgeAnswer()).isExisting()).to.be.false;

      $(HouseHoldPersonalDetailsSectionSummaryPage.submit()).click();
      $(HubPage.summaryRowLink("household-personal-details-section-2")).click();
      $(RepeatingSexPage.male()).click();
      $(RepeatingAgePage.submit()).click();

      expect($(HouseHoldPersonalDetailsSectionSummaryPage.repeatingSexAnswer()).getText()).to.contain("Male");
      expect($(HouseHoldPersonalDetailsSectionSummaryPage.repeatingAgeAnswer()).isExisting()).to.be.false;
    });
  });

  describe("Given the routing and skipping section dependencies questionnaire", () => {
    beforeEach("Load the survey", () => {
      browser.openQuestionnaire("test_routing_and_skipping_section_dependencies.json");
    });
    it("When I answer 'No' to skipping the section question and 'Yes' to enable the section question, Then the household summary will be visible on the hub", () => {
      answerNoToSkipEnableQuestionAndYesToEnableSection();

      expect($(HubPage.summaryRowLink("household-section")).isExisting()).to.be.true;
    });
    it("When I answer 'No' to skipping the section question and 'No' to enable the section question, Then the household summary will not be visible on the hub", () => {
      answerNoToSkipEnableQuestionAndNoToEnableSection();

      expect($(HubPage.summaryRowLink("household-section")).isExisting()).to.be.false;
    });
  });

  describe("Given the routing and skipping section dependencies questionnaire and I answered 'No' to skipping the section question and 'Yes' to enable the section question", () => {
    before("Load the survey", () => {
      browser.openQuestionnaire("test_routing_and_skipping_section_dependencies.json");
    });
    it("When I change my answer to skipping the section question to 'No', Then the household summary will not be visible on the hub", () => {
      answerNoToSkipEnableQuestionAndYesToEnableSection();
      changeSkipEnableQuestionToYes();

      expect($(HubPage.summaryRowLink("household-section")).isExisting()).to.be.false;
    });
  });

  describe("Given the routing and skipping section dependencies questionnaire and I answered 'Yes' to skipping the age question but 'No' to are you sure in skip question confirmation section", () => {
    before("Load the survey", () => {
      browser.openQuestionnaire("test_routing_and_skipping_section_dependencies.json");
    });

    it("When I change my answer to skipping age to 'No', removing the 'are you sure' question from the path, Then in the Primary Person section I am asked my name, age and why I didn't confirm skipping", () => {
      answerYesToSkipAgeQuestion();

      selectConfirmationSectionAndAnswerSecurityQuestion();
      answerNoToSkipConfirmationQuestion();

      editNoToSkipAgeQuestion();

      selectPrimaryPerson();
      answerAndSubmitNameQuestion();
      answerAndSubmitAgeQuestion();

      $(ReasonNoConfirmationPage.iDidButItWasRemovedFromThePathAsIChangedMyAnswerToNoOnTheSkipQuestion()).click();
      $(ReasonNoConfirmationPage.submit()).click();

      expectPersonalDetailsName();
      expectPersonalDetailsAge();
      expect($(PrimaryPersonSummaryPage.reasonNoConfirmationAnswer()).getText()).to.contain(
        "I did, but it was removed from the path as I changed my answer to No on the skip question"
      );
    });
  });

  describe("Given the routing and skipping section dependencies questionnaire and I answered 'Yes' to skipping the age question and complete the Primary Person section", () => {
    before("Load the survey", () => {
      browser.openQuestionnaire("test_routing_and_skipping_section_dependencies.json");
    });

    it("When I change my answer to skipping age to 'No', Then the Primary Person section status is changed to Partially completed", () => {
      answerYesToSkipAgeQuestion();
      selectPrimaryPerson();
      answerAndSubmitNameQuestion();
      answerAndSubmitReasonForNoConfirmationQuestion();
      $(PrimaryPersonSummaryPage.submit()).click();

      expect($(HubPage.summaryRowState("primary-person")).getText()).to.equal("Completed");

      editNoToSkipAgeQuestion();

      expect($(HubPage.summaryRowState("primary-person")).getText()).to.equal("Partially completed");
    });

    it("When I change my answer back to skipping age to 'Yes', Then the Primary Person section status is changed back to Completed", () => {
      editYesToSkipAgeQuestion();

      expect($(HubPage.summaryRowState("primary-person")).getText()).to.equal("Completed");
    });
  });

  describe("Given the routing and skipping section dependencies questionnaire and I answered 'Yes' to skipping the age question and add 2 household members but complete only one", () => {
    before("Load the survey", () => {
      browser.openQuestionnaire("test_routing_and_skipping_section_dependencies.json");
    });

    it("When I change my answer to skipping age to 'No', Then the completed household member status is changed to Partially completed and the other stays as not started", () => {
      answerYesToSkipAgeQuestion();
      addHouseholdMembers();
      $(HubPage.summaryRowLink("household-personal-details-section-1")).click();
      $(RepeatingSexPage.female()).click();
      $(RepeatingSexPage.submit()).click();
      $(HouseHoldPersonalDetailsSectionSummaryPage.submit()).click();

      editNoToSkipAgeQuestion();

      expect($(HubPage.summaryRowState("household-personal-details-section-1")).getText()).to.equal("Partially completed");
      expect($(HubPage.summaryRowState("household-personal-details-section-2")).getText()).to.equal("Not started");
    });

    it("When I change my answer back to skipping age to 'Yes', Then the Partially completed household member status is changed back to Completed and the other stays as not started", () => {
      editYesToSkipAgeQuestion();

      expect($(HubPage.summaryRowState("household-personal-details-section-1")).getText()).to.equal("Completed");
      expect($(HubPage.summaryRowState("household-personal-details-section-2")).getText()).to.equal("Not started");
    });
  });
});

const addHouseholdMembers = () => {
  $(HubPage.summaryRowLink("household-section")).click();
  $(ListCollectorPage.yes()).click();
  $(ListCollectorPage.submit()).click();
  $(ListCollectorAddPage.firstName()).setValue("Sarah");
  $(ListCollectorAddPage.lastName()).setValue("Smith");
  $(ListCollectorAddPage.submit()).click();
  $(ListCollectorPage.yes()).click();
  $(ListCollectorPage.submit()).click();
  $(ListCollectorAddPage.firstName()).setValue("Marcus");
  $(ListCollectorAddPage.lastName()).setValue("Smith");
  $(ListCollectorAddPage.submit()).click();
  $(ListCollectorPage.no()).click();
  $(ListCollectorPage.submit()).click();
  $(HouseholdSectionSummaryPage.submit()).click();
};

const selectPrimaryPerson = () => {
  $(HubPage.summaryRowLink("primary-person")).click();
};

const selectConfirmationSectionAndAnswerSecurityQuestion = () => {
  $(HubPage.summaryRowLink("skip-confirmation-section")).click();
  $(SecurityPage.yes()).click();
  $(SecurityPage.submit()).click();
};

const answerYesToSkipAgeQuestion = () => {
  $(HubPage.summaryRowLink("skip-section")).click();
  $(SkipAgePage.yes()).click();
  $(SkipAgePage.submit()).click();
  $(SkipEnableSectionPage.no()).click();
  $(SkipEnableSectionPage.submit()).click();
  $(EnableSectionPage.yes()).click();
  $(EnableSectionPage.submit()).click();
  $(SkipSectionSummaryPage.submit()).click();
};

const editNoToSkipAgeQuestion = () => {
  $(HubPage.summaryRowLink("skip-section")).click();
  $(SkipSectionSummaryPage.skipAgeAnswerEdit()).click();
  $(SkipAgePage.no()).click();
  $(SkipAgePage.submit()).click();
  $(SkipSectionSummaryPage.submit()).click();
};

const editYesToSkipAgeQuestion = () => {
  $(HubPage.summaryRowLink("skip-section")).click();
  $(SkipSectionSummaryPage.skipAgeAnswerEdit()).click();
  $(SkipAgePage.yes()).click();
  $(SkipAgePage.submit()).click();
  $(SkipSectionSummaryPage.submit()).click();
};

const answerNoToSkipAgeQuestion = () => {
  $(HubPage.summaryRowLink("skip-section")).click();
  $(SkipAgePage.no()).click();
  $(SkipAgePage.submit()).click();
  $(SkipEnableSectionPage.no()).click();
  $(SkipEnableSectionPage.submit()).click();
  $(EnableSectionPage.yes()).click();
  $(EnableSectionPage.submit()).click();
  $(SkipSectionSummaryPage.submit()).click();
};

const answerNoToSkipConfirmationQuestion = () => {
  $(SkipConfirmationPage.no()).click();
  $(SkipConfirmationPage.submit()).click();
  $(SkipConfirmationSectionSummaryPage.submit()).click();
};

const answerYesToSkipConfirmationQuestion = () => {
  $(SkipConfirmationPage.yes()).click();
  $(SkipConfirmationPage.submit()).click();
  $(SkipConfirmationSectionSummaryPage.submit()).click();
};

const answerNoToSkipEnableQuestionAndYesToEnableSection = () => {
  $(HubPage.summaryRowLink("skip-section")).click();
  $(SkipAgePage.no()).click();
  $(SkipAgePage.submit()).click();
  $(SkipEnableSectionPage.no()).click();
  $(SkipEnableSectionPage.submit()).click();
  $(EnableSectionPage.yes()).click();
  $(EnableSectionPage.submit()).click();
  $(SkipSectionSummaryPage.submit()).click();
};

const answerNoToSkipEnableQuestionAndNoToEnableSection = () => {
  $(HubPage.summaryRowLink("skip-section")).click();
  $(SkipAgePage.no()).click();
  $(SkipAgePage.submit()).click();
  $(SkipEnableSectionPage.no()).click();
  $(SkipEnableSectionPage.submit()).click();
  $(EnableSectionPage.no()).click();
  $(EnableSectionPage.submit()).click();
  $(SkipSectionSummaryPage.submit()).click();
};

const changeSkipEnableQuestionToYes = () => {
  $(HubPage.summaryRowLink("skip-section")).click();
  $(SkipSectionSummaryPage.skipHouseholdSectionAnswerEdit()).click();
  $(SkipEnableSectionPage.yes()).click();
  $(SkipEnableSectionPage.submit()).click();
  $(SkipSectionSummaryPage.submit()).click();
};

const answerAndSubmitNameQuestion = () => {
  $(NamePage.name()).setValue("John Smith");
  $(NamePage.submit()).click();
};

const answerAndSubmitAgeQuestion = () => {
  $(AgePage.answer()).setValue("50");
  $(AgePage.submit()).click();
};

const answerAndSubmitReasonForNoConfirmationQuestion = () => {
  $(ReasonNoConfirmationPage.iDidNotVisitSection2SoConfirmationWasNotNeeded()).click();
  $(ReasonNoConfirmationPage.submit()).click();
};

const expectPersonalDetailsName = () => {
  expect($(PrimaryPersonSummaryPage.nameAnswer()).getText()).to.contain("John Smith");
};

const expectPersonalDetailsAge = () => {
  expect($(PrimaryPersonSummaryPage.ageAnswer()).getText()).to.contain("50");
};

const expectReasonNoConfirmationAnswer = () => {
  expect($(PrimaryPersonSummaryPage.reasonNoConfirmationAnswer()).getText()).to.contain("I did not visit section 2, so confirmation was not needed");
};

const expectPersonalDetailsAgeExistingFalse = () => {
  expect($(PrimaryPersonSummaryPage.ageAnswer()).isExisting()).to.be.false;
};

const expectReasonNoConfirmationExistingFalse = () => {
  expect($(PrimaryPersonSummaryPage.reasonNoConfirmationAnswer()).isExisting()).to.be.false;
};
