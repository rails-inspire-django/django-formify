import pytest
from django.template import Context, Template

from django_formify.tailwind.formify_helper import FormifyHelper
from tests.testapp.forms import AllFieldsForm, SampleForm

from .utils import assert_select

pytestmark = pytest.mark.django_db


def render(template, context):
    return Template(template).render(Context(context))


class TestDefaultFormifyHelper:
    def test_render_all_supported_fields(self, mocker):
        mock_text_input = mocker.spy(FormifyHelper, "text_input")

        template = Template(
            """
            {% load formify %}
            {% render_field form.char_field %}
            """
        )
        html = template.render(Context({"form": AllFieldsForm()}))

        mock_text_input.assert_called_once()
        assert_select(html, ".form-group", 1)

    def test_render_email_field(self, mocker):
        mock_email_input = mocker.spy(FormifyHelper, "email_input")

        template = Template(
            """
            {% load formify %}
            {% render_field form.email_field %}
            """
        )
        html = template.render(Context({"form": AllFieldsForm()}))

        mock_email_input.assert_called_once()
        assert_select(html, ".form-group", 1)

    def test_render_integer_field(self, mocker):
        mock_number_input = mocker.spy(FormifyHelper, "number_input")

        template = Template(
            """
            {% load formify %}
            {% render_field form.integer_field %}
            """
        )
        html = template.render(Context({"form": AllFieldsForm()}))

        mock_number_input.assert_called_once()
        assert_select(html, ".form-group", 1)

    def test_render_float_field(self, mocker):
        mock_number_input = mocker.spy(FormifyHelper, "number_input")

        template = Template(
            """
            {% load formify %}
            {% render_field form.float_field %}
            """
        )
        html = template.render(Context({"form": AllFieldsForm()}))

        mock_number_input.assert_called_once()
        assert_select(html, ".form-group", 1)

    def test_render_boolean_field(self, mocker):
        mock_checkbox_input = mocker.spy(FormifyHelper, "checkbox_input")

        template = Template(
            """
            {% load formify %}
            {% render_field form.boolean_field %}
            """
        )
        html = template.render(Context({"form": AllFieldsForm()}))

        mock_checkbox_input.assert_called_once()
        assert_select(html, ".form-group", 1)

    def test_render_date_field(self, mocker):
        mock_date_input = mocker.spy(FormifyHelper, "date_input")

        template = Template(
            """
            {% load formify %}
            {% render_field form.date_field %}
            """
        )
        html = template.render(Context({"form": AllFieldsForm()}))

        mock_date_input.assert_called_once()
        assert_select(html, ".form-group", 1)

    def test_render_time_field(self, mocker):
        mock_time_input = mocker.spy(FormifyHelper, "time_input")

        template = Template(
            """
            {% load formify %}
            {% render_field form.time_field %}
            """
        )
        html = template.render(Context({"form": AllFieldsForm()}))

        mock_time_input.assert_called_once()
        assert_select(html, ".form-group", 1)

    def test_render_datetime_field(self, mocker):
        mock_date_time_input = mocker.spy(FormifyHelper, "date_time_input")

        template = Template(
            """
            {% load formify %}
            {% render_field form.datetime_field %}
            """
        )
        html = template.render(Context({"form": AllFieldsForm()}))

        mock_date_time_input.assert_called_once()
        assert_select(html, ".form-group", 1)

    def test_render_choice_field(self, mocker):
        mock_select = mocker.spy(FormifyHelper, "select")

        template = Template(
            """
            {% load formify %}
            {% render_field form.choice_field %}
            """
        )
        html = template.render(Context({"form": AllFieldsForm()}))

        mock_select.assert_called_once()
        assert_select(html, ".form-group", 1)

    def test_render_choice_radio_field(self, mocker):
        mock_radio_select = mocker.spy(FormifyHelper, "radio_select")

        template = Template(
            """
            {% load formify %}
            {% render_field form.choice_radio_field %}
            """
        )
        html = template.render(Context({"form": AllFieldsForm()}))

        mock_radio_select.assert_called_once()
        assert_select(html, ".form-group", 1)

    def test_render_select_multiple(self, mocker):
        mock_select_multiple = mocker.spy(FormifyHelper, "select_multiple")

        template = Template(
            """
            {% load formify %}
            {% render_field form.multiple_choice_field %}
            """
        )
        html = template.render(Context({"form": AllFieldsForm()}))

        mock_select_multiple.assert_called_once()
        assert_select(html, ".form-group", 1)

    def test_render_checkbox_select_multiple(self, mocker):
        mock_checkbox_select_multiple = mocker.spy(
            FormifyHelper, "checkbox_select_multiple"
        )

        template = Template(
            """
            {% load formify %}
            {% render_field form.favorite_colors %}
            """
        )
        html = template.render(Context({"form": AllFieldsForm()}))

        mock_checkbox_select_multiple.assert_called_once()
        assert_select(html, ".form-group", 1)

    def test_render_file_field(self, mocker):
        mock_clearable_file_input = mocker.spy(FormifyHelper, "clearable_file_input")

        template = Template(
            """
            {% load formify %}
            {% render_field form.file_field %}
            """
        )
        html = template.render(Context({"form": AllFieldsForm()}))

        mock_clearable_file_input.assert_called_once()
        assert_select(html, ".form-group", 1)

    def test_render_image_field(self, mocker):
        mock_clearable_file_input = mocker.spy(FormifyHelper, "clearable_file_input")

        template = Template(
            """
            {% load formify %}
            {% render_field form.image_field %}
            """
        )
        html = template.render(Context({"form": AllFieldsForm()}))

        mock_clearable_file_input.assert_called_once()
        assert_select(html, ".form-group", 1)

    def test_render_url_field(self, mocker):
        mock_url_input = mocker.spy(FormifyHelper, "url_input")

        template = Template(
            """
            {% load formify %}
            {% render_field form.url_field %}
            """
        )
        html = template.render(Context({"form": AllFieldsForm()}))

        mock_url_input.assert_called_once()
        assert_select(html, ".form-group", 1)

    def test_render_regex_field(self, mocker):
        mock_text_input = mocker.spy(FormifyHelper, "text_input")

        template = Template(
            """
            {% load formify %}
            {% render_field form.regex_field %}
            """
        )
        html = template.render(Context({"form": AllFieldsForm()}))

        mock_text_input.assert_called_once()
        assert_select(html, ".form-group", 1)

    def test_render_hidden_field(self):
        template = Template(
            """
            {% load formify %}
            {% render_field form.hidden_field %}
            """
        )
        html = template.render(Context({"form": AllFieldsForm()}))
        assert_select(html, 'input[type="hidden"]', 1)

    def test_render_textarea_field(self, mocker):
        mock_text_input = mocker.spy(FormifyHelper, "textarea")

        template = Template(
            """
            {% load formify %}
            {% render_field form.textarea_field %}
            """
        )
        html = template.render(Context({"form": AllFieldsForm()}))

        mock_text_input.assert_called_once()
        assert_select(html, ".form-group", 1)

    def test_render_password_input_field(self, mocker):
        mock_text_input = mocker.spy(FormifyHelper, "password_input")

        template = Template(
            """
            {% load formify %}
            {% render_field form.password_input_field %}
            """
        )
        html = template.render(Context({"form": AllFieldsForm()}))

        mock_text_input.assert_called_once()
        assert_select(html, ".form-group", 1)


class TestFormFormifyHelper:
    def test_custom_formify_helper(self):
        helper = FormifyHelper()
        helper.form_show_errors = False
        helper.field_wrapper_class = "another-form-group"

        template = Template(
            """
            {% load formify %}
            {% render_form testForm %}
        """
        )

        # now we render it, with errors
        form = SampleForm({"password1": "wargame", "password2": "god"})
        form.formify_helper = helper
        form.is_valid()
        c = Context({"testForm": form})
        html = template.render(c)

        assert_select(html, ".form-group", 0)
        assert_select(html, ".another-form-group")
        assert_select(html, ".form-non-field-errors", 0)

    def test_override_in_field(self):
        """
        Override formify_helper value on field level

        """
        helper = FormifyHelper()

        template = Template(
            """
            {% load formify %}
            {% render_field testForm.password1 form_show_labels=False %}
            {% render_field testForm.password2 %}
        """
        )

        # now we render it, with errors
        form = SampleForm({"password1": "wargame", "password2": "god"})
        form.formify_helper = helper
        form.is_valid()
        c = Context({"testForm": form})
        html = template.render(c)

        assert_select(html, ".form-group")
        assert_select(html, "label", 1)
