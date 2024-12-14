from rest_framework import status

from booking.tests.test_booking.abstract_test_cases import AbstractBookingListTestCase


class PatchBookingListTestCase(AbstractBookingListTestCase):
    def test_patch_not_allowed(self):
        response = self.client.patch(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
