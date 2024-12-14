from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Office, MeetingRoom, Booking
from .serializers import OfficeSerializer, MeetingRoomSerializer, BookingSerializer
from .services.booking_services import BookingQuerySetServiceForGetList, BookingCreateService, BookingUpdateService, \
    BookingDestroyService


class OfficeViewSet(viewsets.ModelViewSet):
    queryset = Office.objects.all()
    serializer_class = OfficeSerializer
    permission_classes = [IsAuthenticated]


class MeetingRoomViewSet(viewsets.ModelViewSet):
    queryset = MeetingRoom.objects.all()
    serializer_class = MeetingRoomSerializer
    permission_classes = [IsAuthenticated]


class BookingViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'put', 'post', 'delete']

    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.action == 'list':
            return BookingQuerySetServiceForGetList(self.request.user, self.request.query_params).execute()
        return Booking.objects.all()

    def perform_create(self, serializer):
        BookingCreateService(self.request.user, serializer).execute()

    def perform_update(self, serializer):
        BookingUpdateService(self.request.user, serializer).execute()

    def perform_destroy(self, instance):
        BookingDestroyService(self.request.user, instance).execute()
