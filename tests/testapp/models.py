from django.db import models


class CrispyTestModel(models.Model):
    email = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
