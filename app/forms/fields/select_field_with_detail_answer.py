from wtforms import SelectField


class SelectFieldWithDetailAnswer(SelectField):
    """
    This custom field allows us to add the additional detail_answer_id to choices/options.
    This saves us having to later map options with their detail_answer.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __iter__(self):
        opts = dict(
            widget=self.option_widget, _name=self.name, _form=None, _meta=self.meta
        )
        for i, (value, label, checked, detail_answer_id) in enumerate(
            self.iter_choices()
        ):
            opt = self._Option(label=label, id='%s-%d' % (self.id, i), **opts)
            opt.process(None, value)
            opt.detail_answer_id = detail_answer_id
            opt.checked = checked
            yield opt

    def iter_choices(self):
        for value, label, detail_answer_id in self.choices:
            yield value, label, self.coerce(value) == self.data, detail_answer_id

    def pre_validate(self, form):
        for value, _, _ in self.choices:
            if value == self.data:
                break
        else:
            raise ValueError(self.gettext('Not a valid choice'))
