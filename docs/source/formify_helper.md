# Formify Helper

## Workflow

Unlike other form rendering packages, below template tags

```bash
{% render_form %}
{% render_submit %}
{% render_field %}
```

Just accept arguments from the templates, and pass the arguments to the `formify_helper` to render them.

So core logic is in the `formify_helper`

The benefit of this approach is it can be easy to customize the logic.

## Global Formify Helper

The default formify helper is `django_formify.tailwind.formify_helper.FormifyHelper`

We can create a class to inherit and override some methods to change the rendering logic.

To change the default global formify helper, just add below code to your Django settings

```python
FORMIFY = {
    "formify_helper": "xxxx",
}
```

Leveraging Python OOP, you can override some methods of the formify helper to customize the rendering behavior.

```bash
{% render_form %}            -> formify_helper.render_form
{% render_submit %}          -> formify_helper.render_submit
{% render_field %}           -> formify_helper.render_field
```

## Field Dispatcher

To make logic of rendering field more clean, there is a field dispatcher in the `render_field` method.

For example, if a field is using `TextInput` widget, it will try to use below methods to render

```
text_input
fallback
```

Notes:

1. If `text_input` method is not found in the `formify_helper` instance, `fallback` method will be used to render the field.
2. This can help developers to control rendering behavior of the specific widgets.

If you have built some custom widgets, just add a method to the `formify_helper` and make it look well, this is much cleaner.

## Formify Helper Variables

Formify Helper have some variables such as:

```python
form_show_errors = True
form_show_labels = True
field_wrapper_class = "field-wrapper mb-3"
```

Developers can override or add more variables to change the behavior.

In the final Django html, just access the variable using ``{{ formify_helper.form_show_errors }}``

For example, to control if rendering field label or not

```html
{% if field.label and formify_helper.form_show_labels %}

{% endif %}
```

## Formify Helper in Form

You can also create formify helper for the form to override the global formify helper.

```python
from django_formify.tailwind.formify_helper import FormifyHelper

class ExampleForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.formify_helper = FormifyHelper()
        self.formify_helper.field_wrapper_class = "another-field-wrapper"
```