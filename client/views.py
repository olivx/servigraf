from django.shortcuts import render
from django.views import generic
from client.models import Ticket, GrupoCliente
from account.models import Profile
# Create your views here.
class TicketList(generic.ListView):
    model = Ticket
    template_name = 'ticket_list.html'

    def get_queryset(self):
        # queryset =  super(TicketList, self).get_queryset()
        queryset =  Ticket.objects.prefetch_related('ticket_trails').select_related('cliente').all()
        if self.request.user.profile.type == Profile.CLIENT_USER:
            clientes = GrupoCliente.objects.filter(
                pk=self.request.user.profile.company_group.pk
            ).values_list('clientes', flat=True)
            print(clientes)
            print(self.request.user.profile.company_group)
            return queryset.filter(cliente__in=clientes)
        return queryset

ticket_list = TicketList.as_view()
