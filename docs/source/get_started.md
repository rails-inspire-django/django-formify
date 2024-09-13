# Get Started

## Simple Form Rendering

Let's assume you already have Django forms.

To render the form with good style in the template

```html
{% load formify %}

<!DOCTYPE html>
<html>
<head>
  <title>My Form</title>
  <script src="https://cdn.tailwindcss.com?plugins=forms"></script>
</head>
<body>

<div class="w-full max-w-3xl mx-auto px-4">
  <form method="post">
    
    {% csrf_token %}

    {% render_form form %}
    
    {% render_submit text='Submit' css_class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline" %}
    
  </form>
</div>

</body>
</html>
```

Notes:

1. We `{% load formify %}` at the top to use relevant tags.
2. We use `<script src="https://cdn.tailwindcss.com?plugins=forms"></script>` to import Tailwind CSS and the `form` plugin, this is for testing purpose only.
3. `{% render_form form %}` is to iterate form fields and display all the fields with their labels and errors.
4. `{% render_submit %}` is to help render submit button with custom text and CSS class.

![](./images/simple_form.jpg)

It will also help display form non-field errors and form field errors as well.

![](./images/simple_form_errors.jpg)

## Render Fields Manually

If you want more control of the form layout, you can render fields manually.

```html
{% load formify %}

<!DOCTYPE html>
<html>
<head>
  <title>My Form</title>
  <script src="https://cdn.tailwindcss.com?plugins=forms"></script>
</head>
<body>

<div class="w-full max-w-3xl mx-auto px-4">
  <form method="post">

    {% csrf_token %}

    <div class="grid grid-cols-12 gap-3">
      <div class="col-span-12 md:col-span-6">
        {% render_field form.name %}
      </div>
      <div class="col-span-12 md:col-span-6">
        {% render_field form.email %}
      </div> 
    </div>
    
    {% render_submit text='Submit' css_class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline" %}

  </form>
</div>

</body>
</html>
```

Notes:

You can use `{% render_field form.email %}` to render specific form field.
