import random

from django.core.management import call_command
from django.core.management.base import BaseCommand
from authentication.models import User
from faker import Faker

from booking.models import Office
from booking.tests.factories import OfficeFactory, MeetingRoomFactory, BookingFactory

fake = Faker('ru_RU')


MEETING_ROOM_NAMES = ['1. Потанцуем', '1. Чай', '1. Кофе', '7. Небо', '7. Одного не ждут', '7. Чудес', '7. Пятниц', '7. Холмов', '7. Гномов', '7. Отмерь-Отрежь', '6. Шива', '3. Мушкетёра', '2. Стула']

class Command(BaseCommand):
    help = 'Заполняет базу данных'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count', type=int, default=10, help='Количество создаваемых пользователей'
        )

    def handle(self, *args, **kwargs):
        call_command('flush', '--noinput')
        count = kwargs['count']
        User.objects.create_superuser('admin@gmail.com', '1111', name='Арапов Дмитрий')

        users = []
        for _ in range(count):
            name = fake.name()
            email = fake.email()
            password = '12345678'


            user = User.objects.create_user(
                email=email,
                name=name,
                password=password,
            )
            users.append(user)

            self.stdout.write(f"Создан пользователь: {user.name} ({user.email})")

        offices = [
            OfficeFactory.create(name='БЦ Морозов'),
            OfficeFactory.create(name='Око'),
        ]


        rooms = [MeetingRoomFactory.create(name=meeting_room_name, office=random.choice(offices)) for meeting_room_name in MEETING_ROOM_NAMES]

        for _ in range(100):
            BookingFactory.create(
                meeting_room=random.choice(rooms),
                creator=random.choice(users),
                participants=random.sample(users, 2)
            )




        self.stdout.write(self.style.SUCCESS(f'Успешно создано {count} пользователей!'))
