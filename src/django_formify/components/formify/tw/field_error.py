from django_viewcomponent import component


@component.register("formify.tw.field_error")
class FieldErrorComponent(component.Component):
    def __init__(self, field, formify_helper, **kwargs):
        self.field = field
        self.formify_helper = formify_helper

    @property
    def should_render(self):
        return self.field.errors and self.formify_helper.form_show_errors

    template_name = "formify/tw/field_error.html"
