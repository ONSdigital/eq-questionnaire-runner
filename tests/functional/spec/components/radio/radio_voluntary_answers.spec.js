describe('Component: Radio', function() {
  describe('Given I start a Voluntary Radio survey', function() {
    const RadioVoluntaryTruePage = require('../../../generated_pages/radio_voluntary/radio-voluntary-true.page.js');
    const RadioVoluntaryFalsePage = require('../../../generated_pages/radio_voluntary/radio-voluntary-false.page.js');

    before(function() {
      browser.openQuestionnaire('test_radio_voluntary.json');
    });

    it('When I have selected a radio option, Then the clear button should be displayed on the page', function() {
       $(RadioVoluntaryTruePage.coffee()).click();
       expect($(RadioVoluntaryTruePage.clearSelectionButton()).isDisplayed()).to.be.true;
     });
     it('When I have selected a radio option and clicked clear button, Then radio option should not be selected and clear button should not be displayed', function() {
       $(RadioVoluntaryTruePage.coffee()).click();
       $(RadioVoluntaryTruePage.clearSelectionButton()).click();
       expect($(RadioVoluntaryTruePage.coffee()).isSelected()).to.be.false;
       expect($(RadioVoluntaryTruePage.clearSelectionButton()).isDisplayed()).to.be.false;
     });
     it('When I have clicked clear button and clicked submit button, Then when I click previous button, radio option should not be selected and clear button should not be displayed', function() {
       $(RadioVoluntaryTruePage.coffee()).click();
       $(RadioVoluntaryTruePage.clearSelectionButton()).click();
       $(RadioVoluntaryTruePage.submit()).click();
       $(RadioVoluntaryTruePage.previous()).click();
       expect($(RadioVoluntaryTruePage.coffee()).isSelected()).to.be.false;
       expect($(RadioVoluntaryTruePage.clearSelectionButton()).isDisplayed()).to.be.false;
     });
     it('When I have selected a radio option, Then the clear button should not be displayed on the page', function() {
       $(RadioVoluntaryTruePage.coffee()).click();
       $(RadioVoluntaryTruePage.submit()).click();
       $(RadioVoluntaryFalsePage.iceCream()).click();
       expect($(RadioVoluntaryFalsePage.clearSelectionButton()).isDisplayed()).to.be.false;
     });
  });
});
