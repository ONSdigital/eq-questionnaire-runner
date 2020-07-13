const checkPeopleInList = (peopleExpected, listLabel) => {
  $(listLabel(0)).waitForDisplayed();

  for (let i = 1; i <= peopleExpected.length; i++) {
    expect($(listLabel(i)).getText()).to.equal(peopleExpected[i]);
  }
};

export default checkPeopleInList;
