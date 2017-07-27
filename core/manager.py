from django.db import models


class ContatoQuerySet(models.QuerySet):

    def ativos(self):
        return self.filter(ativo=True)

class ContatoManager(models.Manager):

    def get_queryset(self):
        return ContatoQuerySet(self.model, using=self._db)

    def ativos(self):
        return self.get_queryset().ativos()

