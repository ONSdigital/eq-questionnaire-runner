const sectionOne = require('../../../generated_pages/section_enabled_hub/section-1-block.page');
const hubPage = require('../../../base_pages/hub.page');

describe('Feature: Section Enabled With Hub', () => {
  beforeEach('Open survey', () => {
    browser.openQuestionnaire('test_section_enabled_hub.json');
  });

  describe('Given the user selects `Section 2`', () => {

    it('When the user submits and proceed to the next page, Then, only section 2 should be displayed on the hub', () => {
      $(sectionOne.section1Section2()).click();
      $(sectionOne.submit()).click();

      expect($(hubPage.summaryRowState(2)).isDisplayed()).to.be.true;
      expect($(hubPage.summaryRowTitle(2)).getText()).to.equal('Section 2');

      expect($(hubPage.summaryRowState(3)).isDisplayed()).to.be.false;
    });

  });

  describe('Given the user selects `Section 3`', () => {
    it('When the user submits and proceed to the next page, Then, section 2 should not be displayed and section 3 should be displayed', () => {
      $(sectionOne.section1Section3()).click();
      $(sectionOne.submit()).click();

      expect($(hubPage.summaryRowState(2)).isDisplayed()).to.be.true;
      expect($(hubPage.summaryRowTitle(2)).getText()).to.equal('Section 3');

      expect($(hubPage.summaryRowState(3)).isDisplayed()).to.be.false;
    });
  });

  describe('Given the user selects `Section 2` and `Section 3`', () => {
    it('When the user submits and proceed to the hub, Then, section 2 and section 3 should be displayed', () => {
      $(sectionOne.section1Section2()).click();
      $(sectionOne.section1Section3()).click();
      $(sectionOne.submit()).click();

      expect($(hubPage.summaryRowState(2)).isDisplayed()).to.be.true;
      expect($(hubPage.summaryRowTitle(2)).getText()).to.equal('Section 2');

      expect($(hubPage.summaryRowState(3)).isDisplayed()).to.be.true;
      expect($(hubPage.summaryRowTitle(3)).getText()).to.equal('Section 3');
    });
  });

  describe('Given the user selects `Neither`', () => {
    it('When the user submits the answer, Then, hub should not display any other section and should be in the `Completed` state.', () => {
      $(sectionOne.section1ExclusiveNeither()).click();
      $(sectionOne.submit()).click();

      expect($(hubPage.summaryRowState(2)).isDisplayed()).to.be.false;
      expect($(hubPage.summaryRowState(3)).isDisplayed()).to.be.false;

      expect($(hubPage.submit()).getText()).to.equal('Submit survey');
      expect($(hubPage.displayedName()).getText()).to.equal('Submit survey');
    });
  });

});
