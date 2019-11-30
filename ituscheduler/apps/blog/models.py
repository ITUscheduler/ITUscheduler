from django.db import models

from ..scheduler.models import ExtendedUser


class Post(models.Model):
    author = models.ForeignKey(ExtendedUser, on_delete=models.PROTECT)
    content = models.TextField()
    media = models.ImageField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return str(self.content[:40])
