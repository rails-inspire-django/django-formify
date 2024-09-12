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
    """
    The css classes are hard coded in this component.

    But you can also set them in the formify_helper instance and get them in the template using formify_helper.xxx
    """

    template_name = "formify/tailwind/components/horizontal_field_wrapper.html"
