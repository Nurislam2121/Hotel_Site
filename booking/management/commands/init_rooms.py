from django.core.management.base import BaseCommand
from booking.models import RoomType, Room, RoomTypeImage, RoomImage

class Command(BaseCommand):
    help = 'Initializes room types, rooms, and their images in the database'

    def handle(self, *args, **options):
        RoomTypeImage.objects.all().delete()
        RoomImage.objects.all().delete()
        RoomType.objects.all().delete()
        Room.objects.all().delete()

        self.stdout.write("Создание типов номеров...")
        types = [
            {'name': 'standard', 'description': 'Стандартный номер', 'base_price': 72000, 'capacity': 8, 'image': 'room_types/standard.jpg'},
            {'name': 'improved', 'description': 'Улучшенный номер', 'base_price': 85000, 'capacity': 8, 'image': 'room_types/improved.jpg'},
            {'name': 'lux', 'description': 'Номер люкс', 'base_price': 123000, 'capacity': 8, 'image': 'room_types/lux.jpg'},
            {'name': 'presidential', 'description': 'Президентский номер', 'base_price': 250000, 'capacity': 8, 'image': 'room_types/presidential.jpg'},
        ]
        for room_type in types:
            obj, created = RoomType.objects.get_or_create(
                name=room_type['name'],
                defaults={
                    'description': room_type['description'],
                    'base_price': room_type['base_price'],
                    'capacity': room_type['capacity'],
                    'image': room_type['image']
                }
            )
            self.stdout.write(f"Тип {room_type['name']} {'создан' if created else 'уже существует'}")

        self.stdout.write("Создание изображений для типов номеров...")
        image_sets = {
            'standard': [
                {'path': 'room_type_images/standard1.jpg', 'caption': 'Стандартный номер - спальня'},
                {'path': 'room_type_images/standard2.jpg', 'caption': 'Стандартный номер - вид 2'},
                {'path': 'room_type_images/standard3.jpg', 'caption': 'Стандартный номер - душевая'},
                {'path': 'room_type_images/standard4.jpg', 'caption': 'Стандартный номер - туалет'},
                {'path': 'room_type_images/standard5.jpg', 'caption': 'Стандартный номер - вид 3'},
            ],
            'improved': [
                {'path': 'room_type_images/improved1.jpg', 'caption': 'Улучшенный номер - вид 1'},
                {'path': 'room_type_images/improved2.jpg', 'caption': 'Улучшенный номер - вид 2'},
                {'path': 'room_type_images/improved3.jpg', 'caption': 'Улучшенный номер - вид 3'},
                {'path': 'room_type_images/improved4.jpg', 'caption': 'Улучшенный номер - вид 4'},
                {'path': 'room_type_images/improved5.jpg', 'caption': 'Улучшенный номер - вид 5'},
                {'path': 'room_type_images/improved6.jpg', 'caption': 'Улучшенный номер - вид 6'},
                {'path': 'room_type_images/improved7.jpg', 'caption': 'Улучшенный номер - вид 7'},
            ],
            'lux': [
                {'path': 'room_type_images/lux.jpg', 'caption': 'Номер люкс - спальня'},
                {'path': 'room_type_images/lux1.jpg', 'caption': 'Номер люкс - вид 1'},
                {'path': 'room_type_images/lux2.jpg', 'caption': 'Номер люкс - вид 2'},
                {'path': 'room_type_images/lux3.jpg', 'caption': 'Номер люкс - вид 3'},
                {'path': 'room_type_images/lux4.jpg', 'caption': 'Номер люкс - душевая'},
                {'path': 'room_type_images/lux5.jpg', 'caption': 'Номер люкс - душевая'},
            ],
            'presidential': [
                {'path': 'room_type_images/presidential1.jpg', 'caption': 'Президентский номер - вид 1'},
                {'path': 'room_type_images/presidential2.jpg', 'caption': 'Президентский номер - вид 2'},
                {'path': 'room_type_images/presidential3.jpg', 'caption': 'Президентский номер - вид 3'},
                {'path': 'room_type_images/presidential4.jpg', 'caption': 'Президентский номер - вид 4'},
                {'path': 'room_type_images/presidential5.jpg', 'caption': 'Президентский номер - вид 5'},
                {'path': 'room_type_images/presidential6.jpg', 'caption': 'Президентский номер - вид 6'},
                {'path': 'room_type_images/presidential7.jpg', 'caption': 'Президентский номер - вид 7'},
                {'path': 'room_type_images/presidential8.jpg', 'caption': 'Президентский номер - вид 8'},
                {'path': 'room_type_images/presidential9.jpg', 'caption': 'Президентский номер - вид 9'},
                {'path': 'room_type_images/presidential10.jpg', 'caption': 'Президентский номер - вид 10'},
            ],
        }

        for room_type in RoomType.objects.all():
            for img in image_sets.get(room_type.name, []):
                RoomTypeImage.objects.get_or_create(
                    room_type=room_type,
                    image=img['path'],
                    caption=img['caption']
                )
            self.stdout.write(f"Изображения для {room_type.name} созданы")

        self.stdout.write("Создание номеров...")
        standard = RoomType.objects.get(name='standard')
        improved = RoomType.objects.get(name='improved')
        lux = RoomType.objects.get(name='lux')
        presidential = RoomType.objects.get(name='presidential')

        # Стандарт (100-150)
        self.stdout.write("Создание стандартных номеров (100-150)...")
        for i in range(100, 151):
            room, created = Room.objects.get_or_create(
                room_number=str(i),
                defaults={
                    'room_type': standard,
                    'price_per_night': standard.base_price,
                    'capacity': standard.capacity,
                    'description': 'Большой номер с лаконичным и стильным дизайном, позволяющий комфортно разместиться двоим гостям. В номере есть все необходимое для полноценного отдыха и для плодотворной работы. Площадь номера - 26 кв.м., количество номеров данной категории в отеле – 50.',
                    'is_available': True
                }
            )
            if created:
                for type_image in standard.type_images.all():
                    RoomImage.objects.get_or_create(
                        room=room,
                        image=type_image.image,
                        caption=type_image.caption
                    )
        self.stdout.write("Стандартные номера созданы")

        self.stdout.write("Создание улучшенных номеров (200-235)...")
        for i in range(200, 236):
            room, created = Room.objects.get_or_create(
                room_number=str(i),
                defaults={
                    'room_type': improved,
                    'price_per_night': improved.base_price,
                    'capacity': improved.capacity,
                    'description': 'Просторный номер с двумя раздельными кроватями удобны для проживания как во время деловых поездок, так и в рамках частных визитов. Площадь номера - 46 кв.м., количество номеров данной категории в отеле – 35.',
                    'is_available': True
                }
            )
            if created:
                for type_image in improved.type_images.all():
                    RoomImage.objects.get_or_create(
                        room=room,
                        image=type_image.image,
                        caption=type_image.caption
                    )
        self.stdout.write("Улучшенные номера созданы")

        self.stdout.write("Создание номеров люкс (300-320)...")
        for i in range(300, 321):
            room, created = Room.objects.get_or_create(
                room_number=str(i),
                defaults={
                    'room_type': lux,
                    'price_per_night': lux.base_price,
                    'capacity': lux.capacity,
                    'description': 'Роскошный и действительно широкий номер с уникальными дизайном для особенно требовательных гостей. Номер впечатляет современными удобствами и необычным европейским интерьером с безупречными цветовыми решениями и дизайнерской мебелью. Площадь номера - 56 кв.м., количество номеров данной категории в отеле – 20.',
                    'is_available': True
                }
            )
            if created:
                for type_image in lux.type_images.all():
                    RoomImage.objects.get_or_create(
                        room=room,
                        image=type_image.image,
                        caption=type_image.caption
                    )
        self.stdout.write("Номера люкс созданы")

        self.stdout.write("Создание президентских номеров (400-405)...")
        for i in range(400, 406):
            room, created = Room.objects.get_or_create(
                room_number=str(i),
                defaults={
                    'room_type': presidential,
                    'price_per_night': presidential.base_price,
                    'capacity': presidential.capacity,
                    'description': 'Теплая цветовая гамма, уникальная комплектация, дизайнерская мебель создают особенную атмосферу в номере. Стильная и просторная гостиная с мягким диваном, рабочей зоной, чайной станцией и мини-холодильником. Уютная спальня с комфортной кроватью размера king size, ванная комната и сауна. Площадь номера - 84 кв.м., количество номеров данной категории в отеле – 5.',
                    'is_available': True
                }
            )
            if created:
                for type_image in presidential.type_images.all():
                    RoomImage.objects.get_or_create(
                        room=room,
                        image=type_image.image,
                        caption=type_image.caption
                    )
        self.stdout.write("Президентские номера созданы")
        self.stdout.write("Номера успешно созданы!")
        self.stdout.write("Типы номеров, номера и изображения успешно созданы!")