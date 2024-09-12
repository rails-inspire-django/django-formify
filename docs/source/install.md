# Installation

```shell
$ pip install django-formify
```

Then add the app into `INSTALLED_APPS` in settings.py

```python
INSTALLED_APPS = [
    ...,
    'django_viewcomponent',       # new
    'django_formify',             # new
]
```

`django_formify` has some components build by `django_viewcomponent`, to make it work, please also update `TEMPLATES` by following the instruction below.

Modify `TEMPLATES` section of settings.py as follows:

1. Remove `'APP_DIRS': True,`
2. add `loaders` to `OPTIONS` list and set it to following value:

```python
TEMPLATES = [
    {
        ...,
        'OPTIONS': {
            'context_processors': [
                ...
            ],
            'loaders':[(
                'django.template.loaders.cached.Loader', [
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                    'django_viewcomponent.loaders.ComponentLoader',
                ]
            )],
        },
    },
]
```
