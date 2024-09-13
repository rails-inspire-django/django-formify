from django_viewcomponent import component
from django_viewcomponent.fields import RendersOneField


@component.register("formify.tw.field_wrapper")
class FieldWrapperComponent(component.Component):
    label = RendersOneField()
    input = RendersOneField()
    field_helper_text_and_errors = RendersOneField()

    template_name = "formify/tw/field_wrapper.html"
