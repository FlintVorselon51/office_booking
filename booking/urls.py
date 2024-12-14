from rest_framework.routers import DefaultRouter
from .views import OfficeViewSet, MeetingRoomViewSet, BookingViewSet

app_name = 'booking'

router = DefaultRouter()
router.register(r'offices', OfficeViewSet, basename='office')
router.register(r'meeting-rooms', MeetingRoomViewSet, basename='meeting-room')
router.register(r'bookings', BookingViewSet, basename='booking')

urlpatterns = router.urls
