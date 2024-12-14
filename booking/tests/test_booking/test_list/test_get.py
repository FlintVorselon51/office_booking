from django.urls import reverse
from rest_framework import status

from booking.models import Office
from booking.tests.test_booking.abstract_test_cases import AbstractBookingListTestCase


class GetBookingListTestCase(AbstractBookingListTestCase):
    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_bookings_for_non_existing_office(self):
        non_existing_office_id = Office.objects.last().id + 1
        url = self.form_url(non_existing_office_id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # def test_get_returns_only_bookings_for_specified_office(self):
    #     def get_response_booking_ids(r) -> list[int]:
    #         return [i['id'] for i in r.data.get('results', [])]
    #
    #     new_booking = self._create_booking_for_user(self.user)
    #     self.assertNotEqual(self.existing_booking.meeting_room.office, new_booking.meeting_room.office)
    #
    #     response = self.client.get(self.url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertIn(self.existing_booking.id, get_response_booking_ids(response))
    #     self.assertNotIn(new_booking.id, get_response_booking_ids(response))
    #
    #     response = self.client.get(self.form_url(new_booking.meeting_room.office.id))
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertIn(new_booking.id, get_response_booking_ids(response))
    #     self.assertNotIn(self.existing_booking.id, get_response_booking_ids(response))

    def test_get_without_office_id(self):
        response = self.client.get(reverse('booking:booking-list'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
