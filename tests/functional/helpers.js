const checkPeopleInList = (peopleExpected, summaryPage) => {
    $(summaryPage.peopleListLabel(1)).waitForDisplayed();

    for (let i=1; i<=peopleExpected.length; i++) {
      expect($(summaryPage.peopleListLabel(i)).getText()).to.equal(peopleExpected[i-1]);
    }
};

module.exports = checkPeopleInList;
