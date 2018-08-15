from django.contrib import admin

# Register your models here.
from client.models import CatalogoGrupo, GrupoCliente, Ticket, TicketItem, StatusTrail
from catalogo.models import Produto
from core.models import Cliente
from client.forms import CatalogoGrupoForm


@admin.register(GrupoCliente)
class GrupoClienteAdmin(admin.ModelAdmin):

    list_display = ('title', )
    search_fields = ('title', 'clientes__nome_fantasia', 'users__profile__full_name',)
    filter_horizontal = ('users' , 'clientes', 'produtos',)


@admin.register(CatalogoGrupo)
class CatalogoGrupoAdmin(admin.ModelAdmin):

    form = CatalogoGrupoForm
    list_display = ('grupo', 'produto','valor',)
    search_fields = ('grupo__title', 'produto__nome',)

    def get_form(self, request, obj=None, **kwargs):
        form = super(CatalogoGrupoAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['produto'].queryset = Produto.objects.all().order_by('nome')
        return form

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        obj.save()

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):

    list_display = ('pk','get_group', 'cliente', 'data_entrega', 'owner', 'criado_em','status','ativo',)
    list_display_links = ('cliente',)
    search_fields = ('cliente__nome_fantasia', 'pk')
    autocomplete_fields = ('cliente',)
    list_filter = ('ativo',)


    def get_group(self, instance):
        group = GrupoCliente.objects.filter(clientes=instance.cliente)
        if group.first():
            return group.first().title.upper()
        return '----'
    get_group.short_description = 'Grupo'

    def status(self, instance):
        return StatusTrail.objects.filter(ticket=instance.pk).last()

@admin.register(StatusTrail)
class StatusTrailAdmin(admin.ModelAdmin):

    list_display = ('ticket', 'status',)
    search_fields = ('ticket__cliente__nonme_fantasia', 'ticket__id')
    list_filter = ('status',)
