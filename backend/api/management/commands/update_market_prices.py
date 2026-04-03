"""
Management command to update market prices daily
Performs:
1. Records current prices to history
2. Updates price trends
3. Generates market analysis
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date, timedelta
from decimal import Decimal
import random
from django.db.models import Avg, Min, Max, Count

from api.models import MarketPrice, PriceHistory, MarketPriceAnalysis


class Command(BaseCommand):
    help = 'Update market prices daily and generate analysis'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force update even if already run today'
        )

    def handle(self, *args, **options):
        force = options.get('force', False)
        today = date.today()
        
        self.stdout.write(self.style.SUCCESS('🔄 Starting daily market price update...'))
        
        try:
            # Step 1: Record current prices to history
            self.update_price_history(today)
            
            # Step 2: Update current prices with realistic variations
            self.update_current_prices(today)
            
            # Step 3: Generate trend analysis
            self.generate_price_analysis(today)
            
            self.stdout.write(self.style.SUCCESS('✅ Daily market price update completed successfully!'))
            return True
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error during update: {str(e)}'))
            return False

    def update_price_history(self, today):
        """Record current active prices to history"""
        self.stdout.write('📊 Recording price history...')
        
        active_prices = MarketPrice.objects.filter(is_active=True).select_related()
        recorded_count = 0
        
        for market_price in active_prices:
            # Check if already recorded today
            existing = PriceHistory.objects.filter(
                commodity_name=market_price.commodity_name,
                market_date=today
            ).first()
            
            if not existing:
                PriceHistory.objects.create(
                    commodity_name=market_price.commodity_name,
                    price=market_price.price,
                    unit=market_price.unit,
                    market_date=today,
                    market_location=market_price.market_location,
                    source='Auto-Update'
                )
                recorded_count += 1
        
        self.stdout.write(f'  ✓ Recorded {recorded_count} prices to history')

    def update_current_prices(self, today):
        """Update current prices with realistic daily variations"""
        self.stdout.write('💹 Updating current prices...')
        
        active_prices = MarketPrice.objects.filter(is_active=True)
        updated_count = 0
        
        for market_price in active_prices:
            # Get last 7 days prices for context
            recent_prices = PriceHistory.objects.filter(
                commodity_name=market_price.commodity_name,
                market_date__gte=today - timedelta(days=7),
                market_date__lt=today
            ).order_by('-market_date')
            
            if recent_prices.exists():
                # Calculate realistic price change (-5% to +5%)
                last_price = recent_prices.first().price
                change_percent = random.uniform(-5, 5)
                new_price = last_price * (1 + Decimal(str(change_percent)) / 100)
                
                # Ensure minimum price
                new_price = max(new_price, Decimal('0.01'))
                
                # Determine trend
                if change_percent > 1:
                    trend = 'up'
                    trend_percentage = Decimal(str(abs(change_percent)))
                elif change_percent < -1:
                    trend = 'down'
                    trend_percentage = Decimal(str(abs(change_percent)))
                else:
                    trend = 'stable'
                    trend_percentage = Decimal(str(abs(change_percent)))
                
                # Update the market price
                market_price.price = new_price
                market_price.trend = trend
                market_price.trend_percentage = trend_percentage
                market_price.market_date = today
                market_price.source = 'Daily-Update'
                market_price.save()
                updated_count += 1
        
        self.stdout.write(f'  ✓ Updated {updated_count} current prices')

    def generate_price_analysis(self, today):
        """Generate trend analysis for each commodity"""
        self.stdout.write('📈 Generating price analysis...')
        
        # Get all unique commodities
        commodities = PriceHistory.objects.filter(
            market_date__gte=today - timedelta(days=30)
        ).values_list('commodity_name', flat=True).distinct()
        
        analysis_count = 0
        
        for commodity_name in commodities:
            try:
                # Get price data
                prices_7d = PriceHistory.objects.filter(
                    commodity_name=commodity_name,
                    market_date__gte=today - timedelta(days=7)
                ).order_by('market_date')
                
                prices_30d = PriceHistory.objects.filter(
                    commodity_name=commodity_name,
                    market_date__gte=today - timedelta(days=30)
                ).order_by('market_date')
                
                if not prices_7d.exists():
                    continue
                
                # Calculate statistics
                prices_7d_list = list(prices_7d.values_list('price', flat=True))
                prices_30d_list = list(prices_30d.values_list('price', flat=True))
                
                current_price = prices_7d.last().price if prices_7d.exists() else Decimal('0')
                
                def get_stats(prices_list):
                    if not prices_list:
                        return Decimal('0'), Decimal('0'), Decimal('0')
                    return (
                        sum(prices_list) / len(prices_list),  # avg
                        min(prices_list),  # min
                        max(prices_list)   # max
                    )
                
                avg_7d, min_7d, max_7d = get_stats(prices_7d_list)
                avg_30d, min_30d, max_30d = get_stats(prices_30d_list)
                
                # Calculate trend
                if len(prices_7d_list) > 1:
                    price_change = float(prices_7d_list[-1] - prices_7d_list[0])
                    trend_percent = (price_change / float(prices_7d_list[0]) * 100) if prices_7d_list[0] > 0 else 0
                else:
                    trend_percent = 0
                
                trend = 'up' if trend_percent > 1 else ('down' if trend_percent < -1 else 'stable')
                
                # Calculate momentum (-100 to +100)
                momentum = min(100, max(-100, trend_percent * 20))
                
                # Calculate volatility (std dev based)
                if len(prices_7d_list) > 1:
                    mean = float(avg_7d)
                    variance = sum((float(p) - mean) ** 2 for p in prices_7d_list) / len(prices_7d_list)
                    std_dev = variance ** 0.5
                    volatility = (std_dev / mean * 100) if mean > 0 else 0
                    volatility = min(100, volatility)
                else:
                    volatility = 0
                
                # Recommendation
                if trend == 'up' and momentum > 20:
                    recommendation = 'sell'
                elif trend == 'down' and momentum < -20:
                    recommendation = 'buy'
                else:
                    recommendation = 'hold'
                
                # Generate insights
                insights = self.generate_insights(
                    commodity_name, trend, momentum, volatility,
                    current_price, avg_7d, avg_30d
                )
                
                # Create or update analysis
                analysis, created = MarketPriceAnalysis.objects.update_or_create(
                    commodity_name=commodity_name,
                    analysis_date=today,
                    defaults={
                        'current_price': current_price,
                        'avg_price_7d': avg_7d,
                        'min_price_7d': min_7d,
                        'max_price_7d': max_7d,
                        'avg_price_30d': avg_30d,
                        'min_price_30d': min_30d,
                        'max_price_30d': max_30d,
                        'trend': trend,
                        'trend_percentage': Decimal(str(trend_percent)),
                        'momentum_score': Decimal(str(momentum)),
                        'volatility_score': Decimal(str(volatility)),
                        'analysis_type': 'trend',
                        'insights': insights,
                        'recommendation': recommendation,
                    }
                )
                analysis_count += 1
                
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'  ⚠ Error analyzing {commodity_name}: {str(e)}'))
                continue
        
        self.stdout.write(f'  ✓ Generated analysis for {analysis_count} commodities')

    def generate_insights(self, commodity, trend, momentum, volatility, current, avg_7d, avg_30d):
        """Generate human-readable market insights"""
        insights = []
        
        # Trend insights
        if trend == 'up':
            insights.append(f'{commodity} prices are trending upward with momentum score of {momentum:.1f}')
        elif trend == 'down':
            insights.append(f'{commodity} prices are declining. Momentum score: {momentum:.1f}')
        else:
            insights.append(f'{commodity} prices are stable with low volatility')
        
        # Price level insights
        if current > avg_30d:
            pct_above = ((current - avg_30d) / avg_30d * 100)
            insights.append(f'Current price is {pct_above:.1f}% above 30-day average')
        else:
            pct_below = ((avg_30d - current) / avg_30d * 100)
            insights.append(f'Current price is {pct_below:.1f}% below 30-day average')
        
        # Volatility insights
        if volatility > 15:
            insights.append('High price volatility detected - prices are unstable')
        elif volatility < 5:
            insights.append('Prices are very stable with low volatility')
        
        return ' | '.join(insights)
