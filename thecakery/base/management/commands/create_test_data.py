from django.core.management.base import BaseCommand
from django.core.files import File
from django.contrib.auth.models import User
from django.utils import timezone
import os
from cakes.models import *
from party_accessories.models import *

class Command(BaseCommand):
    help = 'Create test data for TrendingType model'

    def handle(self, *args, **kwargs):
        # Creating test admin user
        admin_username = 'admin'
        admin_password = '1234'
        admin_email = 'admin@gmail.com'

        if not User.objects.filter(username=admin_username).exists():
            User.objects.create_superuser(
                username=admin_username,
                password=admin_password,
                email=admin_email
            )
            self.stdout.write(self.style.SUCCESS(f'Successfully created admin user: {admin_username}'))
        else:
            self.stdout.write(self.style.WARNING(f'Admin user with username "{admin_username}" already exists.'))

        # Creating test staff user
        staff_username = 'staff'
        staff_password = '1234'
        staff_email = 'staff@gmail.com'

        if not User.objects.filter(username=staff_username).exists():
            User.objects.create_user(
                username=staff_username,
                password=staff_password,
                email=staff_email,
                is_staff=True
            )
            self.stdout.write(self.style.SUCCESS(f'Successfully created staff user: {staff_username}'))
        else:
            self.stdout.write(self.style.WARNING(f'Staff user with username "{staff_username}" already exists.'))

        # Test data for CakeType
        cake_types = [
            {'name': 'Chocolate'},
            {'name': 'Vanilla'},
            {'name': 'Red Velvet'},
            {'name': 'Cheesecake'},
            {'name': 'Fruit'},
            {'name': 'Sponge'},
            {'name': 'Carrot'},
            {'name': 'Cheese'},
            {'name': 'Cupcake'},
        ]
        for cake_type in cake_types:
            CakeType.objects.get_or_create(name=cake_type['name'])

        # Test data for Category
        categories = [
            {'name': 'Birthday', 'description': 'Cakes specially designed for birthday celebrations.'},
            {'name': 'Wedding', 'description': 'Elegant and often multi-tiered cakes for weddings.'},
            {'name': 'Anniversary', 'description': 'Cakes for celebrating anniversaries.'},
            {'name': 'Graduation', 'description': 'Cakes to celebrate graduations.'},
            {'name': 'Baby Shower', 'description': 'Cakes for baby shower celebrations.'},
        ]
        for category in categories:
            # Create or get Category instance
            category_instance, created = Category.objects.get_or_create(
                name=category['name'],
                defaults={'description': category['description']}
            )
            self.stdout.write(self.style.SUCCESS('Category test data inserted successfully.'))

            # if created:
            #     # Add image if available
            #     image_filename = f"{category['name']}.jpg"  # Assuming images are in .jpg format
            #     image_path = os.path.join('static', 'image', image_filename)
                
            #     if os.path.exists(image_path):
            #         with open(image_path, 'rb') as image_file:
            #             category_instance.image.save(image_filename, File(image_file))
            #             category_instance.save()

        # Test data for Flavour
        flavours = [
            {'name': 'Chocolate', 'description': 'Rich and creamy chocolate flavor.', 'image': 'chocolate.jpg'},
            {'name': 'Vanilla', 'description': 'Classic and smooth vanilla flavor.', 'image': 'vanilla.jpg'},
            {'name': 'Strawberry', 'description': 'Fresh and fruity strawberry flavor.', 'image': 'strawberry.jpg'},
            {'name': 'Lemon', 'description': 'Zesty and tangy lemon flavor.', 'image': 'lemon.jpg'},
            {'name': 'Caramel', 'description': 'Sweet and buttery caramel flavor.', 'image': 'caramel.jpg'},
            {'name': 'Mint', 'description': 'Cool and refreshing mint flavor.', 'image': 'mint.jpg'},
        ]

        for flavour_data in flavours:
            flavour, created = Flavour.objects.get_or_create(name=flavour_data['name'], defaults={
                'description': flavour_data['description']
            })
            if created and flavour_data['image']:
                # Path to the static image file
                image_path = os.path.join('static', 'image', flavour_data['image'])
                # Use Django's File class to open and assign the image
                with open(image_path, 'rb') as img_file:
                    flavour.image.save(flavour_data['image'], File(img_file), save=True)

        # Test data for TrendingType
        trending_types = [
            {'name': 'Popular', 'description': 'Cakes that are currently highly popular among customers, often due to their unique flavors, presentation, or overall customer satisfaction.'},
            {'name': 'Hottest', 'description': 'The most sought-after cakes at the moment, often characterized by high demand and frequent purchases.'},
            {'name': 'Recent', 'description': 'Newly added cakes to the catalog, highlighting the latest additions for customers to explore fresh offerings.'},
            {'name': 'Top Rated', 'description': 'Cakes that have received the highest ratings from customers, often praised for their taste, quality, and presentation.'},
            {'name': 'Most Reviewed', 'description': 'Cakes with the most customer reviews, providing a wealth of feedback and insights from other customers.'},
            {'name': 'Most Viewed', 'description': 'Cakes that have attracted the most views on the website, indicating strong interest and curiosity from visitors.'},
            {'name': "Editor's Choice", 'description': 'Specially curated cakes recommended by the staff or culinary experts, selected for their exceptional quality or unique attributes.'},
            {'name': 'Limited Edition', 'description': 'Cakes available for a limited time or in limited quantities, often featuring seasonal ingredients or special designs.'},
            {'name': 'Best Seller', 'description': 'The top-selling cakes, favored by customers for their consistency in quality and flavor.'},
            {'name': 'Seasonal Favorites', 'description': 'Cakes that are particularly popular during specific seasons or holidays, often featuring seasonal ingredients or themes.'},
        ]
        for trend in trending_types:
            TrendingType.objects.get_or_create(name=trend['name'])

        # Create Cakes
        cake_data = [
            {
                'name': 'Chocolate Delight',
                'description': 'A delightful chocolate cake.',
                'cake_type': CakeType.objects.get(name='Chocolate'),
                'price': 25.99,
                'stock': 50,
                'category': Category.objects.get(name='Birthday'),
                'image': 'Chocolate Delight.jpg',
            },
            {
                'name': 'Vanilla Dream',
                'description': 'A smooth and creamy vanilla cake.',
                'cake_type': CakeType.objects.get(name='Vanilla'),
                'price': 20.99,
                'stock': 40,
                'category': Category.objects.get(name='Wedding'),
                'image': 'Vanilla Dream.jpg',
            },
            {
                'name': 'Red Velvet Bliss',
                'description': 'A rich and velvety red velvet cake.',
                'cake_type': CakeType.objects.get(name='Red Velvet'),
                'price': 30.99,
                'stock': 30,
                'category': Category.objects.get(name='Birthday'),
                'image': 'Red Velvet Bliss.jpg',
            },
            {
                'name': 'Fruit Fiesta',
                'description': 'A refreshing fruit cake with seasonal fruits.',
                'cake_type': CakeType.objects.get(name='Fruit'),
                'price': 35.99,
                'stock': 20,
                'category': Category.objects.get(name='Birthday'),
                'image': 'Fruit Fiesta.jpg',
            },
            {
                'name': 'Cheesecake Heaven',
                'description': 'A rich and creamy cheesecake.',
                'cake_type': CakeType.objects.get(name='Cheese'),
                'price': 40.99,
                'stock': 25,
                'category': Category.objects.get(name='Wedding'),
                'image': 'Cheesecake Heaven.jpg',
            },
            {
                'name': 'Lemon Zest',
                'description': 'A tangy lemon cake with a zesty flavor.',
                'cake_type': CakeType.objects.get(name='Fruit'),
                'price': 22.99,
                'stock': 35,
                'category': Category.objects.get(name='Birthday'),
                'image': 'Lemon Zest.jpg',
            },
            {
                'name': 'Berry Burst',
                'description': 'A cake bursting with fresh berries.',
                'cake_type': CakeType.objects.get(name='Fruit'),
                'price': 28.99,
                'stock': 45,
                'category': Category.objects.get(name='Birthday'),
                'image': 'Berry Burst.jpg',
            },
            {
                'name': 'Chocolate Fudge',
                'description': 'A rich and fudgy chocolate cake.',
                'cake_type': CakeType.objects.get(name='Chocolate'),
                'price': 32.99,
                'stock': 50,
                'category': Category.objects.get(name='Wedding'),
                'image': 'Chocolate Fudge.jpg',
            },
            {
                'name': 'Strawberry Shortcake',
                'description': 'A classic strawberry shortcake.',
                'cake_type': CakeType.objects.get(name='Vanilla'),
                'price': 27.99,
                'stock': 40,
                'category': Category.objects.get(name='Birthday'),
                'image': 'Strawberry Shortcake.jpg',
            },
            {
                'name': 'Caramel Delight',
                'description': 'A cake with a rich caramel flavor.',
                'cake_type': CakeType.objects.get(name='Chocolate'),
                'price': 29.99,
                'stock': 30,
                'category': Category.objects.get(name='Birthday'),
                'image': 'Caramel Delight.jpg',
            },
        ]
        for data in cake_data:
            # Create or get Cake instance
            cake, created = Cake.objects.get_or_create(
                name=data['name'],
                defaults={
                    'description': data['description'],
                    'cake_type': data['cake_type'],
                    'price': data['price'],
                    'stock': data['stock'],
                    'category': data['category'],
                }
            )

            if created:
                # Add image if available
                # Path to the static image file
                image_path = os.path.join('static', 'image', data['image'])
                if os.path.exists(image_path):
                    with open(image_path, 'rb') as image_file:
                        cake_image = CakeImage(
                            cake=cake,
                            image=File(image_file),
                            alt_text=f"Image of {cake.name}"
                        )
                        cake_image.save()

                # Associate flavours (for simplicity, associate all cakes with the same flavours)
                cake.flavours.add(*Flavour.objects.all())

        # Create Cake Sizes
        cake_size_data = [
            # Sizes for Chocolate Delight
            {
                'cake': Cake.objects.get(name='Chocolate Delight'),
                'size': 'Small',
                'additional_price': 0.00
            },
            {
                'cake': Cake.objects.get(name='Chocolate Delight'),
                'size': 'Medium',
                'additional_price': 5.00
            },
            {
                'cake': Cake.objects.get(name='Chocolate Delight'),
                'size': 'Large',
                'additional_price': 10.00
            },
            # Sizes for Vanilla Dream
            {
                'cake': Cake.objects.get(name='Vanilla Dream'),
                'size': 'Small',
                'additional_price': 0.00
            },
            {
                'cake': Cake.objects.get(name='Vanilla Dream'),
                'size': 'Medium',
                'additional_price': 4.50
            },
            {
                'cake': Cake.objects.get(name='Vanilla Dream'),
                'size': 'Large',
                'additional_price': 8.50
            },
            # Sizes for Red Velvet Bliss
            {
                'cake': Cake.objects.get(name='Red Velvet Bliss'),
                'size': 'Small',
                'additional_price': 0.00
            },
            {
                'cake': Cake.objects.get(name='Red Velvet Bliss'),
                'size': 'Medium',
                'additional_price': 6.00
            },
            {
                'cake': Cake.objects.get(name='Red Velvet Bliss'),
                'size': 'Large',
                'additional_price': 12.00
            },
            # Sizes for Fruit Fiesta
            {
                'cake': Cake.objects.get(name='Fruit Fiesta'),
                'size': 'Small',
                'additional_price': 0.00
            },
            {
                'cake': Cake.objects.get(name='Fruit Fiesta'),
                'size': 'Medium',
                'additional_price': 7.50
            },
            {
                'cake': Cake.objects.get(name='Fruit Fiesta'),
                'size': 'Large',
                'additional_price': 15.00
            },
            # Sizes for Cheesecake Heaven
            {
                'cake': Cake.objects.get(name='Cheesecake Heaven'),
                'size': 'Small',
                'additional_price': 0.00
            },
            {
                'cake': Cake.objects.get(name='Cheesecake Heaven'),
                'size': 'Medium',
                'additional_price': 10.00
            },
            {
                'cake': Cake.objects.get(name='Cheesecake Heaven'),
                'size': 'Large',
                'additional_price': 20.00
            },
            # Sizes for Lemon Zest
            {
                'cake': Cake.objects.get(name='Lemon Zest'),
                'size': 'Small',
                'additional_price': 0.00
            },
            {
                'cake': Cake.objects.get(name='Lemon Zest'),
                'size': 'Medium',
                'additional_price': 5.50
            },
            {
                'cake': Cake.objects.get(name='Lemon Zest'),
                'size': 'Large',
                'additional_price': 11.00
            },
            # Sizes for Berry Burst
            {
                'cake': Cake.objects.get(name='Berry Burst'),
                'size': 'Small',
                'additional_price': 0.00
            },
            {
                'cake': Cake.objects.get(name='Berry Burst'),
                'size': 'Medium',
                'additional_price': 6.50
            },
            {
                'cake': Cake.objects.get(name='Berry Burst'),
                'size': 'Large',
                'additional_price': 13.00
            },
            # Sizes for Chocolate Fudge
            {
                'cake': Cake.objects.get(name='Chocolate Fudge'),
                'size': 'Small',
                'additional_price': 0.00
            },
            {
                'cake': Cake.objects.get(name='Chocolate Fudge'),
                'size': 'Medium',
                'additional_price': 6.00
            },
            {
                'cake': Cake.objects.get(name='Chocolate Fudge'),
                'size': 'Large',
                'additional_price': 12.00
            },
            # Sizes for Strawberry Shortcake
            {
                'cake': Cake.objects.get(name='Strawberry Shortcake'),
                'size': 'Small',
                'additional_price': 0.00
            },
            {
                'cake': Cake.objects.get(name='Strawberry Shortcake'),
                'size': 'Medium',
                'additional_price': 5.00
            },
            {
                'cake': Cake.objects.get(name='Strawberry Shortcake'),
                'size': 'Large',
                'additional_price': 10.00
            },
            # Sizes for Caramel Delight
            {
                'cake': Cake.objects.get(name='Caramel Delight'),
                'size': 'Small',
                'additional_price': 0.00
            },
            {
                'cake': Cake.objects.get(name='Caramel Delight'),
                'size': 'Medium',
                'additional_price': 7.00
            },
            {
                'cake': Cake.objects.get(name='Caramel Delight'),
                'size': 'Large',
                'additional_price': 14.00
            },
        ]
        for data in cake_size_data:
            CakeSize.objects.get_or_create(**data)

        # Create Trending Cakes
        trending_cake_data = [
            # Popular Cakes
            {
                'cake': Cake.objects.get(name='Chocolate Delight'),
                'trend_type': TrendingType.objects.get(name='Popular'),
                'trend_score': 95,
                'description': 'A perennial favorite, loved for its rich chocolate flavor and moist texture.'
            },
            {
                'cake': Cake.objects.get(name='Red Velvet Bliss'),
                'trend_type': TrendingType.objects.get(name='Popular'),
                'trend_score': 90,
                'description': 'Known for its vibrant color and creamy frosting, a top choice for celebrations.'
            },
            # Hottest Cakes
            {
                'cake': Cake.objects.get(name='Vanilla Dream'),
                'trend_type': TrendingType.objects.get(name='Hottest'),
                'trend_score': 85,
                'description': 'Recently launched, this cake has quickly become a bestseller with its classic vanilla flavor.'
            },
            {
                'cake': Cake.objects.get(name='Berry Burst'),
                'trend_type': TrendingType.objects.get(name='Hottest'),
                'trend_score': 80,
                'description': 'Packed with fresh berries, this cake is perfect for summer and loved by all ages.'
            },
            # Most Recent Cakes
            {
                'cake': Cake.objects.get(name='Fruit Fiesta'),
                'trend_type': TrendingType.objects.get(name='Recent'),
                'trend_score': 75,
                'description': 'A new addition to our lineup, featuring a medley of tropical fruits for a refreshing taste.'
            },
            {
                'cake': Cake.objects.get(name='Cheesecake Heaven'),
                'trend_type': TrendingType.objects.get(name='Recent'),
                'trend_score': 70,
                'description': 'A modern twist on a classic, combining traditional cheesecake with innovative flavors.'
            },
            # Top Rated Cakes
            {
                'cake': Cake.objects.get(name='Lemon Zest'),
                'trend_type': TrendingType.objects.get(name='Top Rated'),
                'trend_score': 100,
                'description': 'Highly rated for its zesty flavor and light, fluffy texture.'
            },
            {
                'cake': Cake.objects.get(name='Strawberry Shortcake'),
                'trend_type': TrendingType.objects.get(name='Top Rated'),
                'trend_score': 98,
                'description': 'Customers rave about its fresh strawberries and whipped cream topping.'
            },
            # Most Reviewed Cakes
            {
                'cake': Cake.objects.get(name='Chocolate Fudge'),
                'trend_type': TrendingType.objects.get(name='Most Reviewed'),
                'trend_score': 92,
                'description': 'Garnered the most reviews for its decadent chocolate fudge layers.'
            },
            {
                'cake': Cake.objects.get(name='Caramel Delight'),
                'trend_type': TrendingType.objects.get(name='Most Reviewed'),
                'trend_score': 89,
                'description': 'Loved for its rich caramel flavor, this cake has been extensively reviewed by our customers.'
            },
        ]
        for data in trending_cake_data:
            TrendingCake.objects.get_or_create(**data)

        # Create Party Accessories
        accessory_data = [
            {
                'name': 'Birthday Balloons',
                'description': 'Colorful balloons perfect for any birthday celebration.',
                'price': 9.99,
                'stock': 100,
                'image': 'balloon.jpg',
            },
            {
                'name': 'Party Hats',
                'description': 'Fun and festive party hats for guests.',
                'price': 5.99,
                'stock': 200,
                'image': 'hat.webp',
            },
            {
                'name': 'Confetti Cannon',
                'description': 'A burst of colorful confetti to light up your party.',
                'price': 12.99,
                'stock': 50,
                'image': 'cannon.jpg',
            },
            {
                'name': 'Streamers',
                'description': 'Decorative streamers in various colors.',
                'price': 7.99,
                'stock': 150,
                'image': 'streamers.jpg',
            },
            {
                'name': 'Disposable Cups',
                'description': 'Colorful disposable cups, perfect for serving drinks.',
                'price': 4.99,
                'stock': 300,
                'image': 'cup.jpg',
            },
            # Add more accessories as needed
        ]
        
        for data in accessory_data:
            accessory, created = PartyAccessory.objects.get_or_create(
                name=data['name'],
                description=data['description'],
                price=data['price'],
                stock=data['stock'],
                created_at=timezone.now(),
                updated_at=timezone.now()
            )

            if created:
                # Add image if available
                # Path to the static image file
                image_path = os.path.join('static', 'image', data['image'])
                if os.path.exists(image_path):
                    with open(image_path, 'rb') as image_file:
                        accessory_image = PartyAccessoryImage(
                            accessory=accessory,
                            image=File(image_file),
                            alt_text=f"Image of {accessory.name}"
                        )
                        accessory_image.save()
        
        self.stdout.write(self.style.SUCCESS('Test data inserted successfully.'))
