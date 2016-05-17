from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator

# PostgreSQL Fields
from django.contrib.postgres.fields import ArrayField, HStoreField
from django.contrib.postgres.fields.jsonb import JSONField

from .mixins import SerializationMixin
from .settings import DATE_PATTERN
from .validators import (location_schema_validator, info_schema_validator,
                         skills_schema_validator)


class Community(SerializationMixin, models.Model):
    name = models.CharField(max_length=20)
    locations = ArrayField(
        ArrayField(models.FloatField(default=0.0), size=2),
        default=list,
        blank=True, null=True,
        validators=[location_schema_validator],
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Communities'


class Member(SerializationMixin, models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    age = models.PositiveIntegerField(default=20)
    community = models.ForeignKey("Community", related_name="members",
                                  null=True, blank=True)
    events = models.ManyToManyField("Event", through="Registration",
                                    related_name="attendees", blank=True)
    skills = ArrayField(
        models.CharField(max_length=30),
        default=list,
        blank=True, null=True,
        validators=[skills_schema_validator]
    )
    info = JSONField(
        default=dict,
        blank=True, null=True,
        validators=[info_schema_validator]
    )
    contact = HStoreField(blank=True, null=True)

    def __str__(self):
        return "{0} {1}".format(self.first_name, self.last_name)


class Event(SerializationMixin, models.Model):
    name = models.CharField(max_length=20)
    start = models.DateTimeField()
    end = models.DateTimeField()
    ticket_number = models.IntegerField(blank=True, null=True)
    ticket_price = models.IntegerField(blank=True, null=True)
    seat_number = models.IntegerField(blank=True, null=True)

    @property
    def start_date(self):
        return DATE_PATTERN.format(self.start)

    @property
    def end_date(self):
        return DATE_PATTERN.format(self.end)

    def __str__(self):
        return self.name


class Registration(SerializationMixin, models.Model):
    member = models.ForeignKey("Member", related_name="registrations",
                               on_delete=models.CASCADE)
    event = models.ForeignKey("Event", related_name="registrations",
                              on_delete=models.CASCADE)
    ticket = models.IntegerField(default=1)
    online = models.BooleanField(max_length=1)
    discount = models.PositiveIntegerField(
        validators=[MaxValueValidator(100)], default=0)
    registered_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '{member} / {event}'.format(
            member=self.member.first_name,
            event=self.event.name
        )

    class Meta:
        unique_together = ('member', 'event')
