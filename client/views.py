from django.shortcuts import render
from django.views import generic
from client.models import Ticket
# Create your views here.
class TicketList(generic.ListView):
    model = Ticket
    template_name = 'ticket_list.html'

ticket_list = TicketList.as_view()
