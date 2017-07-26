from django.db import models

from core.models import Contato, Email


class ContatoQuerySet(models.QuerySet):

    def all(self):
        return self.filter(ativo=True)

class ContatoManager(models.Manager):

    def get_queryset(self):
        return ContatoQuerySet(model=Contato, using=self._db)
