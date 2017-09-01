from core.models import Cliente, Contato, Email, Telefone
from django.contrib import admin
from core.forms import ClientForm

# Register your models here.

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):

    list_display = ['__str__', 'razao_social', 'documento', 'tipo', 'mensalista']
    search_fields = ('nome_fantasia', 'razao_social', 'documento')
    list_filter = ('mensalista','ativo', 'tipo')
    ordering = ('-criado_em',)

    # form = ClientForm


class EmailContatoInline(admin.TabularInline):
    model =  Email
    extra = 1

class TelefoneContatoInline(admin.TabularInline):
    model = Telefone
    extra = 1

@admin.register(Contato)
class ContatoAdmin(admin.ModelAdmin):
    inlines =  [EmailContatoInline, TelefoneContatoInline]
    list_filter = ('ativo', )
    search_fields = ('nome', 'sobre_nome', '=cliente__nome_fantasia')
    list_display = ('nome', 'sobre_nome' , 'cliente', )




