import SetLengthUnitsBlockPage from "../../generated_pages/unit_patterns/set-length-units-block.page.js";
import SetDurationUnitsBlockPage from "../../generated_pages/unit_patterns/set-duration-units-block.page.js";
import SetAreaUnitsBlockPage from "../../generated_pages/unit_patterns/set-area-units-block.page.js";
import SetVolumeUnitsBlockPage from "../../generated_pages/unit_patterns/set-volume-units-block.page.js";
import SetWeightUnitsBlockPage from "../../generated_pages/unit_patterns/set-weight-units-block.page.js";
import SubmitPage from "../../generated_pages/unit_patterns/submit.page.js";
import { click } from "../../helpers";
describe("Units", () => {
  it("Given we do not set a language code and run the questionnaire, when we enter values for durations, they should be displayed on the summary with their units.", async () => {
    await browser.openQuestionnaire("test_unit_patterns.json", { language: "en" });
    await click(SetLengthUnitsBlockPage.submit());
    await expect(await $(SetDurationUnitsBlockPage.durationHourUnit()).getText()).to.equal("hours");
    await expect(await $(SetDurationUnitsBlockPage.durationYearUnit()).getText()).to.equal("years");
    await $(SetDurationUnitsBlockPage.durationHour()).setValue(6);
    await $(SetDurationUnitsBlockPage.durationYear()).setValue(20);
    await click(SetDurationUnitsBlockPage.submit());
    await click(SetAreaUnitsBlockPage.submit());
    await click(SetVolumeUnitsBlockPage.submit());
    await click(SetWeightUnitsBlockPage.submit());
    await expect(await $(SubmitPage.durationHour()).getText()).to.equal("6 hours");
    await expect(await $(SubmitPage.durationYear()).getText()).to.equal("20 years");
  });

  it("Given we set a language code for welsh and run the questionnaire, when we enter values for durations, they should be displayed on the summary with their units.", async () => {
    await browser.openQuestionnaire("test_unit_patterns.json", { language: "cy" });
    await $(SetLengthUnitsBlockPage.submit()).scrollIntoView();
    await click(SetLengthUnitsBlockPage.submit());
    await expect(await $(SetDurationUnitsBlockPage.durationHourUnit()).getText()).to.equal("awr");
    await expect(await $(SetDurationUnitsBlockPage.durationYearUnit()).getText()).to.equal("flynedd");
    await $(SetDurationUnitsBlockPage.durationHour()).setValue(6);
    await $(SetDurationUnitsBlockPage.durationYear()).setValue(20);
    await $(SetDurationUnitsBlockPage.submit()).scrollIntoView();
    await click(SetDurationUnitsBlockPage.submit());
    await click(SetAreaUnitsBlockPage.submit());
    await click(SetVolumeUnitsBlockPage.submit());
    await click(SetWeightUnitsBlockPage.submit());
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
    await click(SetLengthUnitsBlockPage.submit());
    await click(SetDurationUnitsBlockPage.submit());
    await click(SetAreaUnitsBlockPage.submit());
    await click(SetVolumeUnitsBlockPage.submit());
    await expect(await $("body").getText()).to.have.string("tonnes");
  });

  it("Given we open a questionnaire with unit inputs, when the unit allows a maximum of 6 decimal places, then the correct number of decimal places should be displayed on the summary.", async () => {
    await browser.openQuestionnaire("test_unit_patterns.json", { language: "en" });
    await $(SetLengthUnitsBlockPage.submit()).click();
    await $(SetDurationUnitsBlockPage.submit()).click();
    await $(SetAreaUnitsBlockPage.submit()).click();
    await $(SetVolumeUnitsBlockPage.cubicCentimetres()).setValue(1.1);
    await $(SetVolumeUnitsBlockPage.cubicMetres()).setValue(1.12);
    await $(SetVolumeUnitsBlockPage.litres()).setValue(1.123);
    await $(SetVolumeUnitsBlockPage.hectolitres()).setValue(1.1234);
    await $(SetVolumeUnitsBlockPage.megalitres()).setValue("1.10000");
    await $(SetVolumeUnitsBlockPage.submit()).click();
    await $(SetWeightUnitsBlockPage.submit()).click();
    await expect(await $(SubmitPage.cubicCentimetres()).getText()).to.equal("1.1 cm³");
    await expect(await $(SubmitPage.cubicMetres()).getText()).to.equal("1.12 m³");
    await expect(await $(SubmitPage.litres()).getText()).to.equal("1.123 l");
    await expect(await $(SubmitPage.hectolitres()).getText()).to.equal("1.1234 hl");
    await expect(await $(SubmitPage.megalitres()).getText()).to.equal("1.10000 Ml");
  });
});
