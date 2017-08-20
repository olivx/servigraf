from django.contrib import admin
from django.contrib.admin import SimpleListFilter

# Register your models here.
from catalogo.models import Produto


class ListFilterTipo(SimpleListFilter):
    title = 'Produto/Serviço'
    parameter_name = 'tipo'

    def lookups(self, request, model_admin):
        return (
            (1, 'Produto'),
            (2, 'Serviço')
        )

    def queryset(self, request, queryset):
        if self.value() is not None:
            return queryset.filter(tipo=self.value())
        else:
            return queryset.all()


@admin.register(Produto)
class ProdutoModelAdmin(admin.ModelAdmin):
    list_display = ['nome', 'valor', 'quantidade', '_tipo']
    list_filter = ['ativo', ListFilterTipo]
    search_fields = ['nome', 'desc', 'id']
    list_per_page = 10

    def _tipo(self, obj):
        if obj.tipo == 1:
            return 'PRODUTO'
        return 'SERVICO'
