from django.db.models import Q

from labs.common.models import Member


# Array Field
###############


def has_ruby_skills():
    """
    >>> SELECT * FROM member WHERE member.skills @> ARRAY['ruby']::varchar(30)[]
    """
    member_list = Member.objects.filter(skills__contains=['ruby'])
    for member in member_list:
        skills = ', '.join(member.skills)
        print("{0} is familiar with : {1}".format(member, skills))


def has_all_skills_within_requirement(requirement=[]):
    """
    >>> SELECT * FROM member WHERE (CASE WHEN member.skills IS NULL THEN NULL 
        ELSE coalesce(array_length(member.skills, 1), 0) END >= 1 
        AND member.skills <@ ARRAY['python', 'django', 'js', 'angular', 'ruby']::varchar(30)[])
    """
    if not requirement:
        requirement = ['python', 'django', 'js', 'angular', 'ruby']
    member_list = Member.objects.filter(
        skills__contained_by=requirement,
        skills__len__gte=1
    )
    for member in member_list:
        skills = ', '.join(member.skills)
        print("{0} is familiar with : {1}".format(member, skills))


def match_any_of_requirement(requirement=[]):
    """
    >>> SELECT * WHERE member.skills && ARRAY['python', 'django', 'js', 'angular', 'ruby']::varchar(30)[]
    """
    if not requirement:
        requirement = ['python', 'django', 'js', 'angular', 'ruby']
    member_list = Member.objects.filter(skills__overlap=requirement)
    for member in member_list:
        skills = ', '.join(member.skills)
        print("{0} matches {1} : {2}".format(member, len(skills), skills))


def has_min_3_skills():
    """
    >>> SELECT * FROM member WHERE CASE WHEN member.skills IS NULL THEN NULL
        ELSE coalesce(array_length(member.skills, 1), 0) END >= 3
    """
    member_list = Member.objects.filter(skills__len__gte=3)
    for member in member_list:
        skills = ', '.join(member.skills)
        print("{0} is familiar with : {1}".format(member, skills))


def python_as_first_skill():
    """
    >>> SELECT * WHERE UPPER(member.skills[1]::text) = UPPER('Python')
    """
    member_list = Member.objects.filter(skills__0__iexact="Python")
    for member in member_list:
        skills = ', '.join(member.skills)
        print("{0} loves python : {1}".format(member, skills))


# JSON Field
###############
# considering the follwing structure:
# info = {
#         "languages": [{
#             "name": "English",
#             "level": 8
#         }, {
#             "name": "French",
#             "level": 7
#         }],
#         "contact": {
#             "personal": {
#                 "phone": "7986546",
#                 "street": "8"
#             },
#             "work": {
#                 "phone": "6789546",
#                 "street": "123"
#             }
#         },
#         "websites": ["site1", "site2"]
#     }
#######################################


def has_website():
    """
    Returns members who have the given key:

    >>> SELECT * FROM member WHERE (member.info ? 'websites'
        AND NOT (member.info -> 'websites' = '[]'
        AND member.info IS NOT NULL))
    """
    member_list = Member.objects.filter(
        Q(info__has_key='websites'),
        ~Q(info__websites__exact=[])
    )
    for member in member_list:
        websites = ', '.join(member.info.get('websites'))
        print("{0} has {1} websites: {2}".format(
            member,
            len(member.info.get('websites')),
            websites
        ))


def has_work_and_presonal_phone():
    """
    Multiple keys can be chained together as deep as the structure:

    >>> SELECT COUNT(*) AS __count FROM member 
        WHERE (member.info #> ARRAY['contact', 'work', 'phone'] > ''
        AND member.info #> ARRAY['contact', 'personal', 'phone'] > '')
    """
    count = Member.objects.filter(
        # if key does not exist it will be considered as not matching
        info__contact__work__phone__gt="",
        info__contact__personal__phone__gt=""
    ).count()
    print("{0} members provided work and personal phone contact".format(count))


def can_speak_french():
    """
    Usual lookup (conatins, contained_by, gte, ...) still can be chained:

    >>> SELECT COUNT(*) AS __count FROM member
        WHERE (member.info -> 'languages' @> '[{name: French}]'
        OR member.info -> 'languages' @> '[{name: french}]')
    """
    count = Member.objects.filter(
        Q(info__languages__contains=[{'name': 'French'}]) |
        Q(info__languages__contains=[{'name': 'french'}])
    ).count()
    print("{0} members speak French.".format(count))
