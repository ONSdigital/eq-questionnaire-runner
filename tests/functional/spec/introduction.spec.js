import IntroductionPage from "../generated_pages/introduction/introduction.page";

describe("Introduction page", () => {
  const introductionSchema = "test_introduction.json";
  beforeEach(async () => {
    await browser.openQuestionnaire(introductionSchema);
  });

  it("Given I start a survey, When I view the introduction page, Then I should be able to see introduction information", async () => {
    await browser.openQuestionnaire(introductionSchema);
    await expect(await $(IntroductionPage.useOfData()).getText()).toContain("How we use your data");
    await expect(await $(IntroductionPage.useOfInformation()).getText()).toContain(
      "Data should relate to all sites in England, Scotland and Wales unless otherwise stated.",
    );
    await expect(await $(IntroductionPage.legalResponse()).getText()).toBe("Your response is legally required");
    await expect(await $(IntroductionPage.legalBasis()).getText()).toBe("Notice is given under section 999 of the Test Act 2000");
    await expect(await $(IntroductionPage.introDescription()).getText()).toBe(
      "To take part, all you need to do is check that you have the information you need to answer the survey questions.",
    );
  });
  it("Given I start a survey, When preview content is set on the introduction page, Then the content headings should be displayed at the correct level", async () => {
    await browser.openQuestionnaire(introductionSchema);
    const introQuestionH3Selector = `${IntroductionPage.introQuestion()} h3`;
    const h3Exists = await $(introQuestionH3Selector).isExisting();
    await expect(h3Exists).toBe(true);
  });
  it("Given I start a survey with introduction guidance set, When I view the introduction page, Then I should be able to see introduction guidance", async () => {
    await browser.openQuestionnaire(introductionSchema);
    await expect(await $(IntroductionPage.guidancePanel(1)).isDisplayed()).toBe(true);
    await expect(await $(IntroductionPage.guidancePanel(1)).getText()).toContain("Coronavirus (COVID-19) guidance");
    await expect(await $(IntroductionPage.guidancePanel(1)).getText()).toContain(
      "Explain your figures in the comment section to minimise us contacting you and to help us tell an industry story",
    );
  });
});
