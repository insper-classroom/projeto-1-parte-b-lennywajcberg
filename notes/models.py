from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=40, unique=True)  # evita duplicatas

    def __str__(self):
        return self.name

class Note(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(null=True)
    # 0..1 tag por nota: Many-to-One
    tag = models.ForeignKey(
        Tag,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name="notes"
    )

    def __str__(self):
        return f"{self.id}. {self.title}"
