from django.db import models


class Note(models.Model):
    title = models.CharField(max_length=200, default='')
    content = models.TextField(null=True, default='')

    def __str__(self):
        return f"{self.id}. {self.title}"
