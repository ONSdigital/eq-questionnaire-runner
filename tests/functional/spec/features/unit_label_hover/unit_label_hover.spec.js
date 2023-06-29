describe("Unit Label Hover", () => {
  describe("Given the language is set to English", () => {
    before("Launch survey", async () => {
      await browser.openQuestionnaire("test_unit_label_hover.json");
    });
    it("When we get to unit page, Then correct unit should be displayed.", async () => {
      await expect(await $("body").getText()).to.have.string("tonnes");
      await expect(await $("body").getText()).to.not.have.string("metric tons");
    });
  });
});
