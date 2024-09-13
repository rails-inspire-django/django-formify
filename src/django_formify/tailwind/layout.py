from django.template import Template
from django_viewcomponent import component

from django_formify.utils import flatatt


class Layout(component.Component):
    def __init__(self, *fields):
        self.fields = list(fields)

    def render(self, context_data):
        context = self.prepare_context(context_data)
        fields_html = " ".join(
            [
                child_component.render_from_parent_context(context)
                for child_component in self.fields
            ]
        )
        return fields_html


class Div(component.Component):
    template_name = "formify/tailwind/components/div.html"
    css_class = None

    def __init__(self, *fields, dom_id=None, css_class=None, template=None, **kwargs):
        self.fields = list(fields)
        if self.css_class and css_class:
            self.css_class += f" {css_class}"
        elif css_class:
            self.css_class = css_class
        self.dom_id = dom_id
        self.template_name = template or self.template_name
        self.flat_attrs = flatatt(kwargs)

    def get_context_data(self):
        context = super().get_context_data()
        self.fields_html = " ".join(
            [
                child_component.render_from_parent_context(context)
                for child_component in self.fields
            ]
        )
        return context


class HTML(component.Component):
    """
    It can contain pure HTML and it has access to the whole
    context of the page where the form is being rendered.

    Examples::

        HTML("{% if saved %}Data saved{% endif %}")
        HTML('<input type="hidden" name="{{ step_field }}" value="{{ step0 }}" />')
    """

    def __init__(self, html, **kwargs):
        self.html = html

    def get_template(self) -> Template:
        return Template(self.html)


class Button(component.Component):
    template_name = "formify/tailwind/components/button.html"
    default_css_class = "btn btn-primary"
    button_type = "button"

    def __init__(self, text=None, dom_id=None, css_class=None, template=None, **kwargs):
        self.text = text if text else "Button"
        self.dom_id = dom_id
        self.css_class = css_class or self.default_css_class
        self.template_name = template or self.template_name
        self.flat_attrs = flatatt(kwargs)

    def get_context_data(self):
        context = super().get_context_data()
        self.text_html = Template(str(self.text)).render(context)
        return context


class Submit(Button):
    button_type = "submit"


class Reset(Button):
    button_type = "reset"


class Field(component.Component):
    def __init__(self, field_name):
        self.field_name = field_name

    def render(self, context_data):
        context = self.prepare_context(context_data)
        formify_helper = context.get("formify_helper")
        field = formify_helper.form[self.field_name]
        return formify_helper.render_field(
            field=field, context=context, create_new_context=True
        )


class Fieldset(component.Component):
    template_name = "formify/tailwind/components/fieldset.html"

    def __init__(self, legend, *fields, css_class=None, dom_id=None, **kwargs):
        self.fields = list(fields)
        self.legend = legend
        self.css_class = css_class
        self.dom_id = dom_id
        self.flat_attrs = flatatt(kwargs)

    def get_context_data(self):
        context = super().get_context_data()
        self.fields_html = " ".join(
            [
                child_component.render_from_parent_context(context)
                for child_component in self.fields
            ]
        )
        return context
