export const checkItemsInList = async (itemsExpected, listLabel) => {
  await $(listLabel(1)).waitForDisplayed();

  for (let i = 1; i <= itemsExpected.length; i++) {
    await expect(await $(listLabel(i)).getText()).to.equal(itemsExpected[i - 1]);
  }
};

export const checkListItemComplete = async (listItemLabel) => {
  await expect(await $(listItemLabel).$(`.ons-summary__item-title-icon.ons-summary__item-title-icon--check`).isExisting()).to.be.true;
};
export const checkListItemIncomplete = async (listItemLabel) => {
  await expect(await $(listItemLabel).$(`.ons-summary__item-title-icon.ons-summary__item-title-icon--check`).isExisting()).to.be.false;
};

const assertSummaryFunction = (selector) => {
  return async (entities) => {
    // check each summary value/item/title is present and that the number of them matches what is on the page
    await entities.map(async (entity, index) => {
      await expect(await $$(selector)[index].getText()).to.equal(entity);
    });
    await expect(await $$(selector).length).to.equal(entities.length);
  };
};

export const assertSummaryValues = assertSummaryFunction('dd[class="ons-summary__values"]');
export const assertSummaryTitles = assertSummaryFunction('dt[class="ons-summary__title"]');
export const assertSummaryItems = assertSummaryFunction('dd[class="ons-summary__item--text"]');

export const repeatingAnswerChangeLink = (answerIndex) => {
  return $$('dd[class="ons-summary__actions"]')[answerIndex].$("a");
};

export const listItemIds = () => {
  return $$("[data-list-item-id]").map((listItem) => listItem.getAttribute("data-list-item-id"));
};

export const click = async (selector) => {
  await $(selector).scrollIntoView({ block: "center", inline: "center" });
  await $(selector).click();
};
