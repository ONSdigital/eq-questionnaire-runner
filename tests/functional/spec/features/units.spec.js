import SetLengthUnitsBlockPage from "../../generated_pages/unit_patterns/set-length-units-block.page.js";
import SetDurationUnitsBlockPage from "../../generated_pages/unit_patterns/set-duration-units-block.page.js";
import SetAreaUnitsBlockPage from "../../generated_pages/unit_patterns/set-area-units-block.page.js";
import SetVolumeUnitsBlockPage from "../../generated_pages/unit_patterns/set-volume-units-block.page.js";
import SubmitPage from "../../generated_pages/unit_patterns/submit.page.js";

describe("Units", () => {
  it("Given we do not set a language code and run the questionnaire, when we enter values for durations, they should be displayed on the summary with their units.", async ()=> {
    await browser.openQuestionnaire("test_unit_patterns.json", { language: "en" });
    await $(await SetLengthUnitsBlockPage.submit()).click();
    await expect(await $(await SetDurationUnitsBlockPage.durationHourUnit()).getText()).to.equal("hours");
    await expect(await $(await SetDurationUnitsBlockPage.durationYearUnit()).getText()).to.equal("years");
    await $(await SetDurationUnitsBlockPage.durationHour()).setValue(6);
    await $(await SetDurationUnitsBlockPage.durationYear()).setValue(20);
    await $(await SetDurationUnitsBlockPage.submit()).click();
    await $(await SetAreaUnitsBlockPage.submit()).click();
    await $(await SetVolumeUnitsBlockPage.submit()).click();
    await expect(await $(await SubmitPage.durationHour()).getText()).to.equal("6 hours");
    await expect(await $(await SubmitPage.durationYear()).getText()).to.equal("20 years");
  });

  it("Given we set a language code for welsh and run the questionnaire, when we enter values for durations, they should be displayed on the summary with their units.", async ()=> {
    await browser.openQuestionnaire("test_unit_patterns.json", { language: "cy" });
    await $(await SetLengthUnitsBlockPage.submit()).click();
    await expect(await $(await SetDurationUnitsBlockPage.durationHourUnit()).getText()).to.equal("awr");
    await expect(await $(await SetDurationUnitsBlockPage.durationYearUnit()).getText()).to.equal("flynedd");
    await $(await SetDurationUnitsBlockPage.durationHour()).setValue(6);
    await $(await SetDurationUnitsBlockPage.durationYear()).setValue(20);
    await $(await SetDurationUnitsBlockPage.submit()).click();
    await $(await SetAreaUnitsBlockPage.submit()).click();
    await $(await SetVolumeUnitsBlockPage.submit()).click();
    await expect(await $(await SubmitPage.durationHour()).getText()).to.equal("6 awr");
    await expect(await $(await SubmitPage.durationYear()).getText()).to.equal("20 mlynedd");
  });

  it("Given we open a questionnaire with unit labels, when the label is highlighted by the tooltip, then the long unit label should be displayed.", async ()=> {
    await browser.openQuestionnaire("test_unit_patterns.json", { language: "en" });
    await expect(await $(await SetLengthUnitsBlockPage.centimetresUnit()).getAttribute("title")).to.equal("centimeters");
    await expect(await $(await SetLengthUnitsBlockPage.metresUnit()).getAttribute("title")).to.equal("meters");
    await expect(await $(await SetLengthUnitsBlockPage.kilometresUnit()).getAttribute("title")).to.equal("kilometers");
    await expect(await $(await SetLengthUnitsBlockPage.milesUnit()).getAttribute("title")).to.equal("miles");
  });
});
