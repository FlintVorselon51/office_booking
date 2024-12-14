from rest_framework import status

from booking.models import Booking
from booking.tests.test_booking.abstract_test_cases import AbstractBookingDetailTestCase


class GetBookingDetailTestCase(AbstractBookingDetailTestCase):

    def test_get_user_booking(self) -> None:
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self._assert_booking_fields_in_container(response.data)

    def test_get_another_user_booking(self) -> None:
        self.client.force_authenticate(self.another_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_non_existing_booking(self) -> None:
        response = self.client.get(self._generate_url_for_non_existing_booking())
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
