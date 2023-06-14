import { checkItemsInList } from "../helpers";
import AnyoneLiveAtListCollector from "../generated_pages/answer_action_redirect_to_list_add_block_radio/anyone-else-live-at.page";
import AnyoneLiveAtListCollectorAddPage from "../generated_pages/answer_action_redirect_to_list_add_block_radio/anyone-else-live-at-add.page";
import AnyoneLiveAtListCollectorRemovePage from "../generated_pages/answer_action_redirect_to_list_add_block_radio/anyone-else-live-at-remove.page";
import AnyoneUsuallyLiveAt from "../generated_pages/answer_action_redirect_to_list_add_block_radio/anyone-usually-live-at.page";

describe("Answer Action: Redirect To List Add Question (Radio)", () => {
  describe('Given the user is on a question with a "RedirectToListAddBlock" action enabled', () => {
    before("Launch survey", async () => {
      await browser.openQuestionnaire("test_answer_action_redirect_to_list_add_block_radio.json");
    });

    it('When the user answers "No", Then, they should be taken to straight the list collector.', async () => {
      await $(AnyoneUsuallyLiveAt.no()).click();
      await $(AnyoneUsuallyLiveAt.submit()).click();
      await expect(await browser.getUrl()).to.contain(AnyoneLiveAtListCollector.pageName);
    });

    it('When the user answers "Yes" then they should be taken to the list collector add question.', async () => {
      await browser.url(AnyoneUsuallyLiveAt.url());
      await $(AnyoneUsuallyLiveAt.yes()).click();
      await $(AnyoneUsuallyLiveAt.submit()).click();
      await expect(await browser.getUrl()).to.contain(AnyoneLiveAtListCollectorAddPage.pageName);
      await expect(await browser.getUrl()).to.contain("?previous=anyone-usually-live-at");
    });

    it('When the user clicks the "Previous" link from the add question then they should be taken to the block they came from, not the list collector', async () => {
      await $(AnyoneLiveAtListCollectorAddPage.previous()).click();
      await expect(await browser.getUrl()).to.contain(AnyoneUsuallyLiveAt.pageName);
    });

    it("When the user adds a household member, Then, they are taken to the list collector and the household members are displayed", async () => {
      await $(AnyoneUsuallyLiveAt.submit()).click();
      await $(AnyoneLiveAtListCollectorAddPage.firstName()).setValue("Marcus");
      await $(AnyoneLiveAtListCollectorAddPage.lastName()).setValue("Twin");
      await $(AnyoneLiveAtListCollectorAddPage.submit()).click();
      await expect(await browser.getUrl()).to.contain(AnyoneLiveAtListCollector.pageName);

      const peopleExpected = ["Marcus Twin"];
      checkItemsInList(peopleExpected, AnyoneLiveAtListCollector.listLabel);
    });

    it('When the user click the "Previous" link from the list collector, Then, they are taken to the last complete block', async () => {
      await $(AnyoneLiveAtListCollector.previous()).click();
      await expect(await browser.getUrl()).to.contain(AnyoneUsuallyLiveAt.pageName);
    });

    it("When the user resubmits the first block and then list is not empty, Then they are taken to the list collector", async () => {
      await $(AnyoneUsuallyLiveAt.submit()).click();
      await expect(await browser.getUrl()).to.contain(AnyoneLiveAtListCollector.pageName);
    });

    it("When the users removes the only person (Marcus Twain), Then, they are shown an empty list collector", async () => {
      await $(AnyoneLiveAtListCollector.listRemoveLink(1)).click();
      await $(AnyoneLiveAtListCollectorRemovePage.yes()).click();
      await $(AnyoneLiveAtListCollectorRemovePage.submit()).click();
      await expect(await browser.getUrl()).to.contain(AnyoneLiveAtListCollector.pageName);
      await expect(await $(AnyoneLiveAtListCollector.listLabel(1)).isExisting()).to.be.false;
    });

    it("When the user resubmits the first block and then list is empty, Then they are taken to the add question", async () => {
      await expect(await browser.getUrl()).to.contain(AnyoneLiveAtListCollector.pageName);

      await $(AnyoneLiveAtListCollector.previous()).click();
      await expect(await browser.getUrl()).to.contain(AnyoneUsuallyLiveAt.pageName);

      await $(AnyoneUsuallyLiveAt.submit()).click();
      await expect(await browser.getUrl()).to.contain(AnyoneLiveAtListCollectorAddPage.pageName);
    });
  });
});
