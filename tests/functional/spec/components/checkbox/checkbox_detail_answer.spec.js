const CheckboxVisibleTruePage = require('../../../generated_pages/checkbox_detail_answer/checkbox-visible-true.page.js');
const CheckboxVisibleFalsePage = require('../../../generated_pages/checkbox_detail_answer/checkbox-visible-false.page.js');
const CheckboxVisibleNonePage = require('../../../generated_pages/checkbox_detail_answer/checkbox-visible-none.page.js');
const MutuallyExclusivePage = require('../../../generated_pages/checkbox_detail_answer/mutually-exclusive.page.js');


describe('Given the checkbox detail_answer questionnaire,', function() {
  beforeEach(function() {
    browser.openQuestionnaire('test_checkbox_detail_answer.json');
  });
  it('When a checkbox has a detail_answer with visible set to true, Then the detail answer write-in field should be shown', function() {
    expect($(CheckboxVisibleTruePage.otherDetail()).isDisplayed()).to.be.true;
  });
  it('When a checkbox has a detail_answer with visible set to true and another answer is checked, then the detail answer write-in field should still be shown', function() {
    $(CheckboxVisibleTruePage.coffee()).click();
    expect($(CheckboxVisibleTruePage.otherDetail()).isDisplayed()).to.be.true;
  });
  it('When a checkbox has a detail_answer with visible set to false, Then the detail answer write-in field should not be shown', function() {
    $(CheckboxVisibleTruePage.coffee()).click();
    $(CheckboxVisibleTruePage.submit()).click();
    expect($(CheckboxVisibleFalsePage.otherDetail()).isDisplayed()).to.be.false;
  });
  it('When a checkbox has a detail_answer with visible not set, Then the detail answer write-in field should not be shown', function() {
    $(CheckboxVisibleTruePage.coffee()).click();
    $(CheckboxVisibleTruePage.submit()).click();
    $(CheckboxVisibleFalsePage.iceCream()).click();
    $(CheckboxVisibleFalsePage.submit()).click();
    expect($(CheckboxVisibleNonePage.otherDetail()).isDisplayed()).to.be.false;
  });
  it('When a mutually exclusive checkbox has a detail_answer with visible set to true, Then the detail answer write-in field should be shown', function() {
    $(CheckboxVisibleTruePage.coffee()).click();
    $(CheckboxVisibleTruePage.submit()).click();
    $(CheckboxVisibleFalsePage.iceCream()).click();
    $(CheckboxVisibleFalsePage.submit()).click();
    $(CheckboxVisibleNonePage.blue()).click();
    $(CheckboxVisibleNonePage.submit()).click();
    expect($(MutuallyExclusivePage.otherDetail()).isDisplayed()).to.be.true;
  });
});
