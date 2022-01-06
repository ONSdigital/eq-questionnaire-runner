from wtforms import SelectMultipleField


class MultipleSelectFieldWithDetailAnswer(SelectMultipleField):
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
            selected = self.data is not None and self.coerce(value) in self.data
            yield value, label, selected, detail_answer_id
