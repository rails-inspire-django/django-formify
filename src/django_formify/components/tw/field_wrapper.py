from django_viewcomponent import component
from django_viewcomponent.fields import RendersOneField


@component.register("formify.tw.field_wrapper")
class FieldWrapperComponent(component.Component):
    label = RendersOneField()
    input = RendersOneField()
    field_helper_text_and_errors = RendersOneField()

    template_name = "formify/tailwind/components/field_wrapper.html"


@component.register("formify.tw.horizontal_field_wrapper")
class HorizontalFieldWrapperComponent(FieldWrapperComponent):
    template_name = "formify/tailwind/components/horizontal_field_wrapper.html"
