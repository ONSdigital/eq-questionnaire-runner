import VariantBlockPage from "../generated_pages/list_collector_variants_primary_person/variant-block.page";
import PrimaryPersonListCollectorPage from "../generated_pages/list_collector_variants_primary_person/primary-person-list-collector.page";
import ListCollectorAddPage from "../generated_pages/list_collector_variants_primary_person/list-collector-add.page";
import ListCollectorPage from "../generated_pages/list_collector_variants_primary_person/list-collector.page";
import EditPersonPage from "../generated_pages/list_collector_variants_primary_person/list-collector-edit.page";
import SubmitPage from "../generated_pages/list_collector_variants_primary_person/submit.page";
import ThankYouPage from "../base_pages/thank-you.page.js";
import { click } from "../helpers";

describe("List collector with variants primary person", () => {
  describe("Given that person lives in house", () => {
    before("Load the survey", async () => {
      await browser.openQuestionnaire("test_list_collector_variants_primary_person.json");
      it("When the user is asked questions about whether they like variant, Then they are routed to section asking if they live in the house", async () => {
        await $(VariantBlockPage.yes()).click();
        await click(VariantBlockPage.submit());
        await expect(await $(PrimaryPersonListCollectorPage.legend()).getText()).toBe("Do you live here? (variant)");
      });
    });
  });
  describe("Given the user starts on the 'Do you like variant' question", () => {
    before("Load the survey", async () => {
      await browser.openQuestionnaire("test_list_collector_variants_primary_person.json");
    });
    it("When the user says that they do live there, Then they are shown as the primary person", async () => {
      await $(VariantBlockPage.yes()).click();
      await click(VariantBlockPage.submit());
      await $(PrimaryPersonListCollectorPage.youLiveHereYes()).click();
      await click(PrimaryPersonListCollectorPage.submit());
      await $(ListCollectorAddPage.firstName()).setValue("John");
      await $(ListCollectorAddPage.lastName()).setValue("Doe");
      await click(ListCollectorAddPage.submit());
      await expect(await $(ListCollectorPage.listLabel(1)).getText()).toBe("John Doe (You)");
    });
    it("When the user adds another person, Then they are shown in the list collector summary", async () => {
      await $(ListCollectorPage.yesLabel()).click();
      await click(ListCollectorPage.submit());
      await $(ListCollectorAddPage.firstName()).setValue("Samuel");
      await $(ListCollectorAddPage.lastName()).setValue("Clemens");
      await click(ListCollectorAddPage.submit());
      await expect(await $(ListCollectorPage.listLabel(2)).getText()).toBe("Samuel Clemens");
    });
    it("When the user goes back and answers 'No' for 'Do you live here' question, Then the primary person is not shown", async () => {
      await $(ListCollectorPage.previous()).click();
      await $(PrimaryPersonListCollectorPage.youLiveHereNo()).click();
      await click(PrimaryPersonListCollectorPage.submit());
      await expect(await $(ListCollectorPage.listLabel(1)).getText()).toBe("Samuel Clemens");
    });

    it("When the user adds another person, Then the user is able to add members of the household", async () => {
      await $(ListCollectorPage.yes()).click();
      await click(ListCollectorPage.submit());
      await expect(await $(ListCollectorAddPage.questionText()).getText()).toBe("What is the name of the person?");
      await $(ListCollectorAddPage.firstName()).setValue("Samuel");
      await $(ListCollectorAddPage.lastName()).setValue("Clemens");
      await click(ListCollectorAddPage.submit());
    });
    it("When the user adds the primary person again, Then the primary person is first in the list", async () => {
      await $(ListCollectorPage.previous()).click();
      await $(PrimaryPersonListCollectorPage.youLiveHereYes()).click();
      await click(PrimaryPersonListCollectorPage.submit());
      await $(ListCollectorAddPage.firstName()).setValue("Mark");
      await $(ListCollectorAddPage.lastName()).setValue("Twin");
      await click(ListCollectorAddPage.submit());
      await expect(await $(ListCollectorPage.listLabel(1)).getText()).toBe("Mark Twin (You)");
    });
    it("When the user views the summary, Then it does not show the remove link for the primary person", async () => {
      await expect(await $(ListCollectorPage.listRemoveLink(1)).isExisting()).toBe(false);
      await expect(await $(ListCollectorPage.listRemoveLink(2)).isExisting()).toBe(true);
    });
    it("When the user changes the primary person's name on the summary, Then the name should be updated", async () => {
      await $(ListCollectorPage.listEditLink(1)).click();
      await $(EditPersonPage.firstName()).setValue("John");
      await $(EditPersonPage.lastName()).setValue("Doe");
      await click(EditPersonPage.submit());
      await expect(await $(ListCollectorPage.listLabel(1)).getText()).toBe("John Doe (You)");
      await expect(await $(ListCollectorPage.listLabel(2)).getText()).toBe("Samuel Clemens");
    });

    it("When the user answers 'no' to add any person, Then the questionnaire shows the confirmation page", async () => {
      await $(ListCollectorPage.no()).click();
      await click(ListCollectorPage.submit());
      await expect(await browser.getUrl()).toContain(SubmitPage.url());
    });

    it("When the user attempts to submit, Then they are shown the confirmation page", async () => {
      await expect(await $(SubmitPage.guidance()).getText()).toBe("Please submit this survey to complete it");
    });

    it("When user updates the variant answer, Then it should come back to summary screen with updated answer", async () => {
      await $(SubmitPage.variantAnswerEdit()).click();
      await $(VariantBlockPage.no()).click();
      await click(VariantBlockPage.submit());
      await expect(await $(SubmitPage.variantAnswer()).getText()).toBe("No");
    });

    it("When the user submits, Then they are allowed to submit the survey", async () => {
      await click(SubmitPage.submit());
      await expect(await browser.getUrl()).toContain(ThankYouPage.pageName);
    });
  });
});

describe("Given the user starts on the 'Do you like variant' question", () => {
  before("Load the survey", async () => {
    await browser.openQuestionnaire("test_list_collector_variants_primary_person.json");
  });
  it("When the user answers 'No' for variant question, Then they are routed to section asking if they live in the house", async () => {
    await $(VariantBlockPage.no()).click();
    await click(VariantBlockPage.submit());
    await expect(await $(PrimaryPersonListCollectorPage.legend()).getText()).toBe("Do you live here?");
  });

  it("When the user says they do not live there and anyone else, Then confirmation screen is displayed", async () => {
    await $(PrimaryPersonListCollectorPage.youLiveHereNo()).click();
    await click(PrimaryPersonListCollectorPage.submit());
    await $(ListCollectorPage.no()).click();
    await click(ListCollectorPage.submit());

    await expect(await $(SubmitPage.guidance()).getText()).toBe("Please submit this survey to complete it");
  });
});
