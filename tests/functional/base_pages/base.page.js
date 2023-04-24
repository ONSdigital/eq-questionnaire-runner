export default class BasePage {
  constructor(pageName) {
    this.pageName = pageName;
  }

  previous() {
    return 'a[id="top-previous"]';
  }

  heading() {
    return "h1";
  }

  warning() {
    return '[data-qa="warning"]';
  }

  guidance() {
    return '[data-qa="guidance"]';
  }

  acceptCookies() {
    return '[data-button="accept"]';
  }

  submit() {
    return '[data-qa="btn-submit"]';
  }

  saveSignOut() {
    return '[data-qa="btn-save-sign-out"]';
  }

  switchLanguage(languageCode) {
    return `a[href="?language_code=${languageCode}"]`;
  }
}
