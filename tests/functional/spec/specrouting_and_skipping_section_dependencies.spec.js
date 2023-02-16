import AgePage from "../generated_pages/new_routing_and_skipping_section_dependencies/age.page";
import HouseHoldPersonalDetailsSectionSummaryPage from "../generated_pages/new_routing_and_skipping_section_dependencies/household-personal-details-section-summary.page";
import HouseholdSectionSummaryPage from "../generated_pages/new_routing_and_skipping_section_dependencies/household-section-summary.page";
import ListCollectorAddPage from "../generated_pages/new_routing_and_skipping_section_dependencies/list-collector-add.page";
import ListCollectorPage from "../generated_pages/new_routing_and_skipping_section_dependencies/list-collector.page";
import NamePage from "../generated_pages/new_routing_and_skipping_section_dependencies/name-block.page";
import PrimaryPersonSummaryPage from "../generated_pages/new_routing_and_skipping_section_dependencies/primary-person-summary.page";
import ReasonNoConfirmationPage from "../generated_pages/new_routing_and_skipping_section_dependencies/reason-no-confirmation.page";
import RepeatingAgePage from "../generated_pages/new_routing_and_skipping_section_dependencies/repeating-age.page";
import RepeatingSexPage from "../generated_pages/new_routing_and_skipping_section_dependencies/repeating-sex.page";
import SecurityPage from "../generated_pages/new_routing_and_skipping_section_dependencies/security.page";
import SkipAgePage from "../generated_pages/new_routing_and_skipping_section_dependencies/skip-age.page";
import SkipEnableSectionPage from "../generated_pages/new_routing_and_skipping_section_dependencies/skip-household-section.page";
import EnableSectionPage from "../generated_pages/new_routing_and_skipping_section_dependencies/enable-section.page";
import SkipConfirmationPage from "../generated_pages/new_routing_and_skipping_section_dependencies/skip-confirmation.page";
import SkipConfirmationSectionSummaryPage from "../generated_pages/new_routing_and_skipping_section_dependencies/skip-confirmation-section-summary.page";
import SkipSectionSummaryPage from "../generated_pages/new_routing_and_skipping_section_dependencies/skip-section-summary.page";

import HubPage from "../base_pages/hub.page";

