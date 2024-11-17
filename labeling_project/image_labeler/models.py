from django.db import models

class ImageData(models.Model):
    image_name = models.CharField(max_length=255)
    label = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.image_name}: {self.label if self.label else 'No Label'}"
