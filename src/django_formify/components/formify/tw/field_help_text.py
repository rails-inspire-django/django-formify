from django_viewcomponent import component


@component.register("formify.tw.field_help_text")
class FieldHelpTextComponent(component.Component):
    def __init__(self, field, formify_helper, **kwargs):
        self.field = field
        self.formify_helper = formify_helper

    @property
    def should_render(self):
        return self.field.help_text

    template_name = "formify/tw/field_help_text.html"
