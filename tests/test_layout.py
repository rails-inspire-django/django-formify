from django.template import Context, Template

from django_formify.tailwind.formify_helper import FormifyHelper
from django_formify.tailwind.layout import (
    HTML,
    Button,
    Div,
    Field,
    Fieldset,
    Layout,
    Reset,
    Submit,
)
from django_formify.utils import init_formify_helper_for_form
from tests.testapp.forms import SampleForm

from .utils import assert_select


class TestBuiltinComponents:
    def test_html(self):
        html = HTML("{% if saved %}Data saved{% endif %}").render_from_parent_context(
            {"saved": True}
        )
        assert "Data saved" in html

        # step_field and step0 not defined
        html = HTML(
            '<input type="hidden" name="{{ step_field }}" value="{{ step0 }}" />'
        ).render_from_parent_context()
        assert_select(html, "input")

    def test_layout(self):
        html = Layout(
            Div(
                HTML("Hello {{ value_1 }}"),
                HTML("Hello {{ value_2 }}"),
                dom_id="main",
            ),
        ).render_from_parent_context({"value_1": "world"})

        assert_select(html, "div#main")
        assert "Hello world" in html

    def test_div(self):
        html = Div(
            Div(
                HTML("Hello {{ value_1 }}"),
                HTML("Hello {{ value_2 }}"),
                css_class="wrapper",
            ),
            dom_id="main",
        ).render_from_parent_context({"value_1": "world"})

        assert_select(html, "div#main")
        assert_select(html, "div.wrapper")
        assert "Hello world" in html

    def test_button(self):
        html = Div(
            Div(
                Button("{{ value_1 }}", css_class="btn btn-primary"),
            ),
            dom_id="main",
        ).render_from_parent_context({"value_1": "world"})

        assert_select(html, "button.btn")
        assert_select(html, "button[type=button]")
        assert "world" in html

        # test custom attributes
        html = Button(
            "Hello",
            css_class="btn btn-primary",
            name="action_remove",
            value="action_remove",
            data_turbo_confirm="Are you sure?",
        ).render_from_parent_context()

        assert_select(html, "button.btn")
        assert_select(html, "button[type=button]")
        assert_select(html, "button[name=action_remove]")
        assert_select(html, "button[value=action_remove]")
        assert_select(html, "button[data-turbo-confirm]")

    def test_submit(self):
        html = Div(
            Div(
                Submit("{{ value_1 }}", css_class="btn btn-primary"),
            ),
            dom_id="main",
        ).render_from_parent_context({"value_1": "world"})

        assert_select(html, "button.btn")
        assert_select(html, "button[type=submit]")
        assert "world" in html

        # test custom attributes
        html = Submit(
            "Hello",
            css_class="btn btn-primary",
            name="action_remove",
            value="action_remove",
            data_turbo_confirm="Are you sure?",
        ).render_from_parent_context()

        assert_select(html, "button.btn")
        assert_select(html, "button[type=submit]")
        assert_select(html, "button[name=action_remove]")
        assert_select(html, "button[value=action_remove]")
        assert_select(html, "button[data-turbo-confirm]")

    def test_reset(self):
        html = Div(
            Div(
                Reset("{{ value_1 }}", css_class="btn btn-primary"),
            ),
            dom_id="main",
        ).render_from_parent_context({"value_1": "world"})

        assert_select(html, "button.btn")
        assert_select(html, "button[type=reset]")
        assert "world" in html

        # test custom attributes
        html = Reset(
            "Hello",
            css_class="btn btn-primary",
            name="action_remove",
            value="action_remove",
            data_turbo_confirm="Are you sure?",
        ).render_from_parent_context()

        assert_select(html, "button.btn")
        assert_select(html, "button[type=reset]")
        assert_select(html, "button[name=action_remove]")
        assert_select(html, "button[value=action_remove]")
        assert_select(html, "button[data-turbo-confirm]")

    def test_field(self):
        form = SampleForm()
        formify_helper = init_formify_helper_for_form(form)

        html = Div(
            Field("email"),
            Submit("Submit"),
            dom_id="main",
        ).render_from_parent_context({"formify_helper": formify_helper})

        assert_select(html, "div#main")
        assert_select(html, "button[type=submit]")
        assert_select(html, "input[name=email]", 1)

    def test_fieldset(self):
        form = SampleForm()
        formify_helper = init_formify_helper_for_form(form)

        html = Div(
            Fieldset(
                "Basic Info",
                Field("first_name"),
                Field("last_name"),
                Field("email"),
                css_class="fieldset",
            ),
            Submit("Submit"),
            dom_id="main",
        ).render_from_parent_context({"formify_helper": formify_helper})

        assert_select(html, "div#main")
        assert_select(html, "fieldset.fieldset")
        assert "Basic Info" in html

        assert_select(html, "input", 3)
        assert_select(html, "button[type=submit]")

    def test_form_helper(self):
        template = Template(
            """
            {% load formify %}
            {% render_form test_form %}
        """
        )

        # now we render it, with errors
        form = SampleForm({"password1": "wargame", "password2": "god"})
        form.formify_helper = FormifyHelper()
        form.formify_helper.layout = Layout(
            Fieldset(
                "Basic Info",
                Field("first_name"),
                Field("last_name"),
                Field("password1"),
                Field("password2"),
                css_class="fieldset",
            ),
        )

        form.is_valid()
        c = Context({"test_form": form})
        html = template.render(c)

        assert_select(html, "input", 4)
        assert "Basic Info" in html
        assert_select(html, ".form-non-field-errors")
