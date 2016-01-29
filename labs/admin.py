from django.contrib import admin
from .models import Community, Member, Event, Registration

admin.site.register(Community)
admin.site.register(Member)
admin.site.register(Event)
admin.site.register(Registration)
