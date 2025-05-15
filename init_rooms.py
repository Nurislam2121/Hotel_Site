from django.contrib.auth.models import User
from booking.models import RoomType, Room

# Создание типов номеров
def create_room_types():
    types = [
        {'name': 'standard', 'description': 'Стандартный номер', 'base_price': 72000, 'capacity': 8},
        {'name': 'improved', 'description': 'Улучшенный номер', 'base_price': 85000, 'capacity': 8},
        {'name': 'lux', 'description': 'Номер люкс', 'base_price': 123000, 'capacity': 8},
        {'name': 'presidential', 'description': 'Президентский номер', 'base_price': 250000, 'capacity': 8},
    ]
    for room_type in types:
        RoomType.objects.get_or_create(
            name=room_type['name'],
            defaults={
                'description': room_type['description'],
                'base_price': room_type['base_price'],
                'capacity': room_type['capacity']
            }
        )

# Создание номеров
def create_rooms():
    try:
        # Получаем или создаем типы номеров
        standard = RoomType.objects.get_or_create(name='standard')[0]
        improved = RoomType.objects.get_or_create(name='improved')[0]
        lux = RoomType.objects.get_or_create(name='lux')[0]
        presidential = RoomType.objects.get_or_create(name='presidential')[0]

        # Стандарт (100-150)
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

        # Улучшенный (200-235)
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

        # Люкс (300-320)
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

        # Президентский (400-405)
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
        print("Номера успешно созданы!")
    except Exception as e:
        print(f"Ошибка при создании номеров: {e}")

if __name__ == "__main__":
    create_room_types()
    create_rooms()
    print("Типы номеров и номера успешно созданы!")