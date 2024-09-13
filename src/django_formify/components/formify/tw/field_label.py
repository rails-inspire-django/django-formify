from django_viewcomponent import component


@component.register("formify.tw.field_label")
class FieldLabelComponent(component.Component):
    def __init__(self, field, formify_helper, **kwargs):
        self.field = field
        self.formify_helper = formify_helper

    @property
    def should_render(self):
        return self.field.label and self.formify_helper.form_show_labels

    @property
    def asterisk_if_required(self):
        if self.field.field.required:
            return '<span class="asteriskField">*</span>'
        else:
            return ""

    template_name = "formify/tw/field_label.html"
