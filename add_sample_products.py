#!/usr/bin/env python
import os
import sys
import django

# Setup Django
sys.path.append('C:\\Users\\KRISHNA SINGH\\OneDrive\\Desktop\\DoodleWear\\ecommerce')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from ecommerce.shop.models import Category, Product

def create_sample_data():
    print("Creating sample categories and products...")
    
    # Create categories
    categories_data = [
        {'name': 'T-Shirts', 'slug': 't-shirts', 'description': 'Comfortable and stylish t-shirts for everyday wear'},
        {'name': 'Hoodies', 'slug': 'hoodies', 'description': 'Warm and cozy hoodies for casual style'},
        {'name': 'Tank Tops', 'slug': 'tank-tops', 'description': 'Sleeveless tops perfect for summer'},
        {'name': 'Long Sleeves', 'slug': 'long-sleeves', 'description': 'Long sleeve shirts for cooler days'},
    ]
    
    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(
            slug=cat_data['slug'],
            defaults=cat_data
        )
        if created:
            print(f"Created category: {category.name}")
    
    # Create products
    products_data = [
        # T-Shirts
        {
            'name': 'Classic Cotton T-Shirt',
            'slug': 'classic-cotton-tshirt',
            'category': 't-shirts',
            'description': 'A comfortable 100% cotton t-shirt perfect for everyday wear. Soft, breathable, and available in multiple colors.',
            'price': 25.00,
            'available_sizes': 'xs,s,m,l,xl,xxl',
            'available_colors': 'black,white,red,blue,green',
            'stock_quantity': 50,
            'is_featured': True
        },
        {
            'name': 'Premium Graphic T-Shirt',
            'slug': 'premium-graphic-tshirt',
            'category': 't-shirts',
            'description': 'High-quality graphic t-shirt with unique designs. Made from soft cotton blend for ultimate comfort.',
            'price': 30.00,
            'available_sizes': 's,m,l,xl,xxl',
            'available_colors': 'black,white,gray,navy',
            'stock_quantity': 35,
            'is_featured': False
        },
        {
            'name': 'Vintage Style T-Shirt',
            'slug': 'vintage-style-tshirt',
            'category': 't-shirts',
            'description': 'Retro-inspired t-shirt with a vintage wash and classic fit. Perfect for a timeless look.',
            'price': 28.00,
            'available_sizes': 'xs,s,m,l,xl',
            'available_colors': 'black,white,red,purple',
            'stock_quantity': 25,
        },
        
        # Hoodies
        {
            'name': 'Cozy Pullover Hoodie',
            'slug': 'cozy-pullover-hoodie',
            'category': 'hoodies',
            'description': 'Ultra-soft pullover hoodie with a spacious kangaroo pocket. Perfect for chilly days and relaxed vibes.',
            'price': 55.00,
            'available_sizes': 's,m,l,xl,xxl',
            'available_colors': 'black,gray,navy,red',
            'stock_quantity': 30,
            'is_featured': True
        },
        {
            'name': 'Zip-Up Hoodie',
            'slug': 'zip-up-hoodie',
            'category': 'hoodies',
            'description': 'Versatile zip-up hoodie with adjustable hood and side pockets. Great for layering or wearing alone.',
            'price': 60.00,
            'available_sizes': 'm,l,xl,xxl',
            'available_colors': 'black,gray,blue',
            'stock_quantity': 20,
        },
        
        # Tank Tops
        {
            'name': 'Athletic Tank Top',
            'slug': 'athletic-tank-top',
            'category': 'tank-tops',
            'description': 'Lightweight and breathable tank top designed for workouts and active lifestyle. Moisture-wicking fabric.',
            'price': 20.00,
            'available_sizes': 'xs,s,m,l,xl',
            'available_colors': 'black,white,gray,blue',
            'stock_quantity': 40,
            'is_featured': True
        },
        {
            'name': 'Summer Casual Tank',
            'slug': 'summer-casual-tank',
            'category': 'tank-tops',
            'description': 'Relaxed fit tank top perfect for summer days. Soft cotton blend with a comfortable loose fit.',
            'price': 18.00,
            'available_sizes': 'xs,s,m,l',
            'available_colors': 'white,pink,yellow,green',
            'stock_quantity': 35,
        },
        
        # Long Sleeves
        {
            'name': 'Long Sleeve Basic Tee',
            'slug': 'long-sleeve-basic-tee',
            'category': 'long-sleeves',
            'description': 'Essential long sleeve t-shirt made from premium cotton. Perfect for layering or wearing on its own.',
            'price': 32.00,
            'available_sizes': 'xs,s,m,l,xl,xxl',
            'available_colors': 'black,white,gray,navy',
            'stock_quantity': 45,
            'is_featured': True
        },
        {
            'name': 'Thermal Long Sleeve',
            'slug': 'thermal-long-sleeve',
            'category': 'long-sleeves',
            'description': 'Warm thermal long sleeve perfect for cold weather. Ribbed texture and comfortable fit.',
            'price': 38.00,
            'available_sizes': 's,m,l,xl',
            'available_colors': 'black,gray,red',
            'stock_quantity': 25,
        },
    ]
    
    for product_data in products_data:
        category = Category.objects.get(slug=product_data['category'])
        product_data['category'] = category
        
        product, created = Product.objects.get_or_create(
            slug=product_data['slug'],
            defaults=product_data
        )
        if created:
            print(f"Created product: {product.name} - ${product.price}")
    
    print(f"\nSample data created successfully!")
    print(f"Categories: {Category.objects.count()}")
    print(f"Products: {Product.objects.count()}")
    print("\nYou can now visit /shop/ to see the products!")

if __name__ == '__main__':
    create_sample_data()