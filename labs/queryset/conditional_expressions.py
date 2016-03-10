"""
Chaining only the QuerySet API (filter, exclude,...) and the lookup fields
is not enough to solve queries that match a complex patterns. Therefore Django
provides expressions like Q(), When() and Case() to perform advanced queries.
"""
from functools import reduce
from operator import or_ as OR
from datetime import date, timedelta
from django.db.models import Q, When, Case, Value

from labs.common.models import Member, Event, Registration


## Q() Object
##############


def members_matching_complex_pattern():
    """
    We can compose Q() objects as much as we need using
    the & and | operators to compose more complex statements.
    """
    name_pattern = Q(first_name__startswith='B') | Q(last_name__icontains='H')
    age_pattern = Q(age__lt=25) | Q(age__gt=30)
    composed_pattern = name_pattern & age_pattern
    member_list = Member.objects.filter(composed_pattern)
    member_email_list = member_list.values_list('email', flat=True)
    # >>> SELECT member.email FROM member WHERE (
    #     (member.first_name LIKE 'B%' OR member.last_name LIKE '%H%')
    #     AND (member.age < 25 OR member.age > 30))
    for member in member_email_list:
        print(member)


def events_matching_date_pattern():
    event_list = Event.objects.filter(Q(start__month=8) | Q(start__month=6))
    for event in event_list:
        print("{name} starts {date}".format(
            name=event.name, date=event.start_date))


def registrations_matching_complex_pattern():
    """
    Q objects generation can be also automated
    """
    predicate_list = [
        ('event__name__endswith', 'python'),
        ('member__community__name__contains', 'python')
    ]
    q_object_list = [Q(predicate) for predicate in predicate_list]
    pattern = reduce(OR, q_object_list)
    registration_number = Registration.objects.filter(pattern).count()
    print("{nbr} match the pattern 'python'".format(nbr=registration_number))


## When(), Case() expressions
##############################


def earlier_registration_discount(event_id):
    try:
        event = Event.objects.values('start').get(id=event_id)
        month_ago = event['start'] - timedelta(weeks=4)
        three_weeks_ago = event['start'] - timedelta(weeks=3)
        two_weeks_ago = event['start'] - timedelta(weeks=2)

        Registration.objects.filter(event_id=event_id).update(
            discount=Case(
                When(Q(registered_on__lte=month_ago), then=Value(15)),
                When(Q(registered_on__lte=three_weeks_ago), then=Value(10)),
                When(Q(registered_on__lte=two_weeks_ago), then=Value(5)),
                default=Value(0)
            ))
        # >>> UPDATE registration SET discount = CASE
        #    WHEN registration.registered_on <= '2016-07-15 18:00:00' THEN 15
        #    WHEN registration.registered_on <= '2016-07-22 18:00:00' THEN 10
        #    WHEN registration.registered_on <= '2016-07-29 18:00:00' THEN 5
        #    ELSE 0
        #    END WHERE registration.event_id = 3
    except Event.DoesNotExist as e:
        print("Insert valid event ID")

