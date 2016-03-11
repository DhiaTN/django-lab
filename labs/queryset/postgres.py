from labs.common.models import Member


# Array Field
###############


def has_ruby_skills():
    member_list = Member.objects.filter(skills__contains=['ruby'])
    for member in member_list:
        skills = ', '.join(member.skills)
        print("{0} is familiar with : {1}".format(member, skills))


def has_all_skills_within_requirement(requirement=[]):
    if not requirement:
        requirement = ['python', 'django', 'js', 'angular', 'ruby']
    member_list = Member.objects.filter(skills__contained_by=requirement)
    for member in member_list:
        skills = ', '.join(member.skills)
        print("{0} is familiar with : {1}".format(member, skills))


def match_any_of_requirement(requirement=[]):
    if not requirement:
        requirement = ['python', 'django', 'js', 'angular', 'ruby']
    member_list = Member.objects.filter(skills__overlap=requirement)
    for member in member_list:
        skills = ', '.join(member.skills)
        print("{0} matches {1} : {2}".format(member, len(skills), skills))


def has_min_3_skills():
    member_list = Member.objects.filter(skills__len__gte=3)
    for member in member_list:
        skills = ', '.join(member.skills)
        print("{0} is familiar with : {1}".format(member, skills))


def python_as_first_skill():
    member_list = Member.objects.filter(skills__0__iexact="Python")
    for member in member_list:
        skills = ', '.join(member.skills)
        print("{0} loves python : {1}".format(member, skills))


# JSON Field
###############


# HStore Field
###############
