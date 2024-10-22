import { checkItemsInList, click } from "../../../helpers";
import AnyoneLiveAtListCollector from "../../../generated_pages/answer_action_redirect_to_list_add_block_checkbox/anyone-else-live-at.page";
import AnyoneLiveAtListCollectorAddPage from "../../../generated_pages/answer_action_redirect_to_list_add_block_checkbox/anyone-else-live-at-add.page";
import AnyoneLiveAtListCollectorRemovePage from "../../../generated_pages/answer_action_redirect_to_list_add_block_checkbox/anyone-else-live-at-remove.page";
import AnyoneUsuallyLiveAt from "../../../generated_pages/answer_action_redirect_to_list_add_block_checkbox/anyone-usually-live-at.page";

describe("Answer Action: Redirect To List Add Question (Checkbox)", () => {
  describe('Given the user is on a question with a "RedirectToListAddBlock" action enabled', () => {
    before("Launch survey", async () => {
      await browser.openQuestionnaire("test_answer_action_redirect_to_list_add_block_checkbox.json");
    });

    it('When the user selects "No", Then, they should be taken to the list collector.', async () => {
      await $(AnyoneUsuallyLiveAt.no()).click();
      await click(AnyoneUsuallyLiveAt.submit());
      await expect(browser).toHaveUrl(expect.stringContaining(AnyoneLiveAtListCollector.pageName));
    });

    it('When the user selects "Yes" then they should be taken to the list collector add question.', async () => {
      await browser.url(AnyoneUsuallyLiveAt.url());
      await $(AnyoneUsuallyLiveAt.iThinkSo()).click();
      await click(AnyoneUsuallyLiveAt.submit());
      await expect(browser).toHaveUrl(expect.stringContaining(AnyoneLiveAtListCollectorAddPage.pageName));
      await expect(browser).toHaveUrl(expect.stringContaining("?previous=anyone-usually-live-at"));
    });

    it('When the user clicks the "Previous" link from the add question then they should be taken to the block they came from, not the list collector', async () => {
      await $(AnyoneLiveAtListCollectorAddPage.previous()).click();
      await expect(browser).toHaveUrl(expect.stringContaining(AnyoneUsuallyLiveAt.pageName));
    });

    it("When the user adds a household member, Then, they are taken to the list collector and the household members are displayed", async () => {
      await click(AnyoneUsuallyLiveAt.submit());
      await $(AnyoneLiveAtListCollectorAddPage.firstName()).setValue("Marcus");
      await $(AnyoneLiveAtListCollectorAddPage.lastName()).setValue("Twin");
      await click(AnyoneLiveAtListCollectorAddPage.submit());
      await expect(browser).toHaveUrl(expect.stringContaining(AnyoneLiveAtListCollector.pageName));

      const peopleExpected = ["Marcus Twin"];
      await checkItemsInList(peopleExpected, AnyoneLiveAtListCollector.listLabel);
    });

    it('When the user click the "Previous" link from the list collector, Then, they are taken to the last complete block', async () => {
      await $(AnyoneLiveAtListCollector.previous()).click();
      await expect(browser).toHaveUrl(expect.stringContaining(AnyoneUsuallyLiveAt.pageName));
    });

    it("When the user resubmits the first block and then list is not empty, Then they are taken to the list collector", async () => {
      await click(AnyoneUsuallyLiveAt.submit());
      await expect(browser).toHaveUrl(expect.stringContaining(AnyoneLiveAtListCollector.pageName));
    });

    it("When the users removes the only person (Marcus Twain), Then, they are shown an empty list collector", async () => {
      await $(AnyoneLiveAtListCollector.listRemoveLink(1)).click();
      await $(AnyoneLiveAtListCollectorRemovePage.yes()).click();
      await click(AnyoneLiveAtListCollectorRemovePage.submit());
      await expect(browser).toHaveUrl(expect.stringContaining(AnyoneLiveAtListCollector.pageName));
      await expect(await $(AnyoneLiveAtListCollector.listLabel(1)).isExisting()).toBe(false);
    });

    it("When the user resubmits the first block and then list is empty, Then they are taken to the add question", async () => {
      await expect(browser).toHaveUrl(expect.stringContaining(AnyoneLiveAtListCollector.pageName));

      await $(AnyoneLiveAtListCollector.previous()).click();
      await expect(browser).toHaveUrl(expect.stringContaining(AnyoneUsuallyLiveAt.pageName));

      await click(AnyoneUsuallyLiveAt.submit());
      await expect(browser).toHaveUrl(expect.stringContaining(AnyoneLiveAtListCollectorAddPage.pageName));
    });
  });
});
