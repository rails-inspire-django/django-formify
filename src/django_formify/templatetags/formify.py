from django import template
from django.forms.formsets import BaseFormSet
from django.template.base import Node, NodeList
from django.template.context import Context
from django.template.exceptions import TemplateSyntaxError
from django.template.library import parse_bits
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
        return formify_helper.render_formset(context)
    else:
        # form
        form = form_or_formset
        formify_helper = init_formify_helper_for_form(form)
        return formify_helper.render_form(context)


@register.simple_tag(takes_context=True)
def render_form_errors(context, form_or_formset):
    if isinstance(form_or_formset, BaseFormSet):
        # formset
        formset = form_or_formset
        formify_helper = init_formify_helper_for_formset(formset)
        return formify_helper.render_formset_errors(context)
    else:
        # form
        form = form_or_formset
        formify_helper = init_formify_helper_for_form(form)
        return formify_helper.render_form_errors(context)


@register.simple_tag(takes_context=True)
def render_field(context, field, **kwargs):
    form = field.form
    formify_helper = init_formify_helper_for_form(form)
    return formify_helper.render_field(
        context=context,
        field=field,
        **kwargs,
    )


@register.simple_tag(takes_context=True)
def render_submit(context, form=None, **kwargs):
    formify_helper = init_formify_helper_for_form(form)
    return formify_helper.render_submit(context, **kwargs)


@register.filter
def flatatt(attrs):
    return mark_safe(utils_flatatt(attrs))


class FormTagNode(Node):
    def __init__(
        self,
        context_args,
        context_kwargs,
        nodelist: NodeList,
    ):
        self.context_args = context_args or []
        self.context_kwargs = context_kwargs or {}
        self.nodelist = nodelist

    def __repr__(self):
        return "<FormTagNode Contents: %r>" % (
            getattr(
                self, "nodelist", None
            ),  # 'nodelist' attribute only assigned later.
        )

    def render(self, context: Context):
        resolved_component_args = [
            safe_resolve(arg, context) for arg in self.context_args
        ]
        resolved_component_kwargs = {
            key: safe_resolve(kwarg, context)
            for key, kwarg in self.context_kwargs.items()
        }
        form = resolved_component_args[0]
        formify_helper = init_formify_helper_for_form(form)
        content = self.nodelist.render(context)
        return formify_helper.render_form_tag(
            context=context, content=content, **resolved_component_kwargs
        )


@register.tag(name="form_tag")
def do_form_tag(parser, token):
    bits = token.split_contents()
    tag_name = "form_tag"
    tag_args, tag_kwargs = parse_bits(
        parser=parser,
        bits=bits,
        params=[],
        takes_context=False,
        name=tag_name,
        varargs=True,
        varkw=[],
        defaults=None,
        kwonly=[],
        kwonly_defaults=None,
    )

    if tag_name != tag_args[0].token:
        raise RuntimeError(
            f"Internal error: Expected tag_name to be {tag_name}, but it was {tag_args[0].token}"
        )

    if len(tag_args) != 2:
        raise TemplateSyntaxError(
            f"'{tag_name}' tag should have form as the first argument, other arguments should be keyword arguments."
        )

    context_args = tag_args[1:]
    context_kwargs = tag_kwargs

    nodelist: NodeList = parser.parse(parse_until=["endform_tag"])
    parser.delete_first_token()

    component_node = FormTagNode(
        context_args=context_args,
        context_kwargs=context_kwargs,
        nodelist=nodelist,
    )

    return component_node


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


def safe_resolve(context_item, context):
    """Resolve FilterExpressions and Variables in context if possible.  Return other items unchanged."""

    return (
        context_item.resolve(context)
        if hasattr(context_item, "resolve")
        else context_item
    )
