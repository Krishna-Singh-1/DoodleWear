from django.core.management.base import BaseCommand
from django.core.files import File
from ecommerce.shop.models import Design
import os


class Command(BaseCommand):
    help = 'Update designs with actual image files'

    def handle(self, *args, **kwargs):
        # Define design image mappings
        design_images = {
            'Skull & Roses': 'skull_roses.svg',
            'Mountain Adventure': 'mountain.svg',
            'Geometric Pattern': 'geometric.svg',
            'Vintage Logo': 'vintage.svg',
            'Ocean Waves': 'ocean.svg',
            'Street Art': 'street_art.svg',
            'Minimalist Line': 'minimalist.svg',
            'Floral Bloom': 'floral.svg',
            'Galaxy Space': 'galaxy.svg',
            'Animal Kingdom': 'animal.svg',
            'Abstract Art': 'abstract.svg',
            'Sunset Vibes': 'sunset.svg',
            'Music Notes': 'music.svg',
            'Mandala Magic': 'mandala.svg',
            'Sports Champion': 'sports.svg',
        }

        media_path = 'media/designs/'
        updated_count = 0

        for design_name, image_file in design_images.items():
            try:
                design = Design.objects.get(name=design_name)
                image_path = os.path.join(media_path, image_file)
                
                if os.path.exists(image_path):
                    with open(image_path, 'rb') as f:
                        design.image.save(image_file, File(f), save=True)
                    updated_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'✓ Updated {design_name} with {image_file}')
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(f'⚠ Image file not found: {image_path}')
                    )
            except Design.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'✗ Design not found: {design_name}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'\n✅ Successfully updated {updated_count} designs with images!')
        )