describe("Routing and skipping section dependencies", () => {
  describe("Given the routing and skipping section dependencies questionnaire", () => {
    beforeEach("Load the survey", async ()=> {
      await browser.openQuestionnaire("test_new_routing_and_skipping_section_dependencies.json");
    });

    it("When I answer 'No' to skipping the age question, Then in the Primary Person section I am asked my name, age and why I didn't confirm skipping", async ()=> {
      answerNoToSkipAgeQuestion();

      selectPrimaryPerson();
      answerAndSubmitNameQuestion();
      answerAndSubmitAgeQuestion();
      answerAndSubmitReasonForNoConfirmationQuestion();

      expectPersonalDetailsName();
      expectPersonalDetailsAge();
      expectReasonNoConfirmationAnswer();
    });

    it("When I answer 'Yes' to skipping the age question, Then in the Primary Person section I am only asked my name and why I didn't confirm skipping", async ()=> {
      answerYesToSkipAgeQuestion();

      selectPrimaryPerson();
      answerAndSubmitNameQuestion();
      answerAndSubmitReasonForNoConfirmationQuestion();

      expectPersonalDetailsName();
      expectReasonNoConfirmationAnswer();
      expectPersonalDetailsAgeExistingFalse();
    });

    it("When I answer 'Yes' to skipping the age question and 'Yes' to are you sure in skip question confirmation section, Then in the Primary Person section I am just asked my name", async ()=> {
      answerYesToSkipAgeQuestion();

      selectConfirmationSectionAndAnswerSecurityQuestion();
      answerYesToSkipConfirmationQuestion();

      selectPrimaryPerson();
      answerAndSubmitNameQuestion();

      expectPersonalDetailsName();
      expectPersonalDetailsAgeExistingFalse();
      expectReasonNoConfirmationExistingFalse();
    });

    it("When I answer 'Yes' to skipping the age question but 'No' to are you sure in skip question confirmation section, Then in the Primary Person section I am only asked my name and age", async ()=> {
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

    it("When I answer 'No' to skipping the age question and populate the household, Then in each repeating section I am not asked their age", async ()=> {
      answerNoToSkipAgeQuestion();

      addHouseholdMembers();

      await $(await HubPage.summaryRowLink("household-personal-details-section-1")).click();
      await $(await RepeatingSexPage.female()).click();
      await $(await RepeatingSexPage.submit()).click();
      await $(await RepeatingAgePage.answer()).setValue("45");
      await $(await RepeatingAgePage.submit()).click();

      await expect(await $(await HouseHoldPersonalDetailsSectionSummaryPage.repeatingSexAnswer()).getText()).to.contain("Female");
      await expect(await $(await HouseHoldPersonalDetailsSectionSummaryPage.repeatingAgeAnswer()).getText()).to.contain("45");

      await $(await HouseHoldPersonalDetailsSectionSummaryPage.submit()).click();
      await $(await HubPage.summaryRowLink("household-personal-details-section-2")).click();
      await $(await RepeatingSexPage.male()).click();
      await $(await RepeatingSexPage.submit()).click();
      await $(await RepeatingAgePage.answer()).setValue("10");
      await $(await RepeatingAgePage.submit()).click();

      await expect(await $(await HouseHoldPersonalDetailsSectionSummaryPage.repeatingSexAnswer()).getText()).to.contain("Male");
      await expect(await $(await HouseHoldPersonalDetailsSectionSummaryPage.repeatingAgeAnswer()).getText()).to.contain("10");
    });

    it("When I answer 'Yes' to skipping the age question and populate the household, Then in each repeating section I am not asked their age", async ()=> {
      answerYesToSkipAgeQuestion();

      addHouseholdMembers();

      await $(await HubPage.summaryRowLink("household-personal-details-section-1")).click();
      await $(await RepeatingSexPage.female()).click();
      await $(await RepeatingSexPage.submit()).click();
      await expect(await $(await HouseHoldPersonalDetailsSectionSummaryPage.repeatingSexAnswer()).getText()).to.contain("Female");
      await expect(await $(await HouseHoldPersonalDetailsSectionSummaryPage.repeatingAgeAnswer()).isExisting()).to.be.false;

      await $(await HouseHoldPersonalDetailsSectionSummaryPage.submit()).click();
      await $(await HubPage.summaryRowLink("household-personal-details-section-2")).click();
      await $(await RepeatingSexPage.male()).click();
      await $(await RepeatingAgePage.submit()).click();

      await expect(await $(await HouseHoldPersonalDetailsSectionSummaryPage.repeatingSexAnswer()).getText()).to.contain("Male");
      await expect(await $(await HouseHoldPersonalDetailsSectionSummaryPage.repeatingAgeAnswer()).isExisting()).to.be.false;
    });
  });

  describe("Given the routing and skipping section dependencies questionnaire", () => {
    beforeEach("Load the survey", async ()=> {
      await browser.openQuestionnaire("test_new_routing_and_skipping_section_dependencies.json");
    });
    it("When I answer 'No' to skipping the section question and 'Yes' to enable the section question, Then the household summary will be visible on the hub", async ()=> {
      answerNoToSkipEnableQuestionAndYesToEnableSection();

      await expect(await $(await HubPage.summaryRowLink("household-section")).isExisting()).to.be.true;
    });
    it("When I answer 'No' to skipping the section question and 'No' to enable the section question, Then the household summary will not be visible on the hub", async ()=> {
      answerNoToSkipEnableQuestionAndNoToEnableSection();

      await expect(await $(await HubPage.summaryRowLink("household-section")).isExisting()).to.be.false;
    });
  });

  describe("Given the routing and skipping section dependencies questionnaire and I answered 'No' to skipping the section question and 'Yes' to enable the section question", () => {
    before("Load the survey", async ()=> {
      await browser.openQuestionnaire("test_new_routing_and_skipping_section_dependencies.json");
    });
    it("When I change my answer to skipping the section question to 'No', Then the household summary will not be visible on the hub", async ()=> {
      answerNoToSkipEnableQuestionAndYesToEnableSection();
      changeSkipEnableQuestionToYes();

      await expect(await $(await HubPage.summaryRowLink("household-section")).isExisting()).to.be.false;
    });
  });

  describe("Given the routing and skipping section dependencies questionnaire and I answered 'Yes' to skipping the age question but 'No' to are you sure in skip question confirmation section", () => {
    before("Load the survey", async ()=> {
      await browser.openQuestionnaire("test_new_routing_and_skipping_section_dependencies.json");
    });

    it("When I change my answer to skipping age to 'No', removing the 'are you sure' question from the path, Then in the Primary Person section I am asked my name, age and why I didn't confirm skipping", async ()=> {
      answerYesToSkipAgeQuestion();

      selectConfirmationSectionAndAnswerSecurityQuestion();
      answerNoToSkipConfirmationQuestion();

      editNoToSkipAgeQuestion();

      selectPrimaryPerson();
      answerAndSubmitNameQuestion();
      answerAndSubmitAgeQuestion();

      await $(await ReasonNoConfirmationPage.iDidButItWasRemovedFromThePathAsIChangedMyAnswerToNoOnTheSkipQuestion()).click();
      await $(await ReasonNoConfirmationPage.submit()).click();

      expectPersonalDetailsName();
      expectPersonalDetailsAge();
      await expect(await $(await PrimaryPersonSummaryPage.reasonNoConfirmationAnswer()).getText()).to.contain(
        "I did, but it was removed from the path as I changed my answer to No on the skip question"
      );
    });
  });

  describe("Given the routing and skipping section dependencies questionnaire and I answered 'Yes' to skipping the age question and complete the Primary Person section", () => {
    before("Load the survey", async ()=> {
      await browser.openQuestionnaire("test_new_routing_and_skipping_section_dependencies.json");
    });

    it("When I change my answer to skipping age to 'No', Then the Primary Person section status is changed to Partially completed", async ()=> {
      answerYesToSkipAgeQuestion();
      selectPrimaryPerson();
      answerAndSubmitNameQuestion();
      answerAndSubmitReasonForNoConfirmationQuestion();
      await $(await PrimaryPersonSummaryPage.submit()).click();

      await expect(await $(await HubPage.summaryRowState("primary-person")).getText()).to.equal("Completed");

      editNoToSkipAgeQuestion();

      await expect(await $(await HubPage.summaryRowState("primary-person")).getText()).to.equal("Partially completed");
    });

    it("When I change my answer back to skipping age to 'Yes', Then the Primary Person section status is changed back to Completed", async ()=> {
      editYesToSkipAgeQuestion();

      await expect(await $(await HubPage.summaryRowState("primary-person")).getText()).to.equal("Completed");
    });
  });

  describe("Given the routing and skipping section dependencies questionnaire and I answered 'Yes' to skipping the age question and add 2 household members but complete only one", () => {
    before("Load the survey", async ()=> {
      await browser.openQuestionnaire("test_new_routing_and_skipping_section_dependencies.json");
    });

    it("When I change my answer to skipping age to 'No', Then the completed household member status is changed to Partially completed and the other stays as not started", async ()=> {
      answerYesToSkipAgeQuestion();
      addHouseholdMembers();
      await $(await HubPage.summaryRowLink("household-personal-details-section-1")).click();
      await $(await RepeatingSexPage.female()).click();
      await $(await RepeatingSexPage.submit()).click();
      await $(await HouseHoldPersonalDetailsSectionSummaryPage.submit()).click();

      editNoToSkipAgeQuestion();

      await expect(await $(await HubPage.summaryRowState("household-personal-details-section-1")).getText()).to.equal("Partially completed");
      await expect(await $(await HubPage.summaryRowState("household-personal-details-section-2")).getText()).to.equal("Not started");
    });

    it("When I change my answer back to skipping age to 'Yes', Then the Partially completed household member status is changed back to Completed and the other stays as not started", async ()=> {
      editYesToSkipAgeQuestion();

      await expect(await $(await HubPage.summaryRowState("household-personal-details-section-1")).getText()).to.equal("Completed");
      await expect(await $(await HubPage.summaryRowState("household-personal-details-section-2")).getText()).to.equal("Not started");
    });
  });
});

const addHouseholdMembers = async ()=> {
  await $(await HubPage.summaryRowLink("household-section")).click();
  await $(await ListCollectorPage.yes()).click();
  await $(await ListCollectorPage.submit()).click();
  await $(await ListCollectorAddPage.firstName()).setValue("Sarah");
  await $(await ListCollectorAddPage.lastName()).setValue("Smith");
  await $(await ListCollectorAddPage.submit()).click();
  await $(await ListCollectorPage.yes()).click();
  await $(await ListCollectorPage.submit()).click();
  await $(await ListCollectorAddPage.firstName()).setValue("Marcus");
  await $(await ListCollectorAddPage.lastName()).setValue("Smith");
  await $(await ListCollectorAddPage.submit()).click();
  await $(await ListCollectorPage.no()).click();
  await $(await ListCollectorPage.submit()).click();
  await $(await HouseholdSectionSummaryPage.submit()).click();
};

const selectPrimaryPerson = async ()=> {
  await $(await HubPage.summaryRowLink("primary-person")).click();
};

const selectConfirmationSectionAndAnswerSecurityQuestion = async ()=> {
  await $(await HubPage.summaryRowLink("skip-confirmation-section")).click();
  await $(await SecurityPage.yes()).click();
  await $(await SecurityPage.submit()).click();
};

const answerYesToSkipAgeQuestion = async ()=> {
  await $(await HubPage.summaryRowLink("skip-section")).click();
  await $(await SkipAgePage.yes()).click();
  await $(await SkipAgePage.submit()).click();
  await $(await SkipEnableSectionPage.no()).click();
  await $(await SkipEnableSectionPage.submit()).click();
  await $(await EnableSectionPage.yes()).click();
  await $(await EnableSectionPage.submit()).click();
  await $(await SkipSectionSummaryPage.submit()).click();
};

const editNoToSkipAgeQuestion = async ()=> {
  await $(await HubPage.summaryRowLink("skip-section")).click();
  await $(await SkipSectionSummaryPage.skipAgeAnswerEdit()).click();
  await $(await SkipAgePage.no()).click();
  await $(await SkipAgePage.submit()).click();
  await $(await SkipSectionSummaryPage.submit()).click();
};

const editYesToSkipAgeQuestion = async ()=> {
  await $(await HubPage.summaryRowLink("skip-section")).click();
  await $(await SkipSectionSummaryPage.skipAgeAnswerEdit()).click();
  await $(await SkipAgePage.yes()).click();
  await $(await SkipAgePage.submit()).click();
  await $(await SkipSectionSummaryPage.submit()).click();
};

const answerNoToSkipAgeQuestion = async ()=> {
  await $(await HubPage.summaryRowLink("skip-section")).click();
  await $(await SkipAgePage.no()).click();
  await $(await SkipAgePage.submit()).click();
  await $(await SkipEnableSectionPage.no()).click();
  await $(await SkipEnableSectionPage.submit()).click();
  await $(await EnableSectionPage.yes()).click();
  await $(await EnableSectionPage.submit()).click();
  await $(await SkipSectionSummaryPage.submit()).click();
};

const answerNoToSkipConfirmationQuestion = async ()=> {
  await $(await SkipConfirmationPage.no()).click();
  await $(await SkipConfirmationPage.submit()).click();
  await $(await SkipConfirmationSectionSummaryPage.submit()).click();
};

const answerYesToSkipConfirmationQuestion = async ()=> {
  await $(await SkipConfirmationPage.yes()).click();
  await $(await SkipConfirmationPage.submit()).click();
  await $(await SkipConfirmationSectionSummaryPage.submit()).click();
};

const answerNoToSkipEnableQuestionAndYesToEnableSection = async ()=> {
  await $(await HubPage.summaryRowLink("skip-section")).click();
  await $(await SkipAgePage.no()).click();
  await $(await SkipAgePage.submit()).click();
  await $(await SkipEnableSectionPage.no()).click();
  await $(await SkipEnableSectionPage.submit()).click();
  await $(await EnableSectionPage.yes()).click();
  await $(await EnableSectionPage.submit()).click();
  await $(await SkipSectionSummaryPage.submit()).click();
};

const answerNoToSkipEnableQuestionAndNoToEnableSection = async ()=> {
  await $(await HubPage.summaryRowLink("skip-section")).click();
  await $(await SkipAgePage.no()).click();
  await $(await SkipAgePage.submit()).click();
  await $(await SkipEnableSectionPage.no()).click();
  await $(await SkipEnableSectionPage.submit()).click();
  await $(await EnableSectionPage.no()).click();
  await $(await EnableSectionPage.submit()).click();
  await $(await SkipSectionSummaryPage.submit()).click();
};

const changeSkipEnableQuestionToYes = async ()=> {
  await $(await HubPage.summaryRowLink("skip-section")).click();
  await $(await SkipSectionSummaryPage.skipHouseholdSectionAnswerEdit()).click();
  await $(await SkipEnableSectionPage.yes()).click();
  await $(await SkipEnableSectionPage.submit()).click();
  await $(await SkipSectionSummaryPage.submit()).click();
};

const answerAndSubmitNameQuestion = async ()=> {
  await $(await NamePage.name()).setValue("John Smith");
  await $(await NamePage.submit()).click();
};

const answerAndSubmitAgeQuestion = async ()=> {
  await $(await AgePage.answer()).setValue("50");
  await $(await AgePage.submit()).click();
};

const answerAndSubmitReasonForNoConfirmationQuestion = async ()=> {
  await $(await ReasonNoConfirmationPage.iDidNotVisitSection2SoConfirmationWasNotNeeded()).click();
  await $(await ReasonNoConfirmationPage.submit()).click();
};

const expectPersonalDetailsName = async ()=> {
  await expect(await $(await PrimaryPersonSummaryPage.nameAnswer()).getText()).to.contain("John Smith");
};

const expectPersonalDetailsAge = async ()=> {
  await expect(await $(await PrimaryPersonSummaryPage.ageAnswer()).getText()).to.contain("50");
};

const expectReasonNoConfirmationAnswer = async ()=> {
  await expect(await $(await PrimaryPersonSummaryPage.reasonNoConfirmationAnswer()).getText()).to.contain("I did not visit section 2, so confirmation was not needed");
};

const expectPersonalDetailsAgeExistingFalse = async ()=> {
  await expect(await $(await PrimaryPersonSummaryPage.ageAnswer()).isExisting()).to.be.false;
};

const expectReasonNoConfirmationExistingFalse = async ()=> {
  await expect(await $(await PrimaryPersonSummaryPage.reasonNoConfirmationAnswer()).isExisting()).to.be.false;
};
