// You can't directly include question.page in a test. This just inherits from it.
import QuestionPage from "./question.page";

class GenericPage extends QuestionPage {
  constructor() {
    super("generic");
  }
}
export default new GenericPage();
