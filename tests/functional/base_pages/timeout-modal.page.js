class TimeoutModalBasePage {
  timer() {
    return ".ons-js-timeout-timer";
  }

  submit() {
    return ".ons-js-modal-btn";
  }

  acceptCookies() {
    return ".ons-js-accept-cookies";
  }
}

export default TimeoutModalBasePage;
export const TimeoutModalPage = new TimeoutModalBasePage();
