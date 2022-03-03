import IntroductionPage from "../generated_pages/introduction/introduction.page";

describe("Introduction page", () => {
  const introductionSchema = "test_introduction.json";

  it("Given I start a survey, When I view the introduction page, Then I should be able to see introduction information", () => {
    browser.openQuestionnaire(introductionSchema);
    expect($(IntroductionPage.useOfData()).getText()).to.contain("How we use your data");
    expect($(IntroductionPage.useOfInformation()).getText()).to.contain("What you need to do next");
    expect($(IntroductionPage.legalResponse()).getText()).to.contain("Your response is legally required");
    expect($(IntroductionPage.legalBasis()).getText()).to.contain("Notice is given under section 999 of the Test Act 2000");
    expect($(IntroductionPage.introDescription()).getText()).to.contain(
      "To take part, all you need to do is check that you have the information you need to answer the survey questions."
    );
  });
});

describe("Introduction page", () => {
  const introductionSchema = "test_introduction_with_guidance.json";

  it("Given I start a survey with introduction guidance set, When I view the introduction page, Then I should be able to see introduction guidance", () => {
    browser.openQuestionnaire(introductionSchema);
    expect($("#item-guidance-business-details > div").getText()).to.contain("Coronavirus (COVID-19) guidance");
    expect($("#item-guidance-business-details > div > p").getText()).to.contain(
      "Explain your figures in the comment section to minimise us contacting you and to help us tell an industry story"
    );
  });
});
