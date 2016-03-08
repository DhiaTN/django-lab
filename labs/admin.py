from django.contrib import admin
from .models import Community, Member, Event, Registration


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('id', 'event', 'member', 'ticket',
                    'discount', 'online', 'registered_on')
    list_filter = ('event', 'member')

@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'community')


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'start', 'end')
