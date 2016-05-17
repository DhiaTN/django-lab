from django.db.models import Value
from django.db import transaction
from django.db.models.functions import Concat

from labs.common.models import Community
from labs.common.decorators import query_statistic


## Bulk create
##############


@query_statistic
def insert_list_worse_practice():
    """
    Hits the DB 2000 and auto-commits each time.
    """
    for i in range(2000):
        name = "community_{0}".format(i)
        Community.objects.create(name=name)


@query_statistic
def insert_list_better_practice():
    """
    Hits the DB 2000 but commits once at the end.
    """
    with transaction.atomic():
        for i in range(2000):
            name = "community_{0}".format(i)
            Community.objects.create(name=name)


@query_statistic
def insert_list_best_practice():
    """
    By default hits the DB once no matter how many objects, except in SQLite.
    How many objects can be created in a single query can be specified through
    the parameter `batch_size`. In SQLite it's about 999 per query.

    NB:
      - save() will not be called, and the related signals will not be sent.
      - does not work with m2m relationships.
    """
    list_to_insert = list()
    for i in range(2000):
        name = "community_{0}".format(i)
        list_to_insert.append(Community(name=name))
    Community.objects.bulk_create(list_to_insert)


## Bulk update
##############


@query_statistic
def update_list_worse_practice():
    """
    Hits the DB 2000 and auto-commits after each query.
    """
    communities = Community.objects.filter(name__startswith='community')
    for community in communities:
        community.name = community.name + ' e.V'
        community.save()


@query_statistic
def update_list_better_paractice():
    """
    Hits the DB 2000 but commits once at the end.
    """
    communities = Community.objects.filter(name__startswith='community')
    with transaction.atomic():
        for community in communities:
            community.name = community.name + ' e.V'
            community.save()


@query_statistic
def update_list_best_practice():
    """
    Hits the DB once no matter how many objects.
    NB:
      - save() will not be called, and the related signals will not be sent.
      - does not work with m2m relationships.

    >>> UPDATE community SET name = (community.name + ' e.V')
        WHERE community.name LIKE 'community%'
    """
    communities = Community.objects.filter(name__startswith='community')
    communities.update(name=Concat('name', Value(' e.V')))


## Bulk delete
##############


@query_statistic
def delete_list_best_practice():
    """
    Reduce the DB hits as much as possible depending on the DB performance.
    NB:
      - delete() will not be called, however still emit it's related signals
    """
    communities = Community.objects.filter(name__startswith='community')
    communities.delete()
