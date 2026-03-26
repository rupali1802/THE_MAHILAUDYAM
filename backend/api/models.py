"""
Mahila Udyam - Django Models
10 Models for complete business management
"""
from django.db import models
from django.utils import timezone
import uuid


class User(models.Model):
    """Rural women entrepreneur profile - device-based, no login required"""
    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('hi', 'Hindi'),
        ('ta', 'Tamil'),
    ]
    BUSINESS_TYPE_CHOICES = [
        ('agriculture', 'Agriculture'),
        ('handicraft', 'Handicraft'),
        ('food', 'Food & Beverages'),
        ('textile', 'Textile'),
        ('retail', 'Retail'),
        ('service', 'Service'),
        ('dairy', 'Dairy'),
        ('other', 'Other'),
    ]

    device_id = models.CharField(max_length=100, unique=True, primary_key=False)
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, blank=True, default='')
    phone = models.CharField(max_length=15, blank=True, default='')
    email = models.EmailField(blank=True, default='')
    location = models.CharField(max_length=300, blank=True, default='')
    village = models.CharField(max_length=200, blank=True, default='')
    district = models.CharField(max_length=200, blank=True, default='')
    state = models.CharField(max_length=200, blank=True, default='Tamil Nadu')
    business_name = models.CharField(max_length=300, blank=True, default='')
    business_type = models.CharField(max_length=50, choices=BUSINESS_TYPE_CHOICES, default='other')
    upi_id = models.CharField(max_length=100, blank=True, default='')
    language = models.CharField(max_length=5, choices=LANGUAGE_CHOICES, default='en')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'mu_users'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name or self.device_id} ({self.business_type})"


class Income(models.Model):
    """Income records for the entrepreneur"""
    CATEGORY_CHOICES = [
        ('sales', 'Sales'),
        ('service', 'Service'),
        ('loan', 'Loan'),
        ('grant', 'Grant'),
        ('investment', 'Investment'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='incomes', null=True, blank=True)
    device_id = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    source = models.CharField(max_length=300)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='sales')
    description = models.TextField(blank=True, default='')
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'mu_income'
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"Income ₹{self.amount} - {self.source} ({self.date})"


class Expense(models.Model):
    """Business expense records"""
    CATEGORY_CHOICES = [
        ('raw_material', 'Raw Material'),
        ('transport', 'Transport'),
        ('rent', 'Rent'),
        ('electricity', 'Electricity'),
        ('labor', 'Labor'),
        ('marketing', 'Marketing'),
        ('equipment', 'Equipment'),
        ('other', 'Other'),
    ]
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('upi', 'UPI'),
        ('bank_transfer', 'Bank Transfer'),
        ('credit', 'Credit'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses', null=True, blank=True)
    device_id = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')
    description = models.TextField(blank=True, default='')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='cash')
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'mu_expense'
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"Expense ₹{self.amount} - {self.category} ({self.date})"


class Sales(models.Model):
    """Sales transaction records"""
    STATUS_CHOICES = [
        ('completed', 'Completed'),
        ('pending', 'Pending'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sales', null=True, blank=True)
    device_id = models.CharField(max_length=100)
    product_name = models.CharField(max_length=300)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    unit = models.CharField(max_length=50, default='piece')
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    customer_name = models.CharField(max_length=200, blank=True, default='')
    description = models.TextField(blank=True, default='')
    sale_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='completed')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'mu_sales'
        ordering = ['-sale_date', '-created_at']

    def __str__(self):
        return f"Sale: {self.product_name} ₹{self.total_amount} ({self.sale_date})"


class Payment(models.Model):
    """Payment tracking records"""
    METHOD_CHOICES = [
        ('upi', 'UPI'),
        ('cash', 'Cash'),
        ('bank_transfer', 'Bank Transfer'),
        ('cheque', 'Cheque'),
    ]
    STATUS_CHOICES = [
        ('success', 'Success'),
        ('pending', 'Pending'),
        ('failed', 'Failed'),
    ]
    TYPE_CHOICES = [
        ('received', 'Received'),
        ('sent', 'Sent'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments', null=True, blank=True)
    device_id = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    method = models.CharField(max_length=20, choices=METHOD_CHOICES, default='upi')
    payment_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='received')
    reference_number = models.CharField(max_length=200, blank=True, default='')
    party_name = models.CharField(max_length=200, blank=True, default='')
    description = models.TextField(blank=True, default='')
    date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='success')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'mu_payment'
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"Payment ₹{self.amount} via {self.method} ({self.status})"


class MarketPrice(models.Model):
    """Commodity market prices - admin managed"""
    TREND_CHOICES = [
        ('up', 'Up'),
        ('down', 'Down'),
        ('stable', 'Stable'),
    ]
    UNIT_CHOICES = [
        ('kg', 'Per KG'),
        ('quintal', 'Per Quintal'),
        ('litre', 'Per Litre'),
        ('dozen', 'Per Dozen'),
        ('piece', 'Per Piece'),
        ('bundle', 'Per Bundle'),
    ]

    commodity_name = models.CharField(max_length=200)
    commodity_name_hi = models.CharField(max_length=200, blank=True, default='')
    commodity_name_ta = models.CharField(max_length=200, blank=True, default='')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=20, choices=UNIT_CHOICES, default='kg')
    market_date = models.DateField()
    market_location = models.CharField(max_length=200, blank=True, default='')
    trend = models.CharField(max_length=10, choices=TREND_CHOICES, default='stable')
    trend_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    source = models.CharField(max_length=200, default='Admin')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'mu_market_price'
        ordering = ['-market_date', 'commodity_name']

    def __str__(self):
        return f"{self.commodity_name} ₹{self.price}/{self.unit} ({self.market_date})"


