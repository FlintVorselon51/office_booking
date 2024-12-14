from datetime import timedelta

from rest_framework import status
from rest_framework.reverse import reverse

from booking.models import Booking
from booking.tests.test_booking.abstract_test_cases import AbstractBookingDetailTestCase


class PutBookingDetailTestCase(AbstractBookingDetailTestCase):

    def test_put_booking(self):
        payload = self._form_booking_payload_for_user(self.user)
        pk = Booking.objects.last().id
        url = reverse('booking:booking-detail', args=(pk,))

        for _ in range(2):
            response = self.client.put(url, data=payload, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self._assert_booking_fields_in_container(response.data)

    def test_put_booking_of_another_user(self):
        self.client.force_authenticate(self.another_user)
        payload = self._form_booking_payload_for_user(self.user)
        pk = Booking.objects.last().id
        url = reverse('booking:booking-detail', args=(pk,))
        response = self.client.put(url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_booking_overlapping(self):
        booking = self._create_booking_for_user(self.user)

        good_payload = self._form_booking_payload_for_user(self.user)
        good_payload['starts_at'] = booking.starts_at - timedelta(hours=1)
        good_payload['ends_at'] = booking.starts_at
        good_payload['meeting_room'] = booking.meeting_room.id
        response = self.client.put(self.url, data=good_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        good_payload['starts_at'] = booking.ends_at
        good_payload['ends_at'] = booking.ends_at + timedelta(hours=1)
        good_payload['meeting_room'] = booking.meeting_room.id
        response = self.client.put(self.url, data=good_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        bad_payload = self._form_booking_payload_for_user(self.user)
        bad_payload['starts_at'] = booking.starts_at - timedelta(minutes=30)
        bad_payload['ends_at'] = booking.starts_at + timedelta(minutes=30)
        bad_payload['meeting_room'] = booking.meeting_room.id
        response = self.client.put(self.url, data=bad_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

        bad_payload['starts_at'] = booking.ends_at - timedelta(minutes=20)
        bad_payload['ends_at'] = booking.ends_at + timedelta(minutes=20)
        bad_payload['meeting_room'] = booking.meeting_room.id
        response = self.client.put(self.url, data=bad_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)


    def test_put_booking_end_before_start(self):
        payload = self._form_booking_payload_for_user(self.user)
        payload['ends_at'] = payload['starts_at'] - timedelta(minutes=1)
        response = self.client.put(self.url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_put_booking_duration(self):
        good_payload = self._form_booking_payload_for_user(self.user)
        good_payload['ends_at'] = good_payload['starts_at'] + timedelta(seconds=300)
        pk = Booking.objects.last().id
        url = reverse('booking:booking-detail', args=(pk,))
        response = self.client.put(url, data=good_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        good_payload['ends_at'] = good_payload['starts_at'] + timedelta(seconds=7200)
        response = self.client.put(url, data=good_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        bad_payload = self._form_booking_payload_for_user(self.user)
        bad_payload['ends_at'] = bad_payload['starts_at'] + timedelta(seconds=299)
        response = self.client.put(self.url, data=bad_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

        bad_payload['ends_at'] = bad_payload['starts_at'] + timedelta(seconds=7201)
        response = self.client.put(self.url, data=bad_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_put_booking_without_name(self):
        payload = self._form_booking_payload_for_user(self.user, excluded_fields=('name',))
        response = self.client.put(self.url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_booking_without_description(self):
        payload = self._form_booking_payload_for_user(self.user, excluded_fields=('description',))
        response = self.client.put(self.url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_booking_without_meeting_room(self):
        payload = self._form_booking_payload_for_user(self.user, excluded_fields=('meeting_room',))
        response = self.client.put(self.url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_booking_without_participants(self):
        payload = self._form_booking_payload_for_user(self.user, excluded_fields=('participants',))
        response = self.client.put(self.url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_booking_without_starts_at(self):
        payload = self._form_booking_payload_for_user(self.user, excluded_fields=('starts_at',))
        response = self.client.put(self.url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_booking_without_ends_at(self):
        payload = self._form_booking_payload_for_user(self.user, excluded_fields=('ends_at',))
        response = self.client.put(self.url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
