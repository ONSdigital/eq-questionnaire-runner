from app.schema.question import Question


class DateRangeQuestion(Question):
    def __init__(self):
        super().__init__()

    def validate(self, state):
        is_valid = super().validate(state)
        if is_valid:
            from_date = state.children[0].value
            to_date = state.children[1].value

            if to_date == from_date:
                state.is_valid = False
                state.errors = []
                state.errors.append(self.questionnaire.get_error_message("INVALID_DATE_RANGE_TO_FROM_SAME", self.id))
                return False

            if to_date < from_date:
                state.is_valid = False
                state.errors = []
                state.errors.append(self.questionnaire.get_error_message("INVALID_DATE_RANGE_TO_BEFORE_FROM", self.id))
                return False

        return is_valid
