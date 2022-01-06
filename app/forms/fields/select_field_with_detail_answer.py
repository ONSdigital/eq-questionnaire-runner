from wtforms import SelectField
from wtforms.validators import ValidationError


class SelectFieldWithDetailAnswer(SelectField):
    """
    This custom field allows us to add the additional detail_answer_id to choices/options.
    This saves us having to later map options with their detail_answer.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __iter__(self):
        opts = dict(
            widget=self.option_widget, name=self.name, _form=None, _meta=self.meta
        )
        for i, (value, label, checked, detail_answer_id) in enumerate(
            self.iter_choices()
        ):
            opt = self._Option(label=label, id=f"{self.id}-{i}", **opts)
            opt.process(None, value)
            opt.detail_answer_id = detail_answer_id
            opt.checked = checked
            yield opt

    def iter_choices(self):
        for value, label, detail_answer_id in self.choices:
            yield value, label, self.coerce(value) == self.data, detail_answer_id

    def pre_validate(self, _):
        for _, _, match, _ in self.iter_choices():
            if match:
                break
        else:
            raise ValidationError(self.gettext("Not a valid choice."))
