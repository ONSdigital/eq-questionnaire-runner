const checkPeopleInList = (peopleExpected, listLabel) => {
  $(listLabel(1)).waitForDisplayed();

  for (let i = 1; i <= peopleExpected.length; i++) {
    expect($(listLabel(i)).getText()).to.equal(peopleExpected[i - 1]);
  }
};

export default checkPeopleInList;
