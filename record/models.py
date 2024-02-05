from django.db import models


class Record(models.Model):
    url = models.URLField(max_length=2000)
    header = models.CharField(max_length=255)
