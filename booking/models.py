from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models


User = get_user_model()

class Office(models.Model):
    name = models.CharField(max_length=63)
    address = models.CharField(max_length=255)


class MeetingRoom(models.Model):
    name = models.CharField(max_length=63)
    office = models.ForeignKey(Office, on_delete=models.CASCADE)
    capacity = models.IntegerField(validators=[MinValueValidator(1)])


class Booking(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    meeting_room = models.ForeignKey(MeetingRoom, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creator')
    participants = models.ManyToManyField(User, related_name='participants')
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()
