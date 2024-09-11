from django.conf import settings


class AppSettings:
    def __init__(self):
        self.settings = getattr(settings, "FORMIFY", {})

    @property
    def FORMIFY_HELPER(self):
        return self.settings.get(
            "formify_helper",
            "django_formify.tailwind.formify_helper.FormifyHelper",
        )


app_settings = AppSettings()
