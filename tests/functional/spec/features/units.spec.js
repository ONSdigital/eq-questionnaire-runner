import SetLengthUnitsBlockPage from "../../generated_pages/unit_patterns/set-length-units-block.page.js";
import SetDurationUnitsBlockPage from "../../generated_pages/unit_patterns/set-duration-units-block.page.js";
import SetAreaUnitsBlockPage from "../../generated_pages/unit_patterns/set-area-units-block.page.js";
import SetVolumeUnitsBlockPage from "../../generated_pages/unit_patterns/set-volume-units-block.page.js";
import SubmitPage from "../../generated_pages/unit_patterns/submit.page.js";

describe("Units", () => {
  it("Given we do not set a language code and run the questionnaire, when we enter values for durations, they should be displayed on the summary with their units.", () => {
    browser.openQuestionnaire("test_unit_patterns.json", { language: "en" });
    $(SetLengthUnitsBlockPage.submit()).click();
    expect($(SetDurationUnitsBlockPage.durationHourUnit()).getText()).to.equal("hours");
    expect($(SetDurationUnitsBlockPage.durationYearUnit()).getText()).to.equal("years");
    $(SetDurationUnitsBlockPage.durationHour()).setValue(6);
    $(SetDurationUnitsBlockPage.durationYear()).setValue(20);
    $(SetDurationUnitsBlockPage.submit()).click();
    $(SetAreaUnitsBlockPage.submit()).click();
    $(SetVolumeUnitsBlockPage.submit()).click();
    expect($(SubmitPage.durationHour()).getText()).to.equal("6 hours");
    expect($(SubmitPage.durationYear()).getText()).to.equal("20 years");
  });

  it("Given we set a language code for welsh and run the questionnaire, when we enter values for durations, they should be displayed on the summary with their units.", () => {
    browser.openQuestionnaire("test_unit_patterns.json", { language: "cy" });
    $(SetLengthUnitsBlockPage.submit()).click();
    expect($(SetDurationUnitsBlockPage.durationHourUnit()).getText()).to.equal("awr");
    expect($(SetDurationUnitsBlockPage.durationYearUnit()).getText()).to.equal("flynedd");
    $(SetDurationUnitsBlockPage.durationHour()).setValue(6);
    $(SetDurationUnitsBlockPage.durationYear()).setValue(20);
    $(SetDurationUnitsBlockPage.submit()).click();
    $(SetAreaUnitsBlockPage.submit()).click();
    $(SetVolumeUnitsBlockPage.submit()).click();
    expect($(SubmitPage.durationHour()).getText()).to.equal("6 awr");
    expect($(SubmitPage.durationYear()).getText()).to.equal("20 mlynedd");
  });

  it("Given we open a questionnaire with unit labels, when the label is highlighted by the tooltip, then the long unit label should be displayed.", () => {
    browser.openQuestionnaire("test_unit_patterns.json", { language: "en" });
    expect($(SetLengthUnitsBlockPage.centimetres()).getAttribute("title")).to.equal("centimeters");
    expect($(SetLengthUnitsBlockPage.metres()).getAttribute("title")).to.equal("meters");
    expect($(SetLengthUnitsBlockPage.kilometres()).getAttribute("title")).to.equal("kilometers");
    expect($(SetLengthUnitsBlockPage.miles()).getAttribute("title")).to.equal("miles");
  });
});
