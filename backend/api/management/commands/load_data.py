"""
Django Management Command to load Market Prices, Mentors, and Schemes data
"""
from django.core.management.base import BaseCommand
from api.models import MarketPrice, Mentor, Scheme
from decimal import Decimal


class Command(BaseCommand):
    help = 'Load Market Prices, Mentors, and Schemes data'

    def handle(self, *args, **options):
        self.stdout.write('Loading Market Prices...')
        self.load_market_prices()
        
        self.stdout.write('Loading Mentors...')
        self.load_mentors()
        
        self.stdout.write('Loading Schemes...')
        self.load_schemes()
        
        self.stdout.write(self.style.SUCCESS('✅ All data loaded successfully!'))

    def load_market_prices(self):
        """Load commodity prices from local mandis"""
        market_data = [
            # Tamil Nadu Mandis - Rice
            {'commodity_name': 'Rice', 'market_location': 'Coimbatore Mandi', 'price': Decimal('42.50'), 'unit': 'kg', 'market_date': '2026-03-25'},
            {'commodity_name': 'Rice', 'market_location': 'Chennai Mandi', 'price': Decimal('40.00'), 'unit': 'kg', 'market_date': '2026-03-25'},
            {'commodity_name': 'Rice', 'market_location': 'Madurai Mandi', 'price': Decimal('41.75'), 'unit': 'kg', 'market_date': '2026-03-25'},
            
            # Tamil Nadu Mandis - Vegetables
            {'commodity_name': 'Tomato', 'market_location': 'Coimbatore Mandi', 'price': Decimal('35.00'), 'unit': 'kg', 'market_date': '2026-03-25'},
            {'commodity_name': 'Onion', 'market_location': 'Chennai Mandi', 'price': Decimal('28.50'), 'unit': 'kg', 'market_date': '2026-03-25'},
            {'commodity_name': 'Potato', 'market_location': 'Madurai Mandi', 'price': Decimal('18.00'), 'unit': 'kg', 'market_date': '2026-03-25'},
            
            # Spices
            {'commodity_name': 'Turmeric Powder', 'market_location': 'Erode Spice Mandi', 'price': Decimal('95.00'), 'unit': 'kg', 'market_date': '2026-03-25'},
            {'commodity_name': 'Chili Powder', 'market_location': 'Guntur Mandi', 'price': Decimal('125.50'), 'unit': 'kg', 'market_date': '2026-03-25'},
            {'commodity_name': 'Coriander Powder', 'market_location': 'Rajasthan Mandi', 'price': Decimal('85.00'), 'unit': 'kg', 'market_date': '2026-03-25'},
            
            # Dairy
            {'commodity_name': 'Milk', 'market_location': 'Chennai Dairy', 'price': Decimal('45.00'), 'unit': 'litre', 'market_date': '2026-03-25'},
            {'commodity_name': 'Ghee', 'market_location': 'Tamil Nadu Dairy', 'price': Decimal('580.00'), 'unit': 'kg', 'market_date': '2026-03-25'},
            
            # Fruits
            {'commodity_name': 'Banana', 'market_location': 'Chennai Fruit Market', 'price': Decimal('32.00'), 'unit': 'kg', 'market_date': '2026-03-25'},
            {'commodity_name': 'Mango', 'market_location': 'Madurai Fruit Market', 'price': Decimal('65.00'), 'unit': 'kg', 'market_date': '2026-03-25'},
            {'commodity_name': 'Coconut', 'market_location': 'Kerala Mandi', 'price': Decimal('15.00'), 'unit': 'piece', 'market_date': '2026-03-25'},
        ]
        
        for data in market_data:
            MarketPrice.objects.get_or_create(
                commodity_name=data['commodity_name'],
                market_location=data['market_location'],
                defaults={
                    'price': data['price'],
                    'unit': data['unit'],
                    'market_date': data['market_date'],
                }
            )
        self.stdout.write(self.style.SUCCESS(f'  ✓ Loaded {len(market_data)} market prices'))

    def load_mentors(self):
        """Load mentor profiles"""
        mentor_data = [
            {
                'name': 'Priya Sharma',
                'specialization': 'Dairy Business Expert',
                'phone': '+91-9876543210',
                'email': 'priya.dairy@example.com',
                'bio': 'Dairy business expert with 15 years experience in milk production and dairy product marketing.',
                'languages_spoken': 'Hindi, English',
                'experience_years': 15,
            },
            {
                'name': 'Anita Verma',
                'specialization': 'Organic Agriculture',
                'phone': '+91-9876543211',
                'email': 'anita.agri@example.com',
                'bio': 'Agricultural consultant for organic farming and sustainable practices.',
                'languages_spoken': 'Hindi, English',
                'experience_years': 12,
            },
            {
                'name': 'Lakshmi Raj',
                'specialization': 'Textile & Handicraft',
                'phone': '+91-9876543212',
                'email': 'lakshmi.craft@example.com',
                'bio': 'Textile and handicraft business mentor with expertise in traditional crafts.',
                'languages_spoken': 'Tamil, English',
                'experience_years': 18,
            },
            {
                'name': 'Meena Singh',
                'specialization': 'Food Business',
                'phone': '+91-9876543213',
                'email': 'meena.food@example.com',
                'bio': 'Food business and kitchen startup expert with FSSAI certification expertise.',
                'languages_spoken': 'English, Hindi',
                'experience_years': 10,
            },
            {
                'name': 'Kavya Nair',
                'specialization': 'Retail & E-commerce',
                'phone': '+91-9876543214',
                'email': 'kavya.retail@example.com',
                'bio': 'Retail business and e-commerce consultant helping entrepreneurs go digital.',
                'languages_spoken': 'Tamil, English, Malayalam',
                'experience_years': 8,
            },
            {
                'name': 'Sneha Gupta',
                'specialization': 'Financial Planning',
                'phone': '+91-9876543215',
                'email': 'sneha.finance@example.com',
                'bio': 'Financial planning and business loan guidance expert.',
                'languages_spoken': 'Hindi, English',
                'experience_years': 14,
            },
        ]
        
        for data in mentor_data:
            Mentor.objects.get_or_create(
                email=data['email'],
                defaults={
                    'name': data['name'],
                    'specialization': data['specialization'],
                    'expertise': data['specialization'],
                    'phone': data['phone'],
                    'bio': data['bio'],
                    'languages_spoken': data['languages_spoken'],
                    'experience_years': data['experience_years'],
                    'is_active': True,
                    'rating': Decimal('4.5'),
                }
            )
        self.stdout.write(self.style.SUCCESS(f'  ✓ Loaded {len(mentor_data)} mentors'))

    def load_schemes(self):
        """Load government schemes for women entrepreneurs"""
        scheme_data = [
            {
                'name': 'Pradhan Mantri Mahila Shakti Kendra',
                'description': 'Women empowerment scheme with financial assistance up to ₹3 lakhs for starting small businesses.',
                'eligibility': 'Women aged 18-55 years, preferably from rural areas',
                'benefits': '₹50,000 to ₹3,00,000 loan assistance with low interest rates',
                'agency': 'Ministry of Women and Child Development',
                'url': 'https://pmmy.gov.in',
                'category': 'loan',
                'max_amount': Decimal('300000'),
            },
            {
                'name': 'Mahila Udyam Nidhi',
                'description': 'Special fund for women entrepreneurs with low interest rates and flexible repayment.',
                'eligibility': 'Female entrepreneurs with business experience',
                'benefits': 'Concessional credit up to ₹10 lakhs with 4% interest subsidies',
                'agency': 'SIDBI',
                'url': 'https://www.sidbi.in',
                'category': 'loan',
                'max_amount': Decimal('1000000'),
            },
            {
                'name': 'Bhamashah Card',
                'description': 'Rajasthan-based scheme for women financial inclusion and business support.',
                'eligibility': 'Women residents of Rajasthan',
                'benefits': 'Direct bank account opening and subsidized business loans',
                'agency': 'Rajasthan State Government',
                'url': 'https://www.bhamashah.rajasthan.gov.in',
                'category': 'loan',
            },
            {
                'name': 'Tamil Nadu Business Women Scheme',
                'description': 'Loan scheme for women-owned small businesses in Tamil Nadu.',
                'eligibility': 'Women entrepreneurs from Tamil Nadu with business plan',
                'benefits': 'Subsidized loans up to ₹25 lakhs for business setup',
                'agency': 'Tamil Nadu MSME Department',
                'url': 'https://www.tnmsme.in',
                'category': 'loan',
                'max_amount': Decimal('2500000'),
            },
            {
                'name': 'Haryana Antyodaya Parivar Uthhan Yojana',
                'description': 'Haryana scheme for micro-business support and skill development.',
                'eligibility': 'BPL and APL families in Haryana',
                'benefits': 'Skill training and ₹2 lakh financial assistance',
                'agency': 'Haryana State Government',
                'url': 'https://www.haryana.gov.in',
                'category': 'training',
                'max_amount': Decimal('200000'),
            },
            {
                'name': 'Kerala Women Entrepreneurs Development Scheme',
                'description': 'Comprehensive support for women entrepreneurs in Kerala including subsidy.',
                'eligibility': 'Women entrepreneurs from Kerala',
                'benefits': 'Subsidy up to 25% of project cost and training support',
                'agency': 'Kerala State Government',
                'url': 'https://www.ksindustries.gov.in',
                'category': 'subsidy',
            },
            {
                'name': 'Stand Up India',
                'description': 'Centrally sponsored scheme for SC/ST/Women entrepreneurs to start new enterprises.',
                'eligibility': 'Women SC/ST individuals wanting to start business',
                'benefits': 'Loans between ₹10 - ₹1 crore at special interest rates',
                'agency': 'Ministry of Micro, Small and Medium Enterprises',
                'url': 'https://standupmitra.in',
                'category': 'loan',
                'max_amount': Decimal('10000000'),
            },
            {
                'name': 'One District One Product (ODOP)',
                'description': 'Government scheme to promote regional handicrafts and traditional products.',
                'eligibility': 'Women artisans and craftspeople across all regions',
                'benefits': 'Marketing support, training, and export assistance',
                'agency': 'Ministry of Commerce',
                'url': 'https://odopexports.gov.in',
                'category': 'market_linkage',
            },
        ]
        
        for data in scheme_data:
            Scheme.objects.get_or_create(
                name=data['name'],
                defaults={
                    'description': data['description'],
                    'eligibility': data['eligibility'],
                    'benefits': data['benefits'],
                    'agency': data['agency'],
                    'url': data['url'],
                    'category': data['category'],
                    'status': 'active',
                    'max_amount': data.get('max_amount'),
                }
            )
        self.stdout.write(self.style.SUCCESS(f'  ✓ Loaded {len(scheme_data)} schemes'))
