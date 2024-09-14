import pytest
from django.forms.formsets import formset_factory
from django.template import Context, Template

from tests.testapp.forms import SampleForm

from .utils import assert_select

pytestmark = pytest.mark.django_db


class TestBasic:
    def test_form_tag(self):
        template = Template(
            """
            {% load formify %}
            {% with url='/' %}
                {% form_tag form action=url %}
                    {% render_form form %}
                {% endform_tag %}
            {% endwith %}
            """
        )
        c = Context({"form": SampleForm()})
        html = template.render(c)

        assert_select(html, "form", 1)
        assert_select(html, "form[method='POST']", 1)
        assert_select(html, "form[action='/']", 1)

    def test_form_tag_extra_kwargs(self):
        template = Template(
            """
            {% load formify %}

            {% with url='/' %}
                {% form_tag form action=url data_test='test' novalidate=True %}
                    {% render_form form %}
                {% endform_tag %}
            {% endwith %}
            """
        )
        c = Context({"form": SampleForm()})
        html = template.render(c)

        assert_select(html, "form", 1)
        assert_select(html, "form[method='POST']", 1)
        assert_select(html, "form[action='/']", 1)
        assert_select(html, "form[data-test='test']", 1)
        assert_select(html, "form[novalidate]", 1)

    def test_form_tag_with_include(self):
        template = Template(
            """
            {% load formify %}

            {% form_tag form %}
                {% include 'test.html' %}
            {% endform_tag %}
            """
        )
        c = Context({"form": SampleForm()})
        html = template.render(c)
        assert "Hello" in html

    def test_render_field(self):
        template = Template(
            """
            {% load formify %}
            {% for field in form %}
                {% render_field field %}
            {% endfor %}
            """
        )
        html = template.render(Context({"form": SampleForm()}))
        assert_select(html, "input", 8)

    def test_render_form(self):
        template = Template(
            """
            {% load formify %}
            {% render_form form %}
            """
        )
        c = Context({"form": SampleForm()})
        html = template.render(c)

        assert "id_is_company" in html
        assert_select(html, "label", 7)

    def test_render_formset(self):
        template = Template(
            """
            {% load formify %}
            {% render_form testFormset %}
            """
        )

        SampleFormset = formset_factory(SampleForm, extra=4)
        testFormset = SampleFormset()

        c = Context({"testFormset": testFormset})
        html = template.render(c)

        assert_select(html, "form", 0)

        # Check formset management form
        assert "form-TOTAL_FORMS" in html
        assert "form-INITIAL_FORMS" in html
        assert "form-MAX_NUM_FORMS" in html

    def test_form_without_non_field_errors(self):
        template = Template(
            """
            {% load formify %}
            {% render_form form %}
            """
        )
        form = SampleForm({"password1": "god", "password2": "god"})
        form.is_valid()

        c = Context({"form": form})
        html = template.render(c)
        # no non-field errors
        assert_select(html, ".form-non-field-errors", 0)

    def test_form_with_non_field_errors(self):
        template = Template(
            """
            {% load formify %}
            {% render_form form %}
            """
        )
        form = SampleForm({"password1": "god", "password2": "wargame"})
        form.is_valid()

        c = Context({"form": form})
        html = template.render(c)
        assert_select(html, ".form-non-field-errors")

    def test_form_errors_with_non_field_errors(self):
        template = Template(
            """
            {% load formify %}
            {% render_form_errors form %}
            """
        )
        form = SampleForm({"password1": "god", "password2": "wargame"})
        form.is_valid()

        c = Context({"form": form})
        html = template.render(c)
        assert_select(html, ".form-non-field-errors")

    def test_formset_without_non_form_errors(self):
        template = Template(
            """
            {% load formify %}
            {% render_form formset %}
            """
        )

        SampleFormset = formset_factory(SampleForm, max_num=1, validate_max=True)
        formset = SampleFormset()
        formset.is_valid()

        c = Context({"formset": formset})
        html = template.render(c)
        assert_select(html, ".formset-non-form-errors", 0)

    def test_formset_with_non_form_errors(self):
        template = Template(
            """
            {% load formify %}
            {% render_form formset %}
            """
        )

        SampleFormset = formset_factory(SampleForm, max_num=1, validate_max=True)
        formset = SampleFormset(
            {
                "form-TOTAL_FORMS": "2",
                "form-INITIAL_FORMS": "0",
                "form-MAX_NUM_FORMS": "",
                "form-0-password1": "god",
                "form-0-password2": "wargame",
            }
        )
        formset.is_valid()

        c = Context({"formset": formset})
        html = template.render(c)

        assert "Please submit at most 1 form" in html
        assert_select(html, ".formset-non-form-errors")

    def test_formset_errors_with_non_form_errors(self):
        template = Template(
            """
            {% load formify %}
            {% render_form formset %}
            """
        )

        SampleFormset = formset_factory(SampleForm, max_num=1, validate_max=True)
        formset = SampleFormset(
            {
                "form-TOTAL_FORMS": "2",
                "form-INITIAL_FORMS": "0",
                "form-MAX_NUM_FORMS": "",
                "form-0-password1": "god",
                "form-0-password2": "wargame",
            }
        )
        formset.is_valid()

        c = Context({"formset": formset})
        html = template.render(c)

        assert "Please submit at most 1 form" in html
        assert_select(html, ".formset-non-form-errors")

    def test_bound_field(self):
        template = Template(
            """
            {% load formify %}
            {% render_field field %}
            """
        )

        form = SampleForm({"password1": "god", "password2": "god"})
        form.is_valid()

        c = Context({"field": form["password1"]})

        html = template.render(c)
        assert "id_password1" in html
        assert "id_password2" not in html

    def test_render_submit(self):
        template = Template(
            """
            {% load formify %}
            {% render_submit form text='Hello' css_class="btn btn-primary" name='action_primary' value='action_primary' %}
            """
        )
        form = SampleForm()
        c = Context({"form": form})
        html = template.render(c)

        assert_select(html, "button.btn-primary")
        assert_select(html, "button.btn")
        assert_select(html, 'button[type="submit"][value="action_primary"]')
        assert_select(html, "button", text="Hello")

    def test_render_submit_with_none_form(self):
        # should work when form is not defined in context
        template = Template(
            """
            {% load formify %}
            {% render_submit form text='Hello' css_class="btn btn-primary" name='action_primary' value='action_primary' %}
            """
        )
        c = Context({})
        html = template.render(c)

        assert_select(html, "button.btn-primary")
        assert_select(html, "button.btn")
        assert_select(html, 'button[type="submit"][value="action_primary"]')
        assert_select(html, "button", text="Hello")

        # do not pass form
        template = Template(
            """
            {% load formify %}
            {% render_submit text='Hello' css_class="btn btn-primary" name='action_primary' value='action_primary' %}
            """
        )
        c = Context({})
        html = template.render(c)

        assert_select(html, "button.btn-primary")
        assert_select(html, "button.btn")
        assert_select(html, 'button[type="submit"][value="action_primary"]')
        assert_select(html, "button", text="Hello")
