from django.core.management.base import BaseCommand
from ecommerce.shop.models import Category, Product
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Add sample categories and products for testing'

    def handle(self, *args, **options):
        self.stdout.write('Adding sample data...')
        
        # Create categories
        categories_data = [
            {'name': 'T-Shirts', 'description': 'Comfortable cotton t-shirts'},
            {'name': 'Hoodies', 'description': 'Warm and cozy hoodies'},
            {'name': 'Tank Tops', 'description': 'Sleeveless tank tops'},
            {'name': 'Long Sleeve', 'description': 'Long sleeve shirts'},
        ]
        
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'slug': slugify(cat_data['name']),
                    'description': cat_data['description']
                }
            )
            if created:
                self.stdout.write(f'Created category: {category.name}')
        
        # Create products
        products_data = [
            # T-Shirts
            {
                'name': 'Classic Cotton T-Shirt',
                'category': 'T-Shirts',
                'description': 'A classic cotton t-shirt perfect for everyday wear. Made from 100% premium cotton.',
                'price': 899.00,
                'available_sizes': 's,m,l,xl',
                'available_colors': 'black,white,blue,red',
                'stock_quantity': 50
            },
            {
                'name': 'Premium V-Neck T-Shirt',
                'category': 'T-Shirts', 
                'description': 'Stylish v-neck t-shirt with a modern fit. Soft and comfortable fabric.',
                'price': 1199.00,
                'available_sizes': 's,m,l,xl,xxl',
                'available_colors': 'black,white,gray,navy',
                'stock_quantity': 30
            },
            {
                'name': 'Graphic Print T-Shirt',
                'category': 'T-Shirts',
                'description': 'Trendy graphic print t-shirt with unique designs. Express your style.',
                'price': 1299.00,
                'available_sizes': 's,m,l,xl',
                'available_colors': 'black,white,blue',
                'stock_quantity': 25
            },
            
            # Hoodies
            {
                'name': 'Classic Pullover Hoodie',
                'category': 'Hoodies',
                'description': 'Warm and comfortable pullover hoodie. Perfect for casual wear and layering.',
                'price': 2499.00,
                'available_sizes': 's,m,l,xl,xxl',
                'available_colors': 'black,gray,navy,red',
                'stock_quantity': 20
            },
            {
                'name': 'Zip-Up Hoodie',
                'category': 'Hoodies',
                'description': 'Convenient zip-up hoodie with front pockets. Great for outdoor activities.',
                'price': 2799.00,
                'available_sizes': 'm,l,xl,xxl',
                'available_colors': 'black,gray,blue',
                'stock_quantity': 15
            },
            
            # Tank Tops
            {
                'name': 'Athletic Tank Top',
                'category': 'Tank Tops',
                'description': 'Lightweight athletic tank top perfect for workouts and summer wear.',
                'price': 699.00,
                'available_sizes': 's,m,l,xl',
                'available_colors': 'black,white,gray,blue',
                'stock_quantity': 40
            },
            {
                'name': 'Casual Cotton Tank',
                'category': 'Tank Tops',
                'description': 'Soft cotton tank top for everyday comfort. Breathable and stylish.',
                'price': 799.00,
                'available_sizes': 's,m,l,xl',
                'available_colors': 'white,black,pink,yellow',
                'stock_quantity': 35
            },
            
            # Long Sleeve
            {
                'name': 'Long Sleeve Basic Tee',
                'category': 'Long Sleeve',
                'description': 'Essential long sleeve t-shirt. Perfect for layering or wearing alone.',
                'price': 1399.00,
                'available_sizes': 's,m,l,xl,xxl',
                'available_colors': 'black,white,gray,navy',
                'stock_quantity': 25
            },
            {
                'name': 'Thermal Long Sleeve',
                'category': 'Long Sleeve',
                'description': 'Thermal long sleeve shirt for extra warmth. Great for cold weather.',
                'price': 1699.00,
                'available_sizes': 'm,l,xl,xxl',
                'available_colors': 'black,gray,navy',
                'stock_quantity': 20
            },
        ]
        
        for prod_data in products_data:
            category = Category.objects.get(name=prod_data['category'])
            product, created = Product.objects.get_or_create(
                name=prod_data['name'],
                defaults={
                    'slug': slugify(prod_data['name']),
                    'category': category,
                    'description': prod_data['description'],
                    'price': prod_data['price'],
                    'available_sizes': prod_data['available_sizes'],
                    'available_colors': prod_data['available_colors'],
                    'stock_quantity': prod_data['stock_quantity'],
                    'is_active': True,
                    'is_featured': True if 'Premium' in prod_data['name'] or 'Classic' in prod_data['name'] else False
                }
            )
            if created:
                self.stdout.write(f'Created product: {product.name}')
        
        self.stdout.write(self.style.SUCCESS('Sample data added successfully!'))