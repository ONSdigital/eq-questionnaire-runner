import CheckBox from "../generated_pages/multiple_checkbox_answers/checkbox.page";

describe("Multiple Checkbox Answers", () => {
  describe("Given I have completed a questionnaire that has checkbox multiple answers for a question", () => {
    beforeEach("Load the questionnaire", () => {
      browser.openQuestionnaire("test_multiple_checkbox_answers.json");
    });

    it("When I am on the question page, Then the correct instruction fields should be displayed", () => {
      expect($("body").getText()).to.have.string("Select your favourite topping");
      expect($("body").getText()).to.have.string("Select your favourite base");
    });

    it("When I am on the question page, Then all answers should have a label", () => {
      expect($(CheckBox.firstLegend()).getText()).to.equal("Topping");
      expect($(CheckBox.secondLegend()).getText()).to.equal("Base");
    });
  });
});
