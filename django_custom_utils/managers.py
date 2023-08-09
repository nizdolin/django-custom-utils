from django.db import models


__all__ = [
    'ActiveManager',
]


class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)
