const sectionOne = require('../../../generated_pages/section_enabled_checkbox/section-1-block.page');
const sectionTwo = require('../../../generated_pages/section_enabled_checkbox/section-2-block.page');
const summary = require('../../../generated_pages/section_enabled_checkbox/summary.page');


describe('Feature: Section Enabled Based On Checkbox Answers', () => {
  beforeEach('Open survey', () => {
    browser.openQuestionnaire('test_section_enabled_checkbox.json');
  });

  describe('Given the user selects `Section 2`', () => {

    it('When the user submits and proceed to the next page, Then, section 2 should be displayed', () => {
      $(sectionOne.section1Section2()).click();
      $(sectionOne.submit()).click();

      expect(browser.getUrl()).to.contain('section-2-blocks');
    });

  });

  describe('Given the user selects `Section 3`', () => {
    it('When the user submits and proceed to the next page, Then, section 2 should not be displayed and section 3 should be displayed', () => {
      $(sectionOne.section1Section3()).click();
      $(sectionOne.submit()).click();

      expect(browser.getUrl()).to.contain('section-3-block');
    });
  });

  describe('Given the user selects `Section 2` and `Section 3`', () => {
    it('When the user submits and proceed to the next page, Then, section 2 and section 3 should be displayed', () => {
      $(sectionOne.section1Section2()).click();
      $(sectionOne.section1Section3()).click();
      $(sectionOne.submit()).click();

      expect(browser.getUrl()).to.contain('section-2-block');
      $(sectionTwo.submit()).click();
      expect(browser.getUrl()).to.contain('section-3-block');
    });
  });

  describe('Given the user selects `Neither`', () => {
    it('When the user submits the answer, Then, they should be taken straight to the summary', () => {
      $(sectionOne.section1ExclusiveNeither()).click();
      $(sectionOne.submit()).click();

      expect(browser.getUrl()).to.contain('summary');
      expect($(summary.section2Question()).isExisting()).to.be.false;
      expect($(summary.section3Question()).isExisting()).to.be.false;
    });
  });

});