class Scheme(models.Model):
    """Government schemes for women entrepreneurs"""
    CATEGORY_CHOICES = [
        ('loan', 'Loan'),
        ('subsidy', 'Subsidy'),
        ('training', 'Training'),
        ('insurance', 'Insurance'),
        ('market_linkage', 'Market Linkage'),
        ('technology', 'Technology'),
        ('other', 'Other'),
    ]
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('closed', 'Closed'),
        ('upcoming', 'Upcoming'),
    ]

    name = models.CharField(max_length=400)
    name_hi = models.CharField(max_length=400, blank=True, default='')
    name_ta = models.CharField(max_length=400, blank=True, default='')
    description = models.TextField()
    description_hi = models.TextField(blank=True, default='')
    description_ta = models.TextField(blank=True, default='')
    eligibility = models.TextField()
    eligibility_hi = models.TextField(blank=True, default='')
    eligibility_ta = models.TextField(blank=True, default='')
    benefits = models.TextField()
    benefits_hi = models.TextField(blank=True, default='')
    benefits_ta = models.TextField(blank=True, default='')
    how_to_apply = models.TextField(blank=True, default='')
    how_to_apply_hi = models.TextField(blank=True, default='')
    how_to_apply_ta = models.TextField(blank=True, default='')
    agency = models.CharField(max_length=300)
    url = models.URLField(blank=True, default='')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    deadline = models.DateField(null=True, blank=True)
    max_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'mu_scheme'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.agency})"


class Mentor(models.Model):
    """Business mentors available to connect with"""
    AVAILABILITY_CHOICES = [
        ('available', 'Available'),
        ('busy', 'Busy'),
        ('offline', 'Offline'),
    ]

    name = models.CharField(max_length=200)
    expertise = models.CharField(max_length=500)
    bio = models.TextField(blank=True, default='')
    phone = models.CharField(max_length=15, blank=True, default='')
    email = models.EmailField(blank=True, default='')
    whatsapp = models.CharField(max_length=15, blank=True, default='')
    experience_years = models.IntegerField(default=0)
    specialization = models.CharField(max_length=300, blank=True, default='')
    languages_spoken = models.CharField(max_length=200, default='Tamil, English')
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=4.0)
    total_reviews = models.IntegerField(default=0)
    availability = models.CharField(max_length=20, choices=AVAILABILITY_CHOICES, default='available')
    location = models.CharField(max_length=200, blank=True, default='')
    profile_image = models.ImageField(upload_to='mentors/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'mu_mentor'
        ordering = ['-rating', 'name']

    def __str__(self):
        return f"{self.name} - {self.specialization}"


class MentorChat(models.Model):
    """Chat messages between users and mentors"""
    TYPE_CHOICES = [
        ('query', 'Query'),
        ('response', 'Response'),
    ]
    STATUS_CHOICES = [
        ('sent', 'Sent'),
        ('read', 'Read'),
        ('replied', 'Replied'),
    ]

    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE, related_name='chats')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mentor_chats', null=True, blank=True)
    device_id = models.CharField(max_length=100)
    message = models.TextField()
    message_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='query')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='sent')
    language = models.CharField(max_length=5, default='en')
    timestamp = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'mu_mentor_chat'
        ordering = ['timestamp']

    def __str__(self):
        return f"Chat with {self.mentor.name} - {self.message_type} ({self.timestamp})"


