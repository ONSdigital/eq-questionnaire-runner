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
