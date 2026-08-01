from django.core.management.base import BaseCommand
from ecommerce.shop.models import Design


class Command(BaseCommand):
    help = 'Add sample designs to the database'

    def handle(self, *args, **kwargs):
        designs_data = [
            {
                'name': 'Skull & Roses',
                'description': 'Bold skull design with colorful roses',
            },
            {
                'name': 'Mountain Adventure',
                'description': 'Scenic mountain landscape with pine trees',
            },
            {
                'name': 'Geometric Pattern',
                'description': 'Modern abstract geometric shapes',
            },
            {
                'name': 'Vintage Logo',
                'description': 'Retro-style typography design',
            },
            {
                'name': 'Ocean Waves',
                'description': 'Beautiful ocean wave illustration',
            },
            {
                'name': 'Street Art',
                'description': 'Urban graffiti style artwork',
            },
            {
                'name': 'Minimalist Line',
                'description': 'Simple elegant line art',
            },
            {
                'name': 'Floral Bloom',
                'description': 'Vibrant flower arrangement design',
            },
            {
                'name': 'Galaxy Space',
                'description': 'Cosmic stars and planets',
            },
            {
                'name': 'Animal Kingdom',
                'description': 'Majestic wildlife illustration',
            },
            {
                'name': 'Abstract Art',
                'description': 'Colorful abstract expressionism',
            },
            {
                'name': 'Sunset Vibes',
                'description': 'Tropical sunset with palm trees',
            },
            {
                'name': 'Music Notes',
                'description': 'Musical instruments and notes',
            },
            {
                'name': 'Mandala Magic',
                'description': 'Intricate mandala pattern',
            },
            {
                'name': 'Sports Champion',
                'description': 'Athletic sports themed design',
            },
        ]

        created_count = 0
        for design_data in designs_data:
            design, created = Design.objects.get_or_create(
                name=design_data['name'],
                defaults={
                    'description': design_data['description'],
                    'is_active': True,
                }
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Created design: {design.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'- Design already exists: {design.name}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'\n✅ Successfully added {created_count} new designs!')
        )
        self.stdout.write(
            self.style.SUCCESS(f'Total designs in database: {Design.objects.count()}')
        )
