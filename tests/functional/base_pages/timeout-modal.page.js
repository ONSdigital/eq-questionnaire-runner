class TimeoutModalBasePage {
  timer() {
    return ".ons-js-timeout-timer";
  }

  submit() {
    return ".ons-js-modal-btn";
  }
}

export default TimeoutModalBasePage;
export const TimeoutModalPage = new TimeoutModalBasePage();
