from datetime import timezone, UTC, timedelta

import factory
from faker import Faker
from django.contrib.auth import get_user_model
from booking.models import Office, MeetingRoom, Booking

fake = Faker('ru_RU')

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.LazyAttribute(lambda _: fake.unique.email())
    name = factory.LazyAttribute(lambda _: fake.name())
    password = factory.PostGenerationMethodCall('set_password', 'SecurePassword123')


class OfficeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Office

    name = factory.LazyAttribute(lambda _: fake.company())
    address = factory.LazyAttribute(lambda _: fake.address())


class MeetingRoomFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = MeetingRoom

    name = factory.LazyAttribute(lambda _: f"Переговорная {fake.word()}")
    office = factory.SubFactory(OfficeFactory)
    capacity = factory.LazyAttribute(lambda _: fake.random_int(min=1, max=20))


class BookingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Booking

    name = factory.LazyAttribute(lambda _: f"Встреча {fake.word()}")
    description = factory.LazyAttribute(lambda _: fake.text(max_nb_chars=200))
    meeting_room = factory.SubFactory(MeetingRoomFactory)
    # creator = factory.SubFactory(UserFactory)
    starts_at = factory.LazyFunction(lambda: fake.future_datetime(end_date='+3d', tzinfo=UTC))
    ends_at = factory.LazyAttribute(
        lambda obj: fake.date_time_between(start_date=obj.starts_at, end_date=obj.starts_at + timedelta(hours=2), tzinfo=UTC)
    )

    @factory.post_generation
    def participants(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            self.participants.add(*extracted)
        else:
            users = UserFactory.create_batch(size=fake.random_int(min=1, max=5))
            self.participants.add(*users)