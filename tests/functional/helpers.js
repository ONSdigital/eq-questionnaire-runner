const checkPeopleInList = (peopleExpected, listLabel) => {
  $(listLabel(0)).waitForDisplayed();

  for (let i = 1; i <= peopleExpected.length; i++) {
    expect($(listLabel(i - 1)).getText()).to.equal(peopleExpected[i - 1]);
  }
};

export default checkPeopleInList;
