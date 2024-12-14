from rest_framework import status

from booking.tests.test_booking.abstract_test_cases import AbstractBookingDetailTestCase


class PostBookingDetailTestCase(AbstractBookingDetailTestCase):
    def test_post_not_allowed(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
