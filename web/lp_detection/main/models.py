from django.db import models
from django.utils import timezone


def current_time():
    return timezone.now().time()


class LicensePlate(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(upload_to='uploads/')
    number = models.IntegerField(null=True, blank=True)
    annotations = models.FileField(upload_to='uploads/', null=True, blank=True)
    def __str__(self):
        return self.title


class Task(models.Model):
    id = models.AutoField(primary_key=True)
    # number = models.IntegerField()
    status = models.CharField(max_length=50)
    worker_id = models.CharField(max_length=50)
    mode = models.CharField(max_length=50)
    time = models.TimeField(default=current_time)
