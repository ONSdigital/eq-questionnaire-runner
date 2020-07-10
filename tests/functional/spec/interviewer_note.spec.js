import InitialInterstitialPage from "../generated_pages/interviewer_note/initial-interstitial-block.page.js";
import FavouriteTeamPage from "../generated_pages/interviewer_note/favourite-team-block.page.js";
import ConfirmPage from "../generated_pages/interviewer_note/confirm-block.page.js";
import FinalInterstitialPage from "../generated_pages/interviewer_note/final-interstitial-block.page.js";

describe("Interviewer Note", () => {
  beforeEach(() => {
    browser.openQuestionnaire("test_interviewer_note.json");
  });

  it("Given I start a survey, When I view interstitial page and the interviewer_note is set to true then I should be able to see interviewer note", () => {
    expect($(InitialInterstitialPage.questionText()).getText()).to.contain("Interviewer Note");
  });
  it("Given I start a survey, When I view question page and the interviewer_note is set to true then I should be able to see interviewer note", () => {
    $(InitialInterstitialPage.submit()).click();
    expect($(FavouriteTeamPage.questionText()).getText()).to.contain("Interviewer Note");
  });
  it("Given I start a survey, When I view question page and the interviewer_note is set to false then I should not be able to see interviewer note", () => {
    $(InitialInterstitialPage.submit()).click();
    $(FavouriteTeamPage.favouriteTeam()).setValue("TNS");
    $(FavouriteTeamPage.submit()).click();
    expect($(ConfirmPage.questionText()).getText()).to.not.contain("Interviewer Note");
  });
  it("Given I start a survey, When I view interstitial page and the interviewer_note is not set then I should not be able to see interviewer note", () => {
    $(InitialInterstitialPage.submit()).click();
    $(FavouriteTeamPage.favouriteTeam()).setValue("TNS");
    $(FavouriteTeamPage.submit()).click();
    $(ConfirmPage.yes()).click();
    $(ConfirmPage.submit()).click();
    expect($(FinalInterstitialPage.questionText()).getText()).to.not.contain("Interviewer Note");
  });
});
