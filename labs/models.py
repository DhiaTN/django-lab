from django.db import models
from django.core.validators import MaxValueValidator


class Community(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Communities'


class Member(models.Model):
    name = models.CharField(max_length=20)
    community = models.ForeignKey("Community", related_name="members",
                                  null=True, blank=True)
    events = models.ManyToManyField("Event", through="Registration",
                                    related_name="attendees", blank=True)

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=20)
    start = models.DateTimeField()
    end = models.DateTimeField()
    ticket_number = models.IntegerField(blank=True, null=True)
    seat_number = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name


class Registration(models.Model):
    member = models.ForeignKey("Member", related_name="registrations",
                               on_delete=models.CASCADE)
    event = models.ForeignKey("Event", related_name="registrations",
                              on_delete=models.CASCADE)
    ticket = models.IntegerField(default=1)
    online = models.BooleanField(max_length=1)
    discount = models.PositiveIntegerField(validators=[MaxValueValidator(100)], default=0)

    def __str__(self):
        return '{member} / {event}'.format(
            member=self.member.name,
            event=self.event.name
        )

    class Meta:
        unique_together = ('member', 'event')
