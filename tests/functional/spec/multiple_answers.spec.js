import PersonalDetailPage from "../generated_pages/multiple_answers/personal-details-block.page.js";
import SubmitPage from "../generated_pages/multiple_answers/submit.page.js";

describe("Multiple Answers", () => {
  it("Given I complete a survey that has multiple answers for a question when I edit an answer then I appear on the page to edit my answer", () => {
    browser.openQuestionnaire("test_multiple_answers.json");
    $(PersonalDetailPage.firstName()).setValue("HAN");
    $(PersonalDetailPage.surname()).setValue("SOLO");
    $(PersonalDetailPage.submit()).click();
    $(SubmitPage.firstNameAnswerEdit()).click();
    expect(browser.getUrl()).to.contain(PersonalDetailPage.pageName);
    expect($(PersonalDetailPage.firstName()).isFocused()).to.be.true;
  });

  it("Given a survey has multiple answers for a question when I save the survey then the summary shows all the answers", () => {
    browser.openQuestionnaire("test_multiple_answers.json");
    $(PersonalDetailPage.firstName()).setValue("HAN");
    $(PersonalDetailPage.surname()).setValue("SOLO");
    $(PersonalDetailPage.submit()).click();
    expect($(SubmitPage.firstNameAnswer()).getText()).to.contain("HAN");
    expect($(SubmitPage.surnameAnswer()).getText()).to.contain("SOLO");
  });
});
