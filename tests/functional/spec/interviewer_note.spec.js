import ConfirmPage from "../generated_pages/interviewer_note/confirm-block.page.js";
import FavouriteTeamPage from "../generated_pages/interviewer_note/favourite-team-block.page.js";
import FinalInterstitialPage from "../generated_pages/interviewer_note/final-interstitial-block.page.js";
import InitialInterstitialPage from "../generated_pages/interviewer_note/initial-interstitial-block.page.js";
import { click } from "../helpers";

describe("Given I start a survey", () => {
  before(async () => {
    await browser.openQuestionnaire("test_interviewer_note.json");
  });

  it("When I view interstitial page and the interviewer_note is set to true then I should be able to see interviewer note", async () => {
    await expect(await $(InitialInterstitialPage.questionText()).getText()).to.contain("Interviewer note");
  });
  it("When I view question page and the interviewer_note is set to true then I should be able to see interviewer note", async () => {
    await click(InitialInterstitialPage.submit());
    await expect(await $(FavouriteTeamPage.questionText()).getText()).to.contain("Interviewer note");
  });
  it("When I view question page and the interviewer_note is set to false then I should not be able to see interviewer note", async () => {
    await $(FavouriteTeamPage.favouriteTeam()).setValue("TNS");
    await click(FavouriteTeamPage.submit());
    await expect(await $(ConfirmPage.questionText()).getText()).to.not.contain("Interviewer note");
  });
  it("When I view interstitial page and the interviewer_note is not set then I should not be able to see interviewer note", async () => {
    await $(ConfirmPage.yes()).click();
    await click(ConfirmPage.submit());
    await expect(await $(FinalInterstitialPage.questionText()).getText()).to.not.contain("Interviewer note");
  });
});
