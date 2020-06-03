const CheckboxVisibleTruePage = require('../../../generated_pages/checkbox_detail_answer_visible/checkbox-visible-true.page.js');
const CheckboxVisibleFalsePage = require('../../../generated_pages/checkbox_detail_answer_visible/checkbox-visible-false.page.js');
const CheckboxVisibleNonePage = require('../../../generated_pages/checkbox_detail_answer_visible/checkbox-visible-none.page.js');
const MutuallyExclusivePage = require('../../../generated_pages/checkbox_detail_answer_visible/mutually-exclusive.page.js');


describe('Given I start a checkbox survey with a write-in option', function() {
  beforeEach(function() {
    browser.openQuestionnaire('test_checkbox_detail_answer_visible.json');
  });

  it('When I view a write-in checkbox and the visible option is set to true, Then the detail answer label should be displayed', function() {
    expect($(CheckboxVisibleTruePage.otherDetail()).isDisplayed()).to.be.true;
  });

  it('When I view a write-in checkbox and the visible option is set to true, Then after choosing non write-in option the detail answer label should be displayed', function() {
    $(CheckboxVisibleTruePage.coffee()).click();
    expect($(CheckboxVisibleTruePage.otherDetail()).isDisplayed()).to.be.true;
  });

  it('When I view a write-in checkbox and the visible option is set to false, Then the detail answer label should not be displayed', function() {
    $(CheckboxVisibleTruePage.coffee()).click();
    $(CheckboxVisibleTruePage.submit()).click();
    expect($(CheckboxVisibleFalsePage.otherDetail()).isDisplayed()).to.be.false;
  });

  it('When I view a write-in checkbox and the visible option is not set, Then the detail answer label should not be displayed', function() {
    $(CheckboxVisibleTruePage.coffee()).click();
    $(CheckboxVisibleTruePage.submit()).click();
    $(CheckboxVisibleFalsePage.iceCream()).click();
    $(CheckboxVisibleFalsePage.submit()).click();
    expect($(CheckboxVisibleNonePage.otherDetail()).isDisplayed()).to.be.false;
  });

  it('When I view a mutually exclusive, write-in checkbox and the visible option is set to true, Then the detail answer label should be displayed', function() {
    $(CheckboxVisibleTruePage.coffee()).click();
    $(CheckboxVisibleTruePage.submit()).click();
    $(CheckboxVisibleFalsePage.iceCream()).click();
    $(CheckboxVisibleFalsePage.submit()).click();
    $(CheckboxVisibleNonePage.blue()).click();
    $(CheckboxVisibleNonePage.submit()).click();
    expect($(MutuallyExclusivePage.otherDetail()).isDisplayed()).to.be.true;
  });
});
