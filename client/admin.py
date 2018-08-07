from django.contrib import admin

# Register your models here.
from client.models import CatalogoGrupo, GrupoCliente, Ticket, TicketItem
from client.forms import CatalogoGrupoForm
from catalogo.models import Produto


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
