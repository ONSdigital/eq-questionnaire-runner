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

export const assertSummaryValues = async (values) => {
  // check each summary value provided is present and that the number of them matches what is on the page
  // needs to include both dynamic and static answers on any summary with both
  const summaryValues = 'dd[class="ons-summary__values"]';
  await values.map(async (value, index) => {
    await expect(await $$(summaryValues)[index].getText()).to.equal(value);
  });
  await expect(await $$(summaryValues).length).to.equal(values.length);
};
