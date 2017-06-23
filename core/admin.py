from core.models import Cliente, Contato, Email, Telefone
from django.contrib import admin
from core.forms import ClientForm

# Register your models here.

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):

    list_display = ['__str__', 'razao_social', 'documento', 'tipo', 'mensalista']
    search_fields = ('nome_fantasia', 'razao_social', 'cpf', 'cnpj')
    list_filter = ('mensalista',)
    ordering = ('-criado_em',)

    form = ClientForm


class EmailContatoInline(admin.TabularInline):
    model =  Email
    extra = 1

class TelefoneContatoInline(admin.TabularInline):
    model = Telefone
    extra = 1

@admin.register(Contato)
class ContatoAdmin(admin.ModelAdmin):
    inlines =  [EmailContatoInline, TelefoneContatoInline]


