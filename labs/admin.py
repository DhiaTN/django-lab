from django.contrib import admin
from .models import Community, Member, Event, Registration


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('id', 'event', 'member', 'ticket', 'discount', 'online')
    list_filter = ('event', 'online')

admin.site.register(Community)
admin.site.register(Member)
admin.site.register(Event)

