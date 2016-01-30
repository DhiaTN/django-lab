from labs.models import Community, Member, Event, Registration


def all_communities():
    """
    Django ORM fetchs all objects in one query.
    But external relation are only fetched on demand.
    """
    from django.db import connection
    query_count = len(connection.queries)
    communities = Community.objects.all()
    print(communities.query)
    for community in communities:
        name = community.name
    print(all_communities.__name__)
    print(len(connection.queries) - query_count)


############################################
#### OneToOne / OneToMany relationships ####
############################################


def community_per_member_non_optimised():
    """
    Django ORM will execute an additional fetch against the community relation
    for every member.
    """
    from django.db import connection
    query_count = len(connection.queries)
    members = Member.objects.all()
    print(members.query)
    for member in members:
        community = member.community.name
    print(community_per_member_non_optimised.__name__)
    print(len(connection.queries) - query_count)


def community_per_member_optimised():
    """
    Django ORM fetches all objects including nested record in one query
    """
    from django.db import connection
    query_count = len(connection.queries)
    members = Member.objects.all().select_related('community')
    for member in members:
        community = member.community.name
    print(community_per_member_optimised.__name__)
    print(members.query)
    print(len(connection.queries) - query_count)


########################################################
#### ManyToMany / ManyToOne (reverse) relationships ####
########################################################


def events_per_member_non_optimised():
    """
    Django ORM will execute an additional fetch against the event relation
    for every member.
    """
    from django.db import connection
    query_count = len(connection.queries)
    members = Member.objects.all()
    for member in members:
        events = member.events.all()
    print(events_per_member_non_optimised.__name__)
    print(events.query)
    print(len(connection.queries) - query_count)


def events_per_member_optimised():
    """
    Django ORM fetches all objects including nested record in one query
    """
    from django.db import connection
    query_count = len(connection.queries)
    members = Member.objects.all()
    events = Registration.objects.filter(
        member__in=members).select_related("events")
    for member in members:
        registration = registrations.community.name
    print(events_per_member_optimised.__name__)
    print(members.query)
    print(events.query)
    print(len(connection.queries) - query_count)
