# Layout

The layout is to help control the form layout in Python code.

This feature is inspired from `django-crispy-forms`

```python
from django_formify.tailwind.layout import Div, Field, Layout, Submit


class ExampleForm(forms.Form):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.formify_helper = FormifyHelper()
        self.formify_helper.layout = Layout(
            Div(
                Div(
                    Field("email"),
                    css_class="col-span-12 md:col-span-6",
                ),
                Div(
                    Field("password"),
                    css_class="col-span-12 md:col-span-6",
                ),
                Div(
                    Field("address"),
                    css_class="col-span-12",
                ),
                Div(
                    Field("address2"),
                    css_class="col-span-12",
                ),
                Div(
                    Field("city"),
                    css_class="col-span-12 md:col-span-6",
                ),
                Div(
                    Field("state"),
                    css_class="col-span-12 md:col-span-4",
                ),
                Div(
                    Field("zip_code"),
                    css_class="col-span-12 md:col-span-2",
                ),
                Div(
                    Field("check_box"),
                    css_class="col-span-12",
                ),
                Div(
                    Submit(text="Sign in"),
                    css_class="col-span-12",
                ),
                css_class="grid grid-cols-12 gap-3",
            ),
        )
```


![](./images/form_grid.jpg)
