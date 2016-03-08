from django.db.models import F
from django.db import transaction

from labs.models import Event, Registration
from .utils import query_statistic


@query_statistic
def has_enough_seats_gotcha():
    """
    Returns list of events with enough seats.

    Considered as gotcha because the filter is applied at Python level which
    is slow and more memory consuming. It can also lead to loss of data
    if it's combined with an update query.
    """
    event_list = Event.objects.all()
    for event in event_list:
        if event.seat_number >= event.ticket_number:
            print("{name} has enough seats".format(name=event.name))


@query_statistic
def has_enough_seats():
    """
    Returns list of events with enough seats.

    `F()` allows to  refer to a model field within a query before it's loaded,
    the filter is applied at DB level which is faster and more efficient.
    """
    event_list = Event.objects.filter(seat_number__gte=F('ticket_number'))
    event_name_list = event_list.values_list('name', flat=True)
    # >>> SELECT event.name FROM event WHERE event.seat_number >= (event.ticket_number)
    for event_name in event_name_list:
        print("{name} has enough seats".format(name=event_name))


@query_statistic
def welcome_discount_non_optimized(discount_value=10):
    """
    Added a 10% welcome discount to all registrations.

    It pulls all registrations into memory, looping over them,
    updating the field value of each one, and saving each
    one back to DB.
    """
    registration_list = Registration.objects.all()
    with transaction.atomic():
        for registration in registration_list:
            registration.discount += discount_value
            # Hits the database for each update.
            registration.save()


@query_statistic
def welcome_discount_optimized(discount_value=10):
    """
    Added a 10% welcome discount to all registrations.

    All the work is done at the DB level and the number of queries is reduced
    to 1 query independently of number of updated records.

    >>> UPDATE registration SET discount = (registration.discount + 10)
    """
    registration_list = Registration.objects.filter()
    registration_list.update(discount=F('discount') + discount_value)
