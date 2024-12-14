from abc import ABC, abstractmethod
from bisect import bisect_left
from datetime import datetime, timedelta
from typing import Any

from django.contrib.auth import get_user_model
from django.db.models import QuerySet, Q
from django.db.transaction import atomic
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.serializers import Serializer

from tools.exceptions import BadRequest, UnprocessableEntity, Conflict

from booking.models import MeetingRoom, Booking, Office

User = get_user_model()


class BookingQuerySetServiceForGetList:

    def __init__(self, user: User, query_params: dict[str, Any]) -> None:
        self.user = user
        self.query_params = query_params

    def execute(self) -> QuerySet:
        if self.query_params.get('office') is None:
            raise BadRequest('Office must be provided')

        office_id = self.query_params['office']

        try:
            Office.objects.get(id=office_id)
        except Office.DoesNotExist:
            raise NotFound(detail=f'Office with id `{office_id}` does not exist')

        return Booking.objects.filter(meeting_room__office_id=office_id)


class AbstractBookingPerformService(ABC):
    id: int | None = None
    meeting_room: MeetingRoom
    creator: User
    participants: list[User]
    starts_at: datetime
    ends_at: datetime

    def __init__(self, user: User, serializer: Serializer):
        self.user = user
        self.serializer = serializer

    def _validate_booking_duration(self):
        duration = self.ends_at - self.starts_at
        if duration < timedelta(minutes=5) or duration > timedelta(hours=2):
            raise UnprocessableEntity('Duration is out of bound')

    def _validate_overlapping(self):
        qs = Booking.objects.filter(meeting_room=self.meeting_room)
        if self.id is not None:
            qs = qs.filter(~Q(id=self.id))
        lst = [(b.starts_at.timestamp(), b.ends_at.timestamp()) for b in qs]
        lst.sort()
        i = bisect_left(lst, (self.starts_at.timestamp(), self.ends_at.timestamp()))
        if i > 0 and self.starts_at.timestamp() < lst[i - 1][1] or i < len(lst) and self.ends_at.timestamp() > lst[i][0]:
            raise Conflict()


    def _validate_booking(self):
        self._validate_booking_duration()
        self._validate_overlapping()

    @abstractmethod
    def execute(self) -> None:
        if self.serializer.instance is not None:
            self.id = self.serializer.instance.id
        else:
            self.id = None
        self.meeting_room = self.serializer.validated_data['meeting_room']
        self.participants = self.serializer.validated_data['participants']
        self.starts_at = self.serializer.validated_data['starts_at']
        self.ends_at = self.serializer.validated_data['ends_at']


class BookingCreateService(AbstractBookingPerformService):

    def execute(self) -> None:
        super().execute()
        self._validate_booking()
        with atomic():
            self.serializer.save()


class BookingUpdateService(AbstractBookingPerformService):

    def execute(self) -> None:
        super().execute()
        if not self.user.is_superuser and self.serializer.instance.creator != self.user:
            raise PermissionDenied(detail=f'{self.user} does not have permission to perform this operation')
        self._validate_booking()
        with atomic():
            self.serializer.save()


class BookingDestroyService:

    def __init__(self, user: User, booking: Booking):
        self.user = user
        self.booking = booking

    def execute(self) -> None:
        if not self.user.is_superuser and self.booking.creator != self.user:
            raise PermissionDenied(detail='You are not the creator of the booking')

        with atomic():
            self.booking.delete()
