import VariantBlockPage from "../generated_pages/list_collector_variants_primary_person/variant-block.page";
import PrimaryPersonListCollectorPage from "../generated_pages/list_collector_variants_primary_person/primary-person-list-collector.page";
import ListCollectorAddPage from "../generated_pages/list_collector_variants_primary_person/list-collector-add.page";
import ListCollectorPage from "../generated_pages/list_collector_variants_primary_person/list-collector.page";
import EditPersonPage from "../generated_pages/list_collector_variants_primary_person/list-collector-edit.page";
import SubmitPage from "../generated_pages/list_collector_variants_primary_person/submit.page";
import ThankYouPage from "../base_pages/thank-you.page.js";

describe("List collector with variants primary person", () => {
  describe("Given that person lives in house", () => {
    before("Load the survey", () => {
      browser.openQuestionnaire("test_list_collector_variants_primary_person.json");
      it("when the user is asked questions about whether they like variant, Then they are routed to section asking if they live in the house", () => {
        $(VariantBlockPage.yes()).click();
        $(VariantBlockPage.submit()).click();
        expect($(PrimaryPersonListCollectorPage.legend()).getText()).to.contain("Do you live here? (variant)");
      });
    });
  });
  describe("Given the user starts on the 'Do you like variant' question", () => {
    before("Load the survey", () => {
      browser.openQuestionnaire("test_list_collector_variants_primary_person.json");
    });
    it("When the user says that they do live there, then they are shown as the primary person", () => {
      $(VariantBlockPage.yes()).click();
      $(VariantBlockPage.submit()).click();
      $(PrimaryPersonListCollectorPage.youLiveHereYes()).click();
      $(PrimaryPersonListCollectorPage.submit()).click();
      $(ListCollectorAddPage.firstName()).setValue("John");
      $(ListCollectorAddPage.lastName()).setValue("Doe");
      $(ListCollectorAddPage.submit()).click();
      expect($(ListCollectorPage.listLabel(1)).getText()).to.equal("John Doe (You)");
    });
    it("When the user adds another person, then they are shown in the list collector summary", () => {
      $(ListCollectorPage.yesLabel()).click();
      $(ListCollectorPage.submit()).click();
      $(ListCollectorAddPage.firstName()).setValue("Samuel");
      $(ListCollectorAddPage.lastName()).setValue("Clemens");
      $(ListCollectorAddPage.submit()).click();
      expect($(ListCollectorPage.listLabel(2)).getText()).to.equal("Samuel Clemens");
    });
    it("When the user goes back and answers 'No' for 'Do you live here' question, then the primary person is not shown", () => {
      $(ListCollectorPage.previous()).click();
      $(PrimaryPersonListCollectorPage.youLiveHereNo()).click();
      $(PrimaryPersonListCollectorPage.submit()).click();
      expect($(ListCollectorPage.listLabel(1)).getText()).to.equal("Samuel Clemens");
    });

    it("when the user adds another person, Then the user is able to add members of the household", () => {
      $(ListCollectorPage.yes()).click();
      $(ListCollectorPage.submit()).click();
      expect($(ListCollectorAddPage.questionText()).getText()).to.equal("What is the name of the person?");
      $(ListCollectorAddPage.firstName()).setValue("Samuel");
      $(ListCollectorAddPage.lastName()).setValue("Clemens");
      $(ListCollectorAddPage.submit()).click();
    });
    it("When the user adds the primary person again, then the primary person is first in the list", () => {
      $(ListCollectorPage.previous()).click();
      $(PrimaryPersonListCollectorPage.youLiveHereYes()).click();
      $(PrimaryPersonListCollectorPage.submit()).click();
      $(ListCollectorAddPage.firstName()).setValue("Mark");
      $(ListCollectorAddPage.lastName()).setValue("Twin");
      $(ListCollectorAddPage.submit()).click();
      expect($(ListCollectorPage.listLabel(1)).getText()).to.equal("Mark Twin (You)");
    });
    it("When the user views the summary, then it does not show the remove link for the primary person", () => {
      expect($(ListCollectorPage.listRemoveLink(1)).isExisting()).to.be.false;
      expect($(ListCollectorPage.listRemoveLink(2)).isExisting()).to.be.true;
    });
    it("When the user changes the primary person's name on the summary, then the name should be updated", () => {
      $(ListCollectorPage.listEditLink(1)).click();
      $(EditPersonPage.firstName()).setValue("John");
      $(EditPersonPage.lastName()).setValue("Doe");
      $(EditPersonPage.submit()).click();
      expect($(ListCollectorPage.listLabel(1)).getText()).to.equal("John Doe (You)");
      expect($(ListCollectorPage.listLabel(2)).getText()).to.equal("Samuel Clemens");
    });

    it("When the user answers 'no' to add any person, then the questionnaire shows the confirmation page", () => {
      $(ListCollectorPage.no()).click();
      $(ListCollectorPage.submit()).click();
      expect(browser.getUrl()).to.contain(SubmitPage.url());
    });

    it("When the user attempts to submit, then they are shown the confirmation page", () => {
      expect($(SubmitPage.guidance()).getText()).to.contain("Please submit this survey to complete it");
    });

    it("When user updates the variant answer, then it should come back to summary screen with updated answer", () => {
      $(SubmitPage.variantAnswerEdit()).click();
      $(VariantBlockPage.no()).click();
      $(VariantBlockPage.submit()).click();
      expect($(SubmitPage.variantAnswer()).getText()).to.equal("No");
    });

    it("When the user submits, then they are allowed to submit the survey", () => {
      $(SubmitPage.submit()).click();
      expect(browser.getUrl()).to.contain(ThankYouPage.pageName);
    });
  });
});

describe("Given the user starts on the 'Do you like variant' question", () => {
  before("Load the survey", () => {
    browser.openQuestionnaire("test_list_collector_variants_primary_person.json");
  });
  it("when the user answers 'No' for variant question, Then they are routed to section asking if they live in the house", () => {
    $(VariantBlockPage.no()).click();
    $(VariantBlockPage.submit()).click();
    expect($(PrimaryPersonListCollectorPage.legend()).getText()).to.contain("Do you live here?");
  });

  it("When the user says they do not live there and anyone else, then confirmation screen is displayed", () => {
    $(PrimaryPersonListCollectorPage.youLiveHereNo()).click();
    $(PrimaryPersonListCollectorPage.submit()).click();
    $(ListCollectorPage.no()).click();
    $(ListCollectorPage.submit()).click();

    expect($(SubmitPage.guidance()).getText()).to.contain("Please submit this survey to complete it");
  });
});
