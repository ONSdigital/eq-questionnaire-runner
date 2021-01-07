import SuggestionsPage from "../generated_pages/textfield_suggestions/country-block.page.js";
import MultipleSuggestionsPage from "../generated_pages/textfield_suggestions/country-block-multiple-selections.page.js";

describe("Suggestions", () => {
  it("Given I open a textfield with a suggestions url, when I have entered text, then it will show suggestions", () => {
    browser.openQuestionnaire("test_textfield_suggestions.json");
    $(SuggestionsPage.country()).setValue("Uni");
    $("#country-answer-listbox li").waitForDisplayed();
    expect($$(".js-autosuggest-listbox li").length).to.not.equal(0);
  });
});

describe("Suggestions", () => {
  it("Given I open a textfield with a suggestions url, when I have entered text and picked suggestion from a list, then after typing more text it will show new suggestions", () => {
    browser.openQuestionnaire("test_textfield_suggestions.json");
    $(SuggestionsPage.country()).setValue("United States of America");
    $(SuggestionsPage.submit()).click();
    $(MultipleSuggestionsPage.countryMultipleSelections()).click();
    browser.keys("Ita");
    $("#country-multiple-selections-answer-listbox li").waitForDisplayed();
    expect($$(".js-autosuggest-listbox li").length).to.equal(2);
    $("#country-multiple-selections-answer-listbox__option--0").click();
    $(MultipleSuggestionsPage.countryMultipleSelections()).click();
    // Browser needs to pause before typing starts, otherwise this sequence is executed almost instantly
    browser.pause(500);
    browser.keys(" United States");
    $("#country-multiple-selections-answer-listbox li").waitForDisplayed();
    expect($$(".js-autosuggest-listbox li").length).to.equal(3);
  });
});
