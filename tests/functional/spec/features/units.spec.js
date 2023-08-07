import SetLengthUnitsBlockPage from "../../generated_pages/unit_patterns/set-length-units-block.page.js";
import SetDurationUnitsBlockPage from "../../generated_pages/unit_patterns/set-duration-units-block.page.js";
import SetAreaUnitsBlockPage from "../../generated_pages/unit_patterns/set-area-units-block.page.js";
import SetVolumeUnitsBlockPage from "../../generated_pages/unit_patterns/set-volume-units-block.page.js";
import SetWeightUnitsBlockPage from "../../generated_pages/unit_patterns/set-weight-units-block.page.js";
import SubmitPage from "../../generated_pages/unit_patterns/submit.page.js";

describe("Units", () => {
  it("Given we do not set a language code and run the questionnaire, when we enter values for durations, they should be displayed on the summary with their units.", async () => {
    await browser.openQuestionnaire("test_unit_patterns.json", { language: "en" });
    await $(SetLengthUnitsBlockPage.submit()).click();
    await expect(await $(SetDurationUnitsBlockPage.durationHourUnit()).getText()).to.equal("hours");
    await expect(await $(SetDurationUnitsBlockPage.durationYearUnit()).getText()).to.equal("years");
    await $(SetDurationUnitsBlockPage.durationHour()).setValue(6);
    await $(SetDurationUnitsBlockPage.durationYear()).setValue(20);
    await $(SetDurationUnitsBlockPage.submit()).click();
    await $(SetAreaUnitsBlockPage.submit()).click();
    await $(SetVolumeUnitsBlockPage.submit()).click();
    await $(SetWeightUnitsBlockPage.submit()).click();
    await expect(await $(SubmitPage.durationHour()).getText()).to.equal("6 hours");
    await expect(await $(SubmitPage.durationYear()).getText()).to.equal("20 years");
  });

  it("Given we set a language code for welsh and run the questionnaire, when we enter values for durations, they should be displayed on the summary with their units.", async () => {
    await browser.openQuestionnaire("test_unit_patterns.json", { language: "cy" });
    await $(SetLengthUnitsBlockPage.submit()).scrollIntoView();
    await $(SetLengthUnitsBlockPage.submit()).click();
    await expect(await $(SetDurationUnitsBlockPage.durationHourUnit()).getText()).to.equal("awr");
    await expect(await $(SetDurationUnitsBlockPage.durationYearUnit()).getText()).to.equal("flynedd");
    await $(SetDurationUnitsBlockPage.durationHour()).setValue(6);
    await $(SetDurationUnitsBlockPage.durationYear()).setValue(20);
    await $(SetDurationUnitsBlockPage.submit()).scrollIntoView();
    await $(SetDurationUnitsBlockPage.submit()).click();
    await $(SetAreaUnitsBlockPage.submit()).click();
    await $(SetVolumeUnitsBlockPage.submit()).click();
    await $(SetWeightUnitsBlockPage.submit()).click();
    await expect(await $(SubmitPage.durationHour()).getText()).to.equal("6 awr");
    await expect(await $(SubmitPage.durationYear()).getText()).to.equal("20 mlynedd");
  });

  it("Given we open a questionnaire with unit labels, when the label is highlighted by the tooltip, then the long unit label should be displayed.", async () => {
    await browser.openQuestionnaire("test_unit_patterns.json", { language: "en" });
    await expect(await $(SetLengthUnitsBlockPage.centimetresUnit()).getAttribute("title")).to.equal("centimetres");
    await expect(await $(SetLengthUnitsBlockPage.metresUnit()).getAttribute("title")).to.equal("metres");
    await expect(await $(SetLengthUnitsBlockPage.kilometresUnit()).getAttribute("title")).to.equal("kilometres");
    await expect(await $(SetLengthUnitsBlockPage.milesUnit()).getAttribute("title")).to.equal("miles");
  });

  it("Given we open a questionnaire with unit labels, when the weight unit label is highlighted by the tooltip, then the correct unit label should be displayed.", async () => {
    await browser.openQuestionnaire("test_unit_patterns.json", { language: "en" });
    await $(SetLengthUnitsBlockPage.submit()).click();
    await $(SetDurationUnitsBlockPage.submit()).click();
    await $(SetAreaUnitsBlockPage.submit()).click();
    await $(SetVolumeUnitsBlockPage.submit()).click();
    await expect(await $("body").getText()).to.have.string("tons");
  });
});
