from django.core.management.base import BaseCommand
from booking.models import RoomType, Room

class Command(BaseCommand):
    help = 'Initializes room types and rooms in the database'

    def handle(self, *args, **options):
        # Удаляем существующие данные (опционально, для очистки)
        RoomType.objects.all().delete()
        Room.objects.all().delete()

        # Создание типов номеров
        self.stdout.write("Создание типов номеров...")
        types = [
            {'name': 'standard', 'description': 'Стандартный номер', 'base_price': 72000, 'capacity': 8},
            {'name': 'improved', 'description': 'Улучшенный номер', 'base_price': 85000, 'capacity': 8},
            {'name': 'lux', 'description': 'Номер люкс', 'base_price': 123000, 'capacity': 8},
            {'name': 'presidential', 'description': 'Президентский номер', 'base_price': 250000, 'capacity': 8},
        ]
        for room_type in types:
            obj, created = RoomType.objects.get_or_create(
                name=room_type['name'],
                defaults={
                    'description': room_type['description'],
                    'base_price': room_type['base_price'],
                    'capacity': room_type['capacity']
                }
            )
            self.stdout.write(f"Тип {room_type['name']} {'создан' if created else 'уже существует'}")

        # Создание номеров
        self.stdout.write("Создание номеров...")
        standard = RoomType.objects.get_or_create(name='standard')[0]
        improved = RoomType.objects.get_or_create(name='improved')[0]
        lux = RoomType.objects.get_or_create(name='lux')[0]
        presidential = RoomType.objects.get_or_create(name='presidential')[0]

        # Стандарт (100-150)
        self.stdout.write("Создание стандартных номеров (100-150)...")
        for i in range(100, 151):
            Room.objects.get_or_create(
                room_number=str(i),
                defaults={
                    'room_type': standard,
                    'price_per_night': standard.base_price,
                    'capacity': standard.capacity,
                    'description': 'Стандартный номер с базовыми удобствами.',
                    'is_available': True
                }
            )
        self.stdout.write("Стандартные номера созданы")

        # Улучшенный (200-235)
        self.stdout.write("Создание улучшенных номеров (200-235)...")
        for i in range(200, 236):
            Room.objects.get_or_create(
                room_number=str(i),
                defaults={
                    'room_type': improved,
                    'price_per_night': improved.base_price,
                    'capacity': improved.capacity,
                    'description': 'Улучшенный номер с дополнительными удобствами.',
                    'is_available': True
                }
            )
        self.stdout.write("Улучшенные номера созданы")

        # Люкс (300-320)
        self.stdout.write("Создание номеров люкс (300-320)...")
        for i in range(300, 321):
            Room.objects.get_or_create(
                room_number=str(i),
                defaults={
                    'room_type': lux,
                    'price_per_night': lux.base_price,
                    'capacity': lux.capacity,
                    'description': 'Роскошный номер с премиум-удобствами.',
                    'is_available': True
                }
            )
        self.stdout.write("Номера люкс созданы")

        # Президентский (400-405)
        self.stdout.write("Создание президентских номеров (400-405)...")
        for i in range(400, 406):
            Room.objects.get_or_create(
                room_number=str(i),
                defaults={
                    'room_type': presidential,
                    'price_per_night': presidential.base_price,
                    'capacity': presidential.capacity,
                    'description': 'Эксклюзивный президентский номер.',
                    'is_available': True
                }
            )
        self.stdout.write("Президентские номера созданы")
        self.stdout.write("Номера успешно созданы!")
        self.stdout.write("Типы номеров и номера успешно созданы!")