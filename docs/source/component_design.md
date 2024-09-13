# Component Design

## Field Rendering

In field rendering, Django-Formify use components to render the HTML:

```
Field Wrapper                       formify.tw.field_wrapper
    Label                           formify.tw.field_label
    Field                           
    Error And Help Text             formify.tw.field_error_help_text
        Error                       formify.tw.field_error
        Help Text                   formify.tw.field_help_text
```

Notes:

1. Except `Field`, other parts are rendered using components, and each has its own logic.
2. During the rendering, components can read variable from the `formify_helper` to control the rendering behavior.

For example:

```python
form.formify_helper = FormifyHelper()
form.formify_helper.field_wrapper_class = "md:flex md:items-center mb-6"
form.formify_helper.label_container_class = "md:w-1/3"
form.formify_helper.field_container_class = "md:w-2/3"
```

After we set the above class, `formify.tw.field_wrapper` will use the above class to render something like this:

```html
<div class="md:flex md:items-center mb-6">
    <div class="md:w-1/3">
      <label for="id_email">Email</label>
    </div>
    <div class="md:w-2/3">
        <input type="text" name="email" id="id_email">
    </div>  
</div>
```

We just easily changed the form layout to horizontal form, in clean way.

## Customize

All the field rending components are build using [django-viewcomponent](https://github.com/rails-inspire-django/django-viewcomponent), you can easily build your own components to fit your needs.

For example, after you build your own `field wrapper` component, just override `field_wrapper_component` of the `formify_helper`, then it should work.

## Layout

The components in `django_formify.tailwind.layout` are all also built using `django-viewcomponent`.

You can also build custom components to fit your needs, for example, if you want to use `Accordion` to generate complex form, you can build `Accordion` and `AccordionSection` components using `django-viewcomponent`.

And then you can use them like this:

```python
class ExampleForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.formify_helper = FormifyHelper()
        self.formify_helper.layout = Layout(
            Accordion(
                AccordionSection(
                    ...
                ),
                AccordionSection(
                    ...
                ),
                AccordionSection(
                    ...
                ),
                dom_id="accordion-1"
            ),
        )
```

What is more, after creating `Accordion` component, you can also use them in normal web pages as well (not just in form rendering), which is convenient.

## Django-ViewComponent

`django-viewcomponen` provides solution for developer to build reusable components in Django, the biggest advantage in this case is that: **developers can use it to create components, which are used in both Django Templates and Python Code**

In field rendering, we can use component in the django template:

```html
{% load viewcomponent_tags %}

{% component formify_helper.field_wrapper_component as field_component %}

    {% call field_component.label %}
      {% component formify_helper.label_component field=field formify_helper=formify_helper %}{% endcomponent %}
    {% endcall %}

    {% call field_component.input %}
      {{ field_html }}
    {% endcall %}

    {% call field_component.field_helper_text_and_errors %}
      {% component formify_helper.field_error_help_text_component field=field formify_helper=formify_helper %}{% endcomponent %}
    {% endcall %}

{% endcomponent %}
```

In form layout, we can use component in the python code:

```python
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

Since `django-viewcomponent` solve problem very well, `django-formify` use it instead of creating another component solution.
