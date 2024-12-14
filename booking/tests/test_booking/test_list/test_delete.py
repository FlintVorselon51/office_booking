from rest_framework import status

from booking.tests.test_booking.abstract_test_cases import AbstractBookingListTestCase


class DeleteBookingListTestCase(AbstractBookingListTestCase):
    def test_delete_not_allowed(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
