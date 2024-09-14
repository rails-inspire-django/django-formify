import copy
import re

from django.template.base import Template
from django.template.context import Context
from django.template.loader import get_template
from django.utils.safestring import SafeString

from django_formify.tailwind.layout import Field, Layout, Submit
from django_formify.utils import camel_to_snake, init_formify_helper_for_form


class CSSContainer:
    def __init__(self, css_styles):
        for key, value in css_styles.items():
            setattr(self, key, value)

    def get_field_class(self, field):
        widget_cls = field.field.widget.__class__.__name__
        key = camel_to_snake(widget_cls)
        css_classes = getattr(self, key, "")
        return css_classes


class FormifyHelper:
    """
    Developers can override these settings in their own FormifyHelper class
    and access them in template via formify_helper.xxx
    """

    ################################################################################
    # field wrapper
    # field wrapper is a wrapper for label, field and error messages
    ################################################################################
    field_wrapper_class = "field-wrapper mb-3"
    # this is the component used to render the label, field input and error messages
    field_wrapper_component = "formify.tw.field_wrapper"

    ################################################################################
    # field
    ################################################################################
    field_container_class = ""

    # if form validation fail, use this to replace border css class for some inputs
    error_border = "border-red-300"

    common_style = (
        "bg-white focus:outline-none border border-gray-300 rounded-lg py-2 px-4 block w-full "
        "appearance-none leading-normal text-gray-700"
    )

    default_styles = {
        "text_input": common_style,
        "number_input": common_style,
        "email_input": common_style,
        "url_input": common_style,
        "password_input": common_style,
        "textarea": common_style,
        "date_input": common_style,
        "time_input": common_style,
        "date_time_input": common_style,
        "clearable_file_input": "w-full overflow-clip rounded-lg border border-gray-300 bg-gray-50/50 text-gray-600 file:mr-4 file:cursor-pointer file:border-none file:bg-gray-50 file:px-4 file:py-2 file:font-medium file:text-gray-900 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-black disabled:cursor-not-allowed disabled:opacity-75 dark:border-gray-700 dark:bg-gray-900/50 dark:text-gray-300 dark:file:bg-gray-900 dark:file:text-white dark:focus-visible:outline-white",
        "radio_select_option_label": "inline-flex items-center gap-2 text-gray-700",
        "checkbox_label": "inline-flex items-center gap-2 text-gray-700",
    }

    default_error_styles = {
        # border-red-300
        "clearable_file_input": "w-full overflow-clip rounded-lg border border-red-300 bg-gray-50/50 text-gray-600 file:mr-4 file:cursor-pointer file:border-none file:bg-gray-50 file:px-4 file:py-2 file:font-medium file:text-gray-900 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-black disabled:cursor-not-allowed disabled:opacity-75 dark:border-gray-700 dark:bg-gray-900/50 dark:text-gray-300 dark:file:bg-gray-900 dark:file:text-white dark:focus-visible:outline-white",
    }

    css_container = None

    error_css_container = None

    ################################################################################
    # label
    ################################################################################
    form_show_labels = True
    label_component = "formify.tw.field_label"
    label_container_class = ""
    label_class = "label-class block text-gray-900 mb-2"

    ################################################################################
    # other
    ################################################################################
    form_show_errors = True
    field_error_help_text_component = "formify.tw.field_error_help_text"
    field_help_text_component = "formify.tw.field_help_text"
    field_error_component = "formify.tw.field_error"

    form = None

    formset = None

    layout = None

    def __init__(self):
        self.prepare_css_container()

    def prepare_css_container(self):
        self.css_container = CSSContainer(self.default_styles)
        self.error_css_container = CSSContainer(self.default_error_styles)

    def get_context_data(self, context_data) -> Context:
        if isinstance(context_data, Context):
            context = context_data
        else:
            context = Context(context_data)

        context["formify_helper"] = self
        context["form"] = self.form
        context["formset"] = self.formset

        return context

    def smart_render(self, template, context):
        # if template is django.template.base.Template, make sure context is a Context object
        # if not, make sure context is pure dict
        if isinstance(template, Template):
            # make sure the context is Context
            if isinstance(context, Context):
                context_for_render = context
            else:
                context_for_render = Context(context)
            return template.render(context_for_render)
        else:
            # make sure the context is dict
            if isinstance(context, Context):
                # convert to dict
                context_for_render = context.flatten()
            else:
                context_for_render = context

            return template.render(context_for_render)

    def build_default_layout(self):
        return Layout(*[Field(field_name) for field_name in self.form.fields.keys()])

    ################################################################################
    # Rendering Methods
    ################################################################################

    def render_form_tag(self, context, content, **kwargs):
        context["form_content"] = content
        attrs = {
            "class": kwargs.pop("css_class", ""),
            "method": kwargs.pop("method", "POST").upper(),
        }
        action = kwargs.pop("action", "")
        if action:
            attrs["action"] = action
        for key, value in kwargs.items():
            attrs[key] = value
        context["attrs"] = attrs

        template = get_template("formify/tailwind/form_tag.html")
        return self.smart_render(template, context)

    def render_formset(self, context):
        """
        uni_formset.html
        """
        # render formset management form fields
        management_form = self.formset.management_form
        management_form_helper = init_formify_helper_for_form(management_form)
        with context.push():
            update_context = management_form_helper.get_context_data(context)
            management_form_html = management_form_helper.render_form(update_context)

        # render formset errors
        formset_errors = self.render_formset_errors(context)

        forms_html = ""
        for form in self.formset:
            form_helper = init_formify_helper_for_form(form)
            with context.push():
                update_context = form_helper.get_context_data(context)
                forms_html += form_helper.render_form(update_context)

        return SafeString(management_form_html + formset_errors + forms_html)

    def render_form(self, context):
        """
        uni_form.html
        """
        return SafeString(
            self.render_form_errors(context) + self.render_form_fields(context)
        )

    def render_field(self, context, field, **kwargs):
        """
        This method is to render specific field
        """
        field_formify_helper = copy.copy(self)

        # assign extra kwargs to formify_helper if needed
        for key, value in kwargs.items():
            setattr(field_formify_helper, key, value)

        with context.push():
            context["field"] = field

            if field.is_hidden:
                return SafeString(field.as_widget())
            else:
                dispatch_method_callable = field_formify_helper.field_dispatch(field)
                update_context = field_formify_helper.get_context_data(context)
                return SafeString(dispatch_method_callable(update_context))

    def render_submit(self, context, **kwargs):
        """
        It would be called from the render_submit tag

        Here we use Submit component to render the submit button, you can also override this method and
        use Django's get_template and render methods to render the submit button
        """
        css_class = kwargs.pop("css_class", None)
        text = kwargs.pop("text", None)
        submit_component = Submit(text=text, css_class=css_class, **kwargs)
        with context.push():
            update_context = self.get_context_data(context)
            return submit_component.render_from_parent_context(update_context)

    def render_formset_errors(self, context):
        template = get_template("formify/tailwind/errors_formset.html")
        with context.push():
            update_context = self.get_context_data(context)
            return self.smart_render(template, update_context)

    def render_form_errors(self, context):
        template = get_template("formify/tailwind/errors.html")
        with context.push():
            update_context = self.get_context_data(context)
            return self.smart_render(template, update_context)

    ################################################################################

    def field_dispatch(self, field):
        """
        It will check if there is a method to render the field, if not, it will fall back to the "fallback" method

        For TextInput widget, the method is text_input
        """
        widget_cls = field.field.widget.__class__.__name__
        method_name = camel_to_snake(widget_cls)

        # check if method exists for self instance and callable
        if hasattr(self, method_name) and callable(getattr(self, method_name)):
            return getattr(self, method_name)
        else:
            return self.fallback

    def render_form_fields(self, context):
        if not self.layout:
            self.layout = self.build_default_layout()
        with context.push():
            update_context = self.get_context_data(context)
            # render_from_parent_context is a method from the Component class
            return self.layout.render_from_parent_context(update_context)

    def render_as_tailwind_field(self, context):
        """
        Logic from CrispyTailwindFieldNode.render method
        """
        field = context["field"]
        widget = field.field.widget

        attrs = context.get("attrs", {})
        css_class = widget.attrs.get("class", "")
        if "class" not in attrs.keys():
            # if class is not set, then add additional css classes

            # add default input class
            css = " " + self.css_container.get_field_class(field)
            css_class += css

            if field.errors:
                error_css = self.error_css_container.get_field_class(field)
                if error_css:
                    css_class = error_css
                else:
                    # change border css class of the widget
                    css_class = re.sub(r"border-\S+", self.error_border, css_class)

        widget.attrs["class"] = css_class

        # TODO
        # auto add required attribute
        if field.field.required and "required" not in widget.attrs:
            if field.field.widget.__class__.__name__ != "RadioSelect":
                widget.attrs["required"] = "required"

        # TODO
        for attribute_name, attributes in attrs.items():
            if attribute_name in widget.attrs:
                # multiple attribtes are in a single string, e.g.
                # "form-control is-invalid"
                for attr in attributes.split():
                    if attr not in widget.attrs[attribute_name].split():
                        widget.attrs[attribute_name] += " " + attr
            else:
                widget.attrs[attribute_name] = attributes

        return str(field)

    def common_field(self, context):
        field_html = self.render_as_tailwind_field(context)
        context["field_html"] = field_html
        field_template = get_template("formify/tailwind/common_field.html")
        return self.smart_render(field_template, context)

    def fallback(self, context):
        return self.common_field(context)

    ################################################################################
    # Widget Methods
    ################################################################################

    def text_input(self, context):
        return self.common_field(context)

    def number_input(self, context):
        return self.common_field(context)

    def email_input(self, context):
        return self.common_field(context)

    def password_input(self, context):
        return self.common_field(context)

    def checkbox_input(self, context):
        """
        Aligning Checkboxes Horizontally
        """
        field_html = self.render_as_tailwind_field(context)
        context["field_html"] = field_html
        field_template = get_template("formify/tailwind/checkbox_input.html")
        return self.smart_render(field_template, context)

    def date_input(self, context):
        # TODO
        # type="date"
        return self.common_field(context)

    def time_input(self, context):
        # TODO
        # type="time"
        return self.common_field(context)

    def date_time_input(self, context):
        # TODO
        # type="datetime-local"
        return self.common_field(context)

    def select(self, context):
        field_template = get_template("formify/tailwind/select.html")
        return self.smart_render(field_template, context)

    def select_multiple(self, context):
        return self.select(context)

    def radio_select(self, context):
        field_template = get_template("formify/tailwind/radio_select.html")
        return self.smart_render(field_template, context)

    def checkbox_select_multiple(self, context):
        field_template = get_template("formify/tailwind/checkbox_select_multiple.html")
        return self.smart_render(field_template, context)

    def clearable_file_input(self, context):
        return self.common_field(context)

    def url_input(self, context):
        return self.common_field(context)

    def textarea(self, context):
        return self.common_field(context)
