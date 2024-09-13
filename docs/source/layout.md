# Layout

## Usage

The layout is to help control the form layout in Python code.

This feature is inspired from `django-crispy-forms`

```python
from django_formify.tailwind.formify_helper import FormifyHelper
from django_formify.tailwind.layout import Div, Field, Layout, Submit


class ExampleForm(forms.Form):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.formify_helper = FormifyHelper()
        self.formify_helper.layout = Layout(
            Div(
                Div(Field("email"), css_class="col-span-12 md:col-span-6"),
                Div(Field("password"), css_class="col-span-12 md:col-span-6"),
                Div(Field("address"), css_class="col-span-12"),
                Div(Field("address2"), css_class="col-span-12"),
                Div(Field("city"), css_class="col-span-12 md:col-span-6"),
                Div(Field("state"), css_class="col-span-12 md:col-span-4"),
                Div(Field("zip_code"), css_class="col-span-12 md:col-span-2"),
                Div(Field("check_box"), css_class="col-span-12"),
                Div(Submit(text="Sign in"), css_class="col-span-12"),
                css_class="grid grid-cols-12 gap-3",
            ),
        )
```

![](./images/form_grid.jpg)

The `django_formify.tailwind.layout` current contains below classes for developers to use:

- Layout
- Div
- HTML
- Button
- Submit
- Reset
- Field
- Fieldset

## Horizontal Form

Some people might have heard of a horizontal form, where the field labels and fields are arranged side by side

To make it work, please use below code

```python
form.formify_helper = FormifyHelper()
form.formify_helper.field_wrapper_class = "md:flex md:items-center mb-6"
form.formify_helper.label_container_class = "md:w-1/3"
form.formify_helper.field_container_class = "md:w-2/3"
```

![](./images/horizontal_form.jpg)
