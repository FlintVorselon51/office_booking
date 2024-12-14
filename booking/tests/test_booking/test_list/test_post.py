from datetime import timedelta

from rest_framework import status

from booking.models import Booking, MeetingRoom
from booking.tests.test_booking.abstract_test_cases import AbstractBookingListTestCase


class PostBookingListTestCase(AbstractBookingListTestCase):

    def test_post_booking(self):
        payload = self._form_booking_payload_for_user(self.user)
        payload['ends_at'] = payload['starts_at'] + timedelta(hours=1)
        Booking.objects.all().delete()

        response = self.client.post(self.url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self._assert_booking_fields_in_container(response.data)

        response = self.client.post(self.url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_post_booking_overlapping_with_the_same_meeting_room(self):
        payload = self._form_booking_payload_for_user(self.user)
        good_payload = payload.copy()
        bad_payload = payload.copy()

        Booking.objects.all().delete()
        booking = self._create_booking_for_user(
            self.user,
            meeting_room=MeetingRoom.objects.get(id=payload['meeting_room']),
        )

        good_payload['starts_at'] = booking.starts_at - timedelta(hours=1)
        good_payload['ends_at'] = booking.starts_at
        response = self.client.post(self.url, data=good_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        Booking.objects.all().delete()

        booking = self._create_booking_for_user(
            self.user,
            meeting_room=MeetingRoom.objects.get(id=payload['meeting_room']),
        )

        good_payload['starts_at'] = booking.ends_at
        good_payload['ends_at'] = booking.ends_at + timedelta(hours=1)
        response = self.client.post(self.url, data=good_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        Booking.objects.all().delete()
        booking = self._create_booking_for_user(
            self.user,
            meeting_room=MeetingRoom.objects.get(id=payload['meeting_room']),
        )

        bad_payload['starts_at'] = booking.starts_at - timedelta(minutes=30)
        bad_payload['ends_at'] = booking.starts_at + timedelta(minutes=30)
        response = self.client.post(self.url, data=bad_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

        Booking.objects.all().delete()
        booking = self._create_booking_for_user(
            self.user,
            meeting_room=MeetingRoom.objects.get(id=payload['meeting_room']),
        )
        bad_payload['starts_at'] = booking.ends_at - timedelta(minutes=20)
        bad_payload['ends_at'] = booking.ends_at + timedelta(minutes=20)
        response = self.client.post(self.url, data=bad_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_post_booking_overlapping_with_different_meeting_room(self):
        payload = self._form_booking_payload_for_user(self.user)
        good_payload = payload.copy()
        bad_payload = payload.copy()
        Booking.objects.all().delete()
        booking = self._create_booking_for_user(self.user)

        good_payload['starts_at'] = booking.starts_at - timedelta(hours=1)
        good_payload['ends_at'] = booking.starts_at
        response = self.client.post(self.url, data=good_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        Booking.objects.all().delete()
        booking = self._create_booking_for_user(self.user)

        good_payload['starts_at'] = booking.ends_at
        good_payload['ends_at'] = booking.ends_at + timedelta(hours=1)
        response = self.client.post(self.url, data=good_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        Booking.objects.all().delete()
        booking = self._create_booking_for_user(self.user)

        bad_payload['starts_at'] = booking.starts_at - timedelta(minutes=30)
        bad_payload['ends_at'] = booking.starts_at + timedelta(minutes=30)
        response = self.client.post(self.url, data=bad_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        Booking.objects.all().delete()
        booking = self._create_booking_for_user(self.user)

        bad_payload['starts_at'] = booking.ends_at - timedelta(minutes=20)
        bad_payload['ends_at'] = booking.ends_at + timedelta(minutes=20)
        response = self.client.post(self.url, data=bad_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_booking_end_before_start(self):
        payload = self._form_booking_payload_for_user(self.user)
        Booking.objects.all().delete()

        payload['ends_at'] = payload['starts_at'] - timedelta(minutes=1)
        response = self.client.post(self.url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_post_booking_duration(self):
        good_payload = self._form_booking_payload_for_user(self.user)
        bad_payload = self._form_booking_payload_for_user(self.user)
        Booking.objects.all().delete()

        good_payload['ends_at'] = good_payload['starts_at'] + timedelta(seconds=300)
        response = self.client.post(self.url, data=good_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        Booking.objects.all().delete()

        good_payload['ends_at'] = good_payload['starts_at'] + timedelta(seconds=7200)
        response = self.client.post(self.url, data=good_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        Booking.objects.all().delete()

        bad_payload['ends_at'] = bad_payload['starts_at'] + timedelta(seconds=299)
        response = self.client.post(self.url, data=bad_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

        bad_payload['ends_at'] = bad_payload['starts_at'] + timedelta(seconds=7201)
        response = self.client.post(self.url, data=bad_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_post_booking_without_name(self):
        payload = self._form_booking_payload_for_user(self.user, excluded_fields=('name',))
        response = self.client.post(self.url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_booking_without_description(self):
        payload = self._form_booking_payload_for_user(self.user, excluded_fields=('description',))
        response = self.client.post(self.url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_booking_without_meeting_room(self):
        payload = self._form_booking_payload_for_user(self.user, excluded_fields=('meeting_room',))
        response = self.client.post(self.url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_booking_without_participants(self):
        payload = self._form_booking_payload_for_user(self.user, excluded_fields=('participants',))
        response = self.client.post(self.url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_booking_without_starts_at(self):
        payload = self._form_booking_payload_for_user(self.user, excluded_fields=('starts_at',))
        response = self.client.post(self.url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_booking_without_ends_at(self):
        payload = self._form_booking_payload_for_user(self.user, excluded_fields=('ends_at',))
        response = self.client.post(self.url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