class PredictionLog(models.Model):
    """
    Log of all ML model predictions for monitoring and continuous improvement.
    Used to track model accuracy in production and identify misclassifications.
    """
    FEEDBACK_CHOICES = [
        ('correct', 'Correct'),
        ('incorrect', 'Incorrect'),
        ('partial', 'Partially Correct'),
        ('pending', 'Pending Feedback'),
    ]
    MODEL_TYPE_CHOICES = [
        ('ml', 'Machine Learning'),
        ('rule_based', 'Rule Based'),
        ('hybrid', 'Hybrid'),
    ]

    # Input
    device_id = models.CharField(max_length=100, db_index=True)
    input_text = models.TextField()
    input_language = models.CharField(max_length=10, default='unknown')
    
    # Prediction
    predicted_intent = models.CharField(max_length=50, db_index=True)
    confidence = models.FloatField()  # 0.0 to 1.0
    raw_confidence = models.FloatField(null=True, blank=True)  # Raw ML score before calibration
    model_used = models.CharField(max_length=20, choices=MODEL_TYPE_CHOICES, default='ml')
    all_probabilities = models.JSONField(default=dict)  # Store all intent probabilities
    
    # Correctness tracking
    actual_intent = models.CharField(
        max_length=50, 
        null=True, 
        blank=True,
        help_text="Actual intent if user corrects prediction"
    )
    user_feedback = models.CharField(
        max_length=10, 
        choices=FEEDBACK_CHOICES, 
        default='pending',
        db_index=True
    )
    feedback_text = models.TextField(blank=True, default='')
    
    # Timestamps and metadata
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    feedback_timestamp = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'mu_prediction_log'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['device_id', '-timestamp']),
            models.Index(fields=['predicted_intent', '-timestamp']),
            models.Index(fields=['user_feedback', '-timestamp']),
            models.Index(fields=['model_used', '-timestamp']),
        ]

    def __str__(self):
        status = "✓" if self.user_feedback == 'correct' else "✗" if self.user_feedback == 'incorrect' else "?"
        return f"{status} [{self.predicted_intent}] {self.input_text[:50]}... (conf: {self.confidence:.2%})"

    def mark_correct(self):
        """Mark this prediction as correct"""
        self.user_feedback = 'correct'
        self.feedback_timestamp = timezone.now()
        self.save()

    def mark_incorrect(self, actual_intent, feedback_text=''):
        """Mark this prediction as incorrect and log the actual intent"""
        self.user_feedback = 'incorrect'
        self.actual_intent = actual_intent
        self.feedback_text = feedback_text
        self.feedback_timestamp = timezone.now()
        self.save()

    @staticmethod
    def get_accuracy_report(days=7):
        """
        Generate accuracy report for the last N days.
        
        Returns:
            dict with overall_accuracy, accuracy_per_intent, low_confidence_predictions
        """
        from django.utils import timezone
        from datetime import timedelta
        from django.db.models import Count, Q, Avg
        
        start_date = timezone.now() - timedelta(days=days)
        
        # Get all feedback received
        logs_with_feedback = PredictionLog.objects.filter(
            timestamp__gte=start_date,
            user_feedback__in=['correct', 'incorrect', 'partial']
        )
        
        if not logs_with_feedback.exists():
            return {'message': 'No predictions with feedback yet', 'total': 0}
        
        total = logs_with_feedback.count()
        correct = logs_with_feedback.filter(user_feedback='correct').count()
        overall_accuracy = correct / total if total > 0 else 0
        
        # Per-intent accuracy
        intent_stats = logs_with_feedback.values('predicted_intent').annotate(
            count=Count('id'),
            correct_count=Count('id', filter=Q(user_feedback='correct')),
        )
        
        accuracy_per_intent = {
            item['predicted_intent']: {
                'total': item['count'],
                'correct': item['correct_count'],
                'accuracy': item['correct_count'] / item['count'] if item['count'] > 0 else 0
            }
            for item in intent_stats
        }
        
        # Low confidence predictions
        low_conf = logs_with_feedback.filter(
            confidence__lt=0.75
        ).aggregate(
            count=Count('id'),
            avg_confidence=Avg('confidence')
        )
        
        return {
            'period_days': days,
            'total_predictions_with_feedback': total,
            'overall_accuracy': overall_accuracy,
            'accuracy_per_intent': accuracy_per_intent,
            'low_confidence_predictions': {
                'count': low_conf['count'],
                'average_confidence': low_conf['avg_confidence'],
            },
            'date_range': f"{start_date.date()} to {timezone.now().date()}"
        }
