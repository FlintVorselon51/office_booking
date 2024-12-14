from rest_framework import status

from booking.models import Booking
from booking.tests.test_booking.abstract_test_cases import AbstractBookingDetailTestCase


class DeleteBookingDetailTestCase(AbstractBookingDetailTestCase):
    def test_delete_booking_where_user_is_creator(self):
        self.assertTrue(Booking.objects.filter(pk=self.existing_booking.pk).exists())
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_booking_where_user_is_not_creator(self):
        self.client.force_authenticate(self.another_user)
        self.assertTrue(Booking.objects.filter(pk=self.existing_booking.pk).exists())
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_non_existing_booking(self):
        response = self.client.delete(self._generate_url_for_non_existing_booking())
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
