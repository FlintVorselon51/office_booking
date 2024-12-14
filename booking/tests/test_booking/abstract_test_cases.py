from abc import ABC
from typing import Any, Iterable

from django.urls import reverse

from tools.test import AuthenticatedAPITestCase
from booking.models import Office, MeetingRoom, Booking
from booking.tests.factories import OfficeFactory, MeetingRoomFactory, BookingFactory


class AbstractBookingTestCase(AuthenticatedAPITestCase, ABC):

    def setUp(self) -> None:
        super(AbstractBookingTestCase, self).setUp()
        self.existing_booking = BookingFactory(creator=self.user)

    def _assert_booking_fields_in_container(self, container) -> None:
        self.assertEqual(len(container), 8)
        self.assertIn('id', container)
        self.assertIn('name', container)
        self.assertIn('description', container)
        self.assertIn('meeting_room', container)
        self.assertIn('creator', container)
        self.assertIn('participants', container)
        self.assertIn('starts_at', container)
        self.assertIn('ends_at', container)

    @staticmethod
    def _create_office(**kwargs) -> Office:
        return OfficeFactory(**kwargs)

    @staticmethod
    def _create_meeting_room(office: Office, **kwargs) -> MeetingRoom:
        return MeetingRoomFactory(office=office, **kwargs)

    @staticmethod
    def _create_booking_for_user(user, **kwargs) -> Booking:
        return BookingFactory(creator=user, **kwargs)

    @staticmethod
    def _get_id_of_non_existing_booking() -> int:
        return Booking.objects.count() + 1

    @staticmethod
    def _form_booking_payload_for_user(
            user,
            excluded_fields: Iterable[str] | None = None,
            **kwargs
    ) -> dict[str, Any]:

        if excluded_fields is None:
            excluded_fields = tuple()

        instance = BookingFactory(creator=user, **kwargs)

        payload = {
            'name': instance.name,
            'description': instance.description,
            'meeting_room': instance.meeting_room.id,
            'participants': [p.id for p in instance.participants.all()],
            'starts_at': instance.starts_at,
            'ends_at': instance.ends_at,
        }

        for excluded_field in excluded_fields:
            payload.pop(excluded_field)

        return payload


class AbstractBookingListTestCase(AbstractBookingTestCase, ABC):

    def setUp(self) -> None:
        super(AbstractBookingListTestCase, self).setUp()
        self.url = self.form_url(office_id=self.existing_booking.meeting_room.office.id)

    @staticmethod
    def form_url(office_id: int) -> str:
        return reverse('booking:booking-list') + f'?office={office_id}'


class AbstractBookingDetailTestCase(AbstractBookingTestCase, ABC):

    def setUp(self) -> None:
        super(AbstractBookingDetailTestCase, self).setUp()
        self.url = reverse('booking:booking-detail', args=(self.existing_booking.id,))

    @staticmethod
    def _generate_url_for_transaction(booking: Booking) -> str:
        return reverse('booking:booking-detail', args=(booking.id,))

    @staticmethod
    def _generate_url_for_non_existing_booking() -> str:
        non_existing_booking_id = Booking.objects.last().id + 1
        url = reverse('booking:booking-detail', args=(non_existing_booking_id,))
        return url
