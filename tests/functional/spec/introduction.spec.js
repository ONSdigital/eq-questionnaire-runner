import IntroductionPage from "../generated_pages/introduction/introduction.page";

describe("Introduction page", () => {
  const introductionSchema = "test_introduction.json";
  beforeEach(async () => {
    await browser.openQuestionnaire(introductionSchema);
  });

  it("Given I start a survey, When I view the introduction page, Then I should be able to see introduction information", async () => {
    await browser.openQuestionnaire(introductionSchema);
    await expect(await $(IntroductionPage.useOfData()).getText()).to.contain("How we use your data");
    await expect(await $(IntroductionPage.useOfInformation()).getText()).to.contain(
      "Data should relate to all sites in England, Scotland and Wales unless otherwise stated."
    );
    await expect(await $(IntroductionPage.legalResponse()).getText()).to.contain("Your response is legally required");
    await expect(await $(IntroductionPage.legalBasis()).getText()).to.contain("Notice is given under section 999 of the Test Act 2000");
    await expect(await $(IntroductionPage.introDescription()).getText()).to.contain(
      "To take part, all you need to do is check that you have the information you need to answer the survey questions."
    );
  });
  it("Given I start a survey with introduction guidance set, When I view the introduction page, Then I should be able to see introduction guidance", async () => {
    await browser.openQuestionnaire(introductionSchema);
    await expect(await $(IntroductionPage.guidancePanel(1)).isDisplayed()).to.be.true;
    await expect(await $(IntroductionPage.guidancePanel(1)).getText()).to.contain("Coronavirus (COVID-19) guidance");
    await expect(await $(IntroductionPage.guidancePanel(1)).getText()).to.contain(
      "Explain your figures in the comment section to minimise us contacting you and to help us tell an industry story"
    );
  });
});
