from django.db import models
from django.db.models import QuerySet


class ActiveManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(is_active=True)
