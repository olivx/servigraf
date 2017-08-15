from django.contrib import admin

# Register your models here.
from catalogo.models import Produto


@admin.register(Produto)
class ProdutoModelAdmin(admin.ModelAdmin):

    list_display = ['nome' , 'valor' , 'quantidade' , '_tipo']
    list_filter = ['ativo' , 'tipo']
    search_fields = ['nome', 'descricao' , 'id']
    list_per_page = 10


    def _tipo(self, obj):
        if obj.tipo == 1:
            return 'PRODUTO'
        return 'SERVICO'


