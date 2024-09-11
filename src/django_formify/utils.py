import re

from django.forms.utils import flatatt as _flatatt
from django.utils.module_loading import import_string

from django_formify.app_settings import app_settings


def init_formify_helper_for_form(form):
    """
    If form has formify_helper attribute, return it
    If not, return the global helper
    """
    if hasattr(form, "formify_helper"):
        form.formify_helper.form = form
        return form.formify_helper
    else:
        helper_cls = import_string(app_settings.FORMIFY_HELPER)
        helper = helper_cls()
        if form:
            helper.form = form
            form.formify_helper = helper
        return helper


def init_formify_helper_for_formset(formset):
    helper_cls = import_string(app_settings.FORMIFY_HELPER)
    helper = helper_cls()
    helper.formset = formset
    return helper


def camel_to_snake(column_name):
    """
    converts a string that is camelCase into snake_case
    Example:
        print camel_to_snake("javaLovesCamelCase")
        > java_loves_camel_case
    See Also:
        http://stackoverflow.com/questions/1175208/elegant-python-function-to-convert-camelcase-to-camel-case
    """
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", column_name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


def flatatt(attrs):
    """
    Convert a dictionary of attributes to a single string.

    Passed attributes are redirected to `django.forms.utils.flatatt()`
    with replaced "_" (underscores) by "-" (dashes) in their names.
    """
    return _flatatt({k.replace("_", "-"): v for k, v in attrs.items()})
