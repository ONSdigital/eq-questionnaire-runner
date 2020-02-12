const SuggestionsPage = require('../generated_pages/textfield_suggestions/country-block.page.js');

describe('Suggestions', function() {
  it('Given I open a textfield with a suggestions url, when I have entered text, then it will show suggestions', function() {
    browser.openQuestionnaire('test_textfield_suggestions.json');
    $(SuggestionsPage.country()).setValue("Uni");
    $("#country-answer-listbox li").waitForDisplayed();
    expect($$('.js-typeahead-listbox li').length).to.not.equal(0);
  });
});
