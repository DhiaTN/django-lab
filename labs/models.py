from django.db import models


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

    def __str__(self):
        return self.name


class Registration(models.Model):
    member = models.ForeignKey("Member", related_name="registrations",
                               on_delete=models.CASCADE)
    event = models.ForeignKey("Event", related_name="registrations",
                              on_delete=models.CASCADE)
    ticket = models.IntegerField(default=1)
    online = models.BooleanField(max_length=1)

    def __str__(self):
        return '{member} / {event}'.format(
            member=self.member.name,
            event=self.event.name
        )

    class Meta:
        unique_together = ('member', 'event')
