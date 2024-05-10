from django.db import models


class LicensePlate(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='uploads/')
    number = models.IntegerField(null=True, blank=True)
    annotations = models.FileField(upload_to='uploads/', null=True, blank=True)
    # url = models.CharField(max_length=100)
    # summary = models.CharField(max_length=5000)
    def __str__(self):
        return self.title
