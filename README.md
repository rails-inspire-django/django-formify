<div align="center">

<h1>Django Formify</h1>

<p>Django-Formify seamlessly integrates Tailwind CSS styles into your Django forms for a modern look.</p>

<p><strong><a href="https://django-formify.readthedocs.io/en/latest/">Documentation</a> &nbsp;|&nbsp; <a href="https://saashammer.com/lookbook/inspect/form_component/form_fields/">Demo site</a></strong></p>

<p><a href="https://pypi.org/project/django-formify/"><img src="https://badge.fury.io/py/django-formify.svg" alt="Pypi version"></a>
<a href="https://github.com/rails-inspire-django/django-formify/actions/workflows/runtests.yml"><img src="https://github.com/rails-inspire-django/django-formify/actions/workflows/runtests.yml/badge.svg" alt="CI status"></a></p>

</div>

```html
{% load formify %}

<form method="post">

    {% csrf_token %}

    {% render_form form %}

    {% render_submit text='Hello Formify!' variant="primary" %}

</form>
```

![Django Formify Demo](.github/assets/formify-demo.jpg)

## Documentation

## FAQ

### Django-Formify vs Crispy-Tailwind

