export const checkPeopleInList = async (peopleExpected, listLabel) => {
  await $(listLabel(1)).waitForDisplayed();

  for (let i = 1; i <= peopleExpected.length; i++) {
    await expect(await $(listLabel(i)).getText()).to.equal(peopleExpected[i - 1]);
  }
};

export const checkCompaniesInList = async (companiesExpected, listLabel) => {
  await $(listLabel(1)).waitForDisplayed();

  expect(companiesExpected.length.to.equal(listLabel.length));
  for (let i = 1; i <= companiesExpected.length; i++) {
    await expect(await $(listLabel(i)).getText()).to.equal(companiesExpected[i - 1]);
  }
};

export const checkListItemComplete = async (listItemLabel) => {
  await expect(await $(listItemLabel).$(`.ons-summary__item-title-icon.ons-summary__item-title-icon--check`).isExisting()).to.be.true;
};
export const checkListItemIncomplete = async (listItemLabel) => {
  await expect(await $(listItemLabel).$(`.ons-summary__item-title-icon.ons-summary__item-title-icon--check`).isExisting()).to.be.false;
};
