describe('Component: Radio', function() {
  describe('Given I start a Radio survey with a write-in option', function() {
    const RadioOpenTruePage = require('../../../generated_pages/radio_open/radio-open-true.page.js');
    const RadioOpenFalsePage = require('../../../generated_pages/radio_open/radio-open-false.page.js');
    const RadioOpenNonePage = require('../../../generated_pages/radio_open/radio-open-none.page.js');


    it('When I view a write-in radio and the open option is set to true, detail answer label should be displayed', function() {
      browser.openQuestionnaire('test_radio_open.json');
      $(RadioOpenTruePage.coffee()).click();
      expect($(RadioOpenTruePage.otherDetail()).isDisplayed()).to.be.true;
    });

    it('When I view a write-in radio and the open option is set to false, detail answer label should not be displayed', function() {
      browser.openQuestionnaire('test_radio_open.json');
      $(RadioOpenTruePage.coffee()).click();
      $(RadioOpenTruePage.submit()).click();
      $(RadioOpenFalsePage.iceCream()).click();
      expect($(RadioOpenFalsePage.otherDetail()).isDisplayed()).to.be.false;
    });

    it('When I view a write-in radio and the open option is not set, detail answer label should not be displayed', function() {
      browser.openQuestionnaire('test_radio_open.json');
      $(RadioOpenTruePage.coffee()).click();
      $(RadioOpenFalsePage.submit()).click();
      $(RadioOpenFalsePage.iceCream()).click();
      $(RadioOpenFalsePage.submit()).click();
      $(RadioOpenNonePage.blue()).click();
      expect($(RadioOpenNonePage.otherDetail()).isDisplayed()).to.be.false;
    });
  });
});
