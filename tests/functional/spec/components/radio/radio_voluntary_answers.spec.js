describe('Component: Radio', function() {
  describe('Given I start a Voluntary Radio survey', function() {
    const RadioVoluntaryTruePage = require('../../../generated_pages/radio_voluntary/radio-voluntary-true.page.js');
    const RadioVoluntaryFalsePage = require('../../../generated_pages/radio_voluntary/radio-voluntary-false.page.js');

    before(function() {
      browser.openQuestionnaire('test_radio_voluntary.json');
    });

    it('When I select a voluntary radio option, Then the clear button should be displayed', function() {
      $(RadioVoluntaryTruePage.coffee()).click();
      expect($(RadioVoluntaryTruePage.clearSelectionButton()).isDisplayed()).to.equal(true);
    });

    it('When I select a voluntary radio option and click the clear button, Then the radio option should not be selected and the clear button should not be displayed', function() {
      $(RadioVoluntaryTruePage.coffee()).click();
      $(RadioVoluntaryTruePage.clearSelectionButton()).click();
      expect($(RadioVoluntaryTruePage.coffee()).isSelected()).to.equal(false);
      expect($(RadioVoluntaryTruePage.clearSelectionButton()).isDisplayed()).to.equal(false);
    });

    it('When I clear a previously saved voluntary radio option and submit, Then when returning to the page the radio option is no longer selected', function() {
      $(RadioVoluntaryTruePage.coffee()).click();
      $(RadioVoluntaryTruePage.submit()).click();
      $(RadioVoluntaryTruePage.previous()).click();
      $(RadioVoluntaryTruePage.clearSelectionButton()).click();
      $(RadioVoluntaryTruePage.submit()).click();
      $(RadioVoluntaryTruePage.previous()).click();
      expect($(RadioVoluntaryTruePage.coffee()).isSelected()).to.equal(false);
      expect($(RadioVoluntaryTruePage.clearSelectionButton()).isDisplayed()).to.equal(false);
    });

    it('When I select a non-voluntary radio option, Then the clear button should not be displayed on the page', function() {
      $(RadioVoluntaryTruePage.submit()).click();
      $(RadioVoluntaryFalsePage.iceCream()).click();
      expect($(RadioVoluntaryFalsePage.clearSelectionButton()).isDisplayed()).to.equal(false);
    });
  });
});
