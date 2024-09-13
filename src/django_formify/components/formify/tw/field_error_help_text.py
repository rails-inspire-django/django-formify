from django_viewcomponent import component


@component.register("formify.tw.field_error_help_text")
class FieldErrorHelpTextComponent(component.Component):
    def __init__(self, field, formify_helper, **kwargs):
        self.field = field
        self.formify_helper = formify_helper

    template_name = "formify/tw/field_error_help_text.html"
