from .utils import query_statistic
from labs.models import Community, Member, Event, Registration


@query_statistic
def all_communities():
    """
    Django pulls all objects in a single query
    but the related objects are only fetched on demand.
    >>> SELECT community.id, community.name FROM community
    """
    communities = Community.objects.all()  # lazy evaluation
    for community in communities:
        name = community.name


#############################################
#### OneToOne / ForeignKey relationships ####
#############################################


## Forward relation
###################


@query_statistic
def community_per_member_non_optimised():
    """
    Django executes an extra query against the community relation
    for every member.
    """
    members = Member.objects.all()  # lazy evaluation
    # >>> SELECT member.id, member.name, member.community_id FROM member
    for member in members:
        # Hits the database for each member to retrieve the associated Community.
        print("{0} joined {1}".format(member.name, member.community.name))
        # >>> SELECT community.id, community.name FROM community WHERE community.id = member.community_id


@query_statistic
def community_per_member_optimised():
    """
    Django pulls all objects including ForeignKey relation data
    in single SQL join query:

    >>> SELECT member.id, member.name, member.community_id, community.id,
        community.name FROM member LEFT OUTER JOIN community ON
        (member.community_id = community.id)
    """
    members = Member.objects.all()
    members = members.select_related('community')  # lazy evaluation
    for member in members:
        # Doesn't hit the database, instead uses the cached version.
        print("{0} joined {1}".format(member.name, member.community.name))


## Backward relation
####################


@query_statistic
def members_per_community_non_optimised():
    """
    Django executes an extra query against the members reverse
    relation for every community.
    """
    communities = Community.objects.all()  # lazy evaluation
    # >>> SELECT community.id, community.name FROM community

    for community in communities:
        # Hits the database for each community to retrieve its associated members.
        members = community.members.all()
        # >>> SELECT member.id, member.name, member.community_id FROM member WHERE
        #     member.community_id = community.id
        print("{0} has {1} members".format(community.name, len(members)))


@query_statistic
def members_per_community_optimised():
    """
    Django pulls all objects including related objects in 2 separate
    queries, saves the related objects as cached data and then perform
    a join at Python level:

    >>> SELECT community.id, community.name FROM community

    >>> SELECT member.id, member.name, member.community_id FROM member
        WHERE member.community_id IN (1, 2, 3)
    """
    communities = Community.objects.prefetch_related('members')  # lazy evaluation
    for community in communities:
        # Doesn't hit the database, instead uses the cached version.
        members = community.members.all()
        print("{0} has {1} members".format(community.name, len(members)))


##################################
#### ManyToMany relationships ####
##################################


@query_statistic
def events_per_member_non_optimised():
    """
    Django executes an extra query against the event relation
    for every member.
    """
    members = Member.objects.all()  # lazy evaluation
    # >>> SELECT member.id, member.name, member.community_id FROM member
    for member in members:
        # Hits the database for each member to retrieve the associated events.
        events_number = member.events.count()
        # >>> SELECT COUNT(*) AS __count FROM event INNER JOIN registration
        #     ON (event.id = registration.event_id)
        #     WHERE registration.member_id = member.id
        print("{0} registred in {1} events".format(
            member.name,
            events_number
        ))


@query_statistic
def events_per_member_optimised_1():
    """
    Django pulls all objects including related objects in 2 separate
    queries, saves the related objects as cached data and then perform
    a join at Python level:

    >>> SELECT member.id, member.name, member.community_id FROM member

    >>> SELECT (registration.member_id) AS _prefetch_related_val_member_id, event.id,
        event.name, event.start, event.end FROM event INNER JOIN registration
        ON (event.id = registration.event_id) WHERE registration.member_id IN (1, 2, 3)
    """

    members = Member.objects.prefetch_related('events')
    for member in members:
        # Doesn't hit the database, instead uses the cached version.
        print("{0} registred in {1} events".format(
            member.name,
            len(member.events.all())
        ))


@query_statistic
def events_per_member_optimised_2():
    """
    Since select_related can't be applied on a many-to-many relationships
    we can also use the following approach.
    """
    members = Member.objects.all()   # lazy evaluation
    # >>> SELECT member.id, member.name, member.community_id FROM member
    registrations = Registration.objects.filter(member__in=members)
    registrations = registrations.select_related("event")  # lazy evaluation
    # >>> SELECT registration.id, registration.member_id, registration.event_id,
    #     registration.ticket, registration.online, event.id, event.name, event.start,
    #     event.end FROM registration INNER JOIN event ON (registration.event_id = event.id)
    #     WHERE registration.member_id IN (SELECT member.id FROM member)
    registration_dict = dict()
    get = registration_dict.get
    for registration in registrations:
        member_id = registration.member_id
        registration_dict[member_id] = get(member_id, []) + [registration.event]
    for member in members:
        print("{0} registred in {1} events".format(
            member.name,
            len(registration_dict[member_id])
        ))
