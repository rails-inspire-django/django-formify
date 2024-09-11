# Getting Started

```shell
$ pip install django-formify
```

Then add the app into `INSTALLED_APPS` in settings.py

```python
INSTALLED_APPS = [
    ...,
    'django_formify',
]
```

## dom_id

`dom_id` is a helper method that returns a unique DOM ID based on the object's class name and primary key.

```html
{% load template_simplify %}

{% dom_id instance %}               ->  task_1
{% dom_id instance 'detail' %}      ->  detail_task_1
{% dom_id Task %}                   ->  new_task
```

1. `dom_id` first argument can be string, instance or Model class
2. `dom_id` second argument is optional string that will be used as `prefix`.

You can also use it in your Django view code.

```python
from template_simplify import dom_id

target = dom_id(instance, "detail_container")
```

We can say goodbye to `id="task-{{ task.pk }}"` and use `id="{% dom_id task %}"` instead.

The benefit is, **it simplified the DOM ID generation in Python and Django template, and avoid typo error in many cases.**

## class_names

Inspired by JS [classnames](https://www.npmjs.com/package/classnames) and Rails `class_names`

`class_names` can help **conditionally render css classes**

```html
{% load template_simplify %}

<div class="{% class_names test1=True 'test2' ring-slate-900/5=True already-sign-in=request.user.is_authenticated %}"></div>

'<div class="test1 test2 ring-slate-900/5 dark:bg-slate-800 %}"></div>'
```

It can also work well with TailwindCSS's some special char such as `/` and `:`
