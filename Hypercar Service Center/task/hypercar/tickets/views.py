from django.views import View
from django.http.response import HttpResponse, Http404
from django.shortcuts import render

line_of_cars = {
    'change_oil': [],
    'inflate_tires': [],
    'diagnostic': [],
}

last_processed_ticket = 0


class WelcomeView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('<h2>Welcome to the Hypercar Service!</h2>')


class MenuView(View):
    def get(self, request, *args, **kwargs):
        # return HttpResponse('<h2>Welcome to the Hypercar Service!</h2>')
        return render(request, 'menu.html', {})


class ServiceView(View):
    def get(self, request, *args, **kwargs):
        service = kwargs.get('service')
        if service not in line_of_cars.keys():
            raise Http404
        minutes_to_wait_oil_change = len(line_of_cars['change_oil']) * 2
        minutes_to_wait_inflate_tires = minutes_to_wait_oil_change + len(line_of_cars['inflate_tires']) * 5
        minutes_to_wait_diagnostic = minutes_to_wait_inflate_tires + len(line_of_cars['diagnostic']) * 30
        minutes_to_wait = {
            'change_oil': minutes_to_wait_oil_change,
            'inflate_tires': minutes_to_wait_inflate_tires,
            'diagnostic': minutes_to_wait_diagnostic,
        }
        tickets = line_of_cars['change_oil'] + line_of_cars['inflate_tires'] + line_of_cars['diagnostic']
        ticket_number = max(tickets) if tickets else 0
        context = {
            'ticket_number': ticket_number + 1,
            'minutes_to_wait': minutes_to_wait[service],
        }
        line_of_cars[service].append(ticket_number + 1)
        return render(request, 'service.html', context)


class OperatorView(View):
    def get(self, request, *args, **kwargs):
        context = {
            'change_oil': len(line_of_cars['change_oil']),
            'inflate_tires': len(line_of_cars['inflate_tires']),
            'diagnostic': len(line_of_cars['diagnostic']),
        }
        return render(request, 'operator.html', context)

    def post(self, request, *args, **kwargs):
        global last_processed_ticket
        if line_of_cars['change_oil']:
            last_processed_ticket = line_of_cars['change_oil'].pop(0)
        elif line_of_cars['inflate_tires']:
            last_processed_ticket = line_of_cars['inflate_tires'].pop(0)
        elif line_of_cars['diagnostic']:
            last_processed_ticket = line_of_cars['diagnostic'].pop(0)
        else:
            last_processed_ticket = 0
        return self.get(request, *args, **kwargs)


class NextTicketView(View):
    def get(self, request, *args, **kwargs):
        context = {
            'number_of_ticket': last_processed_ticket,
        }
        return render(request, 'next.html', context)
