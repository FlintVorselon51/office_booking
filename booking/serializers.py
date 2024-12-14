from rest_framework import serializers
from .models import Office, MeetingRoom, Booking


class OfficeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Office
        fields = '__all__'


class MeetingRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingRoom
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ('creator',)

    def create(self, validated_data):
        user = self.context['request'].user
        participants_data = validated_data.pop('participants', [])
        booking = Booking.objects.create(creator=user, **validated_data)
        if participants_data:
            booking.participants.set(participants_data)
        return booking
