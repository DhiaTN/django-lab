from django.db.models import Max, Avg, Sum, F

from labs.common.models import Registration


def highest_discount(event_id=1):
    """
    >>> SELECT MAX(registration.discount) AS max_discount FROM registration
        WHERE registration.event_id = event_id
    """
    registrations = Registration.objects.filter(event_id=event_id)
    max_dicount = registrations.aggregate(max_discount=Max('discount'))
    print(max_dicount)


def total_sold_tickets(event_id=1):
    """
    >>> SELECT SUM(registration.ticket) AS total_ticket FROM registration
        WHERE registration.event_id = event_id
    """
    registrations = Registration.objects.filter(event_id=event_id)
    max_dicount = registrations.aggregate(total_ticket=Sum('ticket'))
    print(max_dicount)


def average_tickets_per_registration():
    """
    >>> SELECT AVG(registration.ticket) AS avg_ticket FROM registration
    """
    avg_ticket = Registration.objects.aggregate(avg_ticket=Avg('ticket'))
    print(avg_ticket)


def registration_tickets_price():
    """
    >>> SELECT ..., (registration.ticket * ((100 - registration.discount) * event.ticket_price) / 100) AS price 
        FROM registration INNER JOIN event ON (registration.event_id = event.id) 
        INNER JOIN member ON (registration.member_id = member.id)
    """
    tickets_price = F('ticket') * (100 - F('discount')) * F('event__ticket_price') / 100
    registration_list = Registration.objects.annotate(
        price=tickets_price).select_related()
    for r in registration_list:
        print("{0} pays {1} for {2} tickt(s) with {3}% discount".format(
            r.member, r.price, r.ticket, r.discount))


def event_income():
    """
    >>> SELECT event.name, SUM((((registration.ticket * (100 - registration.discount)) * event.ticket_price) / 100)) AS price
        FROM registration INNER JOIN event ON (registration.event_id = event.id) GROUP BY event.name
    """
    tickets_price = F('ticket') * (100 - F('discount')) * F('event__ticket_price') / 100
    registration_list = Registration.objects.values('event__name') 
    # ==> group by event
    events_income = registration_list.annotate(income=Sum(tickets_price))
    for e in events_income:
        print("{event__name} reaches {income}$ as an income".format(**e))
