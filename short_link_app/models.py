
from django.db import models


# Create your models here.
class ShortLinkService(models.Model):
    """Создаёт запиcb в таблице links"""
    origin_link = models.CharField(max_length=1000, unique=True, null=False)
    short_link = models.CharField(max_length=35, unique=True, null=False)
    count = models.IntegerField(null=False, default=0)

    class Meta:
        db_table = 'links'

    def __str__(self):
        return self.origin_link
