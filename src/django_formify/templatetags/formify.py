from django import template
from django.forms.formsets import BaseFormSet
from django.template.context import Context
from django.utils.safestring import mark_safe

from django_formify.utils import flatatt as utils_flatatt
from django_formify.utils import (
    init_formify_helper_for_form,
    init_formify_helper_for_formset,
)

register = template.Library()


@register.simple_tag(takes_context=True)
def render_form(context, form_or_formset):
    if isinstance(form_or_formset, BaseFormSet):
        # formset
        formset = form_or_formset
        formify_helper = init_formify_helper_for_formset(formset)
        return formify_helper.render_formset(
            Context(context.flatten()), create_new_context=True
        )
    else:
        # form
        form = form_or_formset
        formify_helper = init_formify_helper_for_form(form)
        return formify_helper.render_form(
            Context(context.flatten()), create_new_context=True
        )


@register.simple_tag(takes_context=True)
def render_form_errors(context, form_or_formset):
    if isinstance(form_or_formset, BaseFormSet):
        # formset
        formset = form_or_formset
        formify_helper = init_formify_helper_for_formset(formset)
        return formify_helper.render_formset_errors(
            Context(context.flatten()), create_new_context=True
        )
    else:
        # form
        form = form_or_formset
        formify_helper = init_formify_helper_for_form(form)
        return formify_helper.render_form_errors(
            Context(context.flatten()), create_new_context=True
        )


@register.simple_tag(takes_context=True)
def render_field(context, field, **kwargs):
    form = field.form
    formify_helper = init_formify_helper_for_form(form)
    return formify_helper.render_field(
        field=field,
        context=Context(context.flatten()),
        create_new_context=True,
        **kwargs
    )


@register.simple_tag(takes_context=True)
def render_submit(context, form=None, **kwargs):
    formify_helper = init_formify_helper_for_form(form)
    return formify_helper.render_submit(Context(context.flatten()), **kwargs)


@register.filter
def flatatt(attrs):
    return mark_safe(utils_flatatt(attrs))


@register.filter
def build_attrs(field):
    """
    Copied from crispy form, maybe removed in the future.

    Build HTML attributes for a form field, also checking for a
    ``widget.allow_multiple_selected`` attribute  and adding ``multiple`` to the
    attributes if it is set to ``True``.
    """
    attrs = field.field.widget.attrs
    attrs.setdefault("id", field.auto_id)

    field_built_widget_attrs = field.build_widget_attrs(attrs)
    attrs.update(field_built_widget_attrs)

    # Some custom widgets (e.g. Select2) may add additional attributes to the
    # widget attrs dict. We need to add those to the attrs dict as well calling
    # the widget's build_attrs method.

    built_widget_attrs = field.field.widget.build_attrs(attrs)
    attrs.update(built_widget_attrs)

    if hasattr(field.field.widget, "allow_multiple_selected"):
        attrs["multiple"] = attrs.get(
            "multiple", field.field.widget.allow_multiple_selected
        )
    return mark_safe(flatatt(attrs))


@register.filter
def optgroups(field):
    """
    Copied from crispy form, maybe removed in the future.

    A template filter to help rendering of fields with optgroups.

    Returns:
        A tuple of label, option, index

        label: Group label for grouped optgroups (`None` if inputs are not
               grouped).

        option: A dict containing information to render the option::

            {
                "name": "checkbox_select_multiple",
                "value": 1,
                "label": 1,
                "selected": False,
                "index": "0",
                "attrs": {"id": "id_checkbox_select_multiple_0"},
                "type": "checkbox",
                "template_name": "django/forms/widgets/checkbox_option.html",
                "wrap_label": True,
            }

        index: Group index

    """
    id_ = field.field.widget.attrs.get("id") or field.auto_id
    attrs = {"id": id_} if id_ else {}
    attrs = field.build_widget_attrs(attrs)
    values = field.field.widget.format_value(field.value())
    return field.field.widget.optgroups(field.html_name, values, attrs)
