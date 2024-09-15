# Template Tags

A typical case of using formify in a template is like this:

```html
{% load formify %}

{% form_tag form action=url %}

  {% csrf_token %}

  {% render_form form %}

  {% render_submit text='Submit' css_class="btn btn-primary" %}

{% endform_tag %}
```

## form_tag

This tag is to render the form tag, it can help add some attributes to the form tag from the parameters from the template tag.

## render_form

This tag can render `form` or `formset`.

It will iterate and render all form fields automatically.

## render_submit

This tag is to render the submit button.

You can also add extra variables

```html
{% render_submit text='Sign In' css_class="custom-css" name='action_primary' value='action_primary' %}
```

`render_submit` behavior can be customized by overriding `formify_helper.render_submit` method

Please check [Formify Helper](./formify_helper.md) to learn more.

To use formify_helper attached to the `form` instance, you can pass `form` to the `render_submit` like this:

```html
{% render_submit form text='Hello' css_class="btn btn-primary" %}
```

If you have svg in submit button as indicator, you can use this approach to make your code DRY.

## render_field

In some cases, if you want to render a specific field, you can use this tag.

```html
{% render_field form.email %}
```

You can also override formify_helper variable like this:

```html
{% render_field form.email form_show_labels=False %}
```

## render_form_errors

This tag can render form non-field errors.
