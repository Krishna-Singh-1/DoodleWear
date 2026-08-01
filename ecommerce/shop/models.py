from django.db import models
from django.contrib.auth.models import User
import uuid

class Design(models.Model):
    """Pre-made designs that customers can choose from"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='designs/', help_text='Design image/preview')
    thumbnail = models.ImageField(upload_to='designs/thumbnails/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name

class CustomOrder(models.Model):
    CLOTHING_CHOICES = [
        ('t-shirt', 'T-Shirt'),
        ('hoodie', 'Hoodie'),
        ('tank-top', 'Tank Top'),
        ('long-sleeve', 'Long Sleeve'),
    ]
    
    SIZE_CHOICES = [
        ('xs', 'XS'),
        ('s', 'Small'),
        ('m', 'Medium'),
        ('l', 'Large'),
        ('xl', 'XL'),
        ('xxl', 'XXL'),
    ]
    
    COLOR_CHOICES = [
        ('black', 'Black'),
        ('white', 'White'),
        ('red', 'Red'),
        ('blue', 'Blue'),
        ('green', 'Green'),
        ('yellow', 'Yellow'),
        ('purple', 'Purple'),
        ('pink', 'Pink'),
    ]
    
    PRICE_RANGE_CHOICES = [
        ('budget', '₹800 - ₹1200 (Budget Friendly)'),
        ('standard', '₹1200 - ₹2000 (Standard Quality)'),
        ('premium', '₹2000 - ₹3000 (Premium Quality)'),
        ('luxury', '₹3000+ (Luxury/Designer)'),
    ]
    
    FABRIC_CHOICES = [
        ('cotton', '100% Cotton'),
        ('polyester', '100% Polyester'),
        ('blend', 'Cotton-Polyester Blend'),
        ('organic_cotton', 'Organic Cotton'),
        ('bamboo', 'Bamboo Fabric'),
        ('linen', 'Linen'),
        ('fleece', 'Fleece'),
        ('jersey', 'Jersey Knit'),
    ]
    
    PLACEMENT_CHOICES = [
        ('front', 'Front'),
        ('back', 'Back'),
        ('both', 'Both Front & Back'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending Payment'),
        ('confirmed', 'Order Confirmed'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    # Order identification
    order_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Customer information
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    
    # Product details
    clothing_type = models.CharField(max_length=20, choices=CLOTHING_CHOICES)
    size = models.CharField(max_length=5, choices=SIZE_CHOICES)
    color = models.CharField(max_length=20, choices=COLOR_CHOICES)
    price_range = models.CharField(max_length=20, choices=PRICE_RANGE_CHOICES, default='standard')
    fabric_type = models.CharField(max_length=20, choices=FABRIC_CHOICES, default='cotton')
    
    # Design options
    selected_design = models.ForeignKey(Design, on_delete=models.SET_NULL, null=True, blank=True, related_name='custom_orders', help_text='Pre-made design selected by customer')
    design_placement = models.CharField(max_length=10, choices=PLACEMENT_CHOICES, default='front', help_text='Where to place the design')
    design_text = models.CharField(max_length=500, blank=True)
    design_description = models.TextField()
    design_upload = models.FileField(upload_to='custom_designs/', blank=True, null=True, help_text='Upload your design (.pdf, .jpeg, .png)')
    quantity = models.PositiveIntegerField()
    
    # Pricing
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=1500.00)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # OTP Verification
    otp_code = models.CharField(max_length=6, blank=True, null=True)
    otp_created_at = models.DateTimeField(blank=True, null=True)
    is_otp_verified = models.BooleanField(default=False)
    otp_attempts = models.PositiveIntegerField(default=0)
    
    def save(self, *args, **kwargs):
        if not self.total_price:
            base_price = self.unit_price
            # Add premium for certain items
            if self.clothing_type == 'hoodie':
                base_price += 500  # ₹500 premium for hoodies
            elif self.clothing_type == 'long-sleeve':
                base_price += 200  # ₹200 premium for long sleeves
            
            self.total_price = base_price * self.quantity
        super().save(*args, **kwargs)
    
    def generate_otp(self):
        """Generate a new OTP code"""
        import random
        from django.utils import timezone
        
        self.otp_code = str(random.randint(100000, 999999))
        self.otp_created_at = timezone.now()
        self.otp_attempts = 0
        self.save(update_fields=['otp_code', 'otp_created_at', 'otp_attempts'])
        return self.otp_code
    
    def is_otp_valid(self):
        """Check if OTP is still valid (within 10 minutes)"""
        if not self.otp_created_at:
            return False
        
        from django.utils import timezone
        from datetime import timedelta
        
        return timezone.now() - self.otp_created_at < timedelta(minutes=10)
    
    def verify_otp(self, entered_otp):
        """Verify the entered OTP"""
        self.otp_attempts += 1
        self.save(update_fields=['otp_attempts'])
        
        if self.otp_attempts > 3:
            return False, "Too many attempts. Please request a new OTP."
        
        if not self.is_otp_valid():
            return False, "OTP has expired. Please request a new one."
        
        if self.otp_code == entered_otp:
            self.is_otp_verified = True
            self.otp_code = None  # Clear OTP after successful verification
            self.save(update_fields=['is_otp_verified', 'otp_code'])
            return True, "OTP verified successfully!"
        
        return False, "Invalid OTP code."
    
    def __str__(self):
        return f"Order {self.order_id} - {self.customer_name}"
    
    class Meta:
        ordering = ['-created_at']

class ShippingAddress(models.Model):
    order = models.OneToOneField(CustomOrder, on_delete=models.CASCADE, related_name='shipping_address')
    full_name = models.CharField(max_length=100)
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default='India')
    phone_number = models.CharField(max_length=20)
    
    def __str__(self):
        return f"Shipping for Order {self.order.order_id}"

class PaymentDetails(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('upi', 'UPI (PhonePe, Google Pay, Paytm)'),
        ('net_banking', 'Net Banking'),
        ('paypal', 'PayPal'),
        ('google_pay', 'Google Pay'),
        ('paytm', 'Paytm Wallet'),
        ('razorpay', 'Razorpay'),
        ('cod', 'Cash on Delivery'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    order = models.OneToOneField(CustomOrder, on_delete=models.CASCADE, related_name='payment_details')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    
    # Card details (encrypted in real implementation)
    cardholder_name = models.CharField(max_length=100, blank=True)
    card_last_four = models.CharField(max_length=4, blank=True)
    
    # Payment processing
    transaction_id = models.CharField(max_length=100, blank=True)
    payment_date = models.DateTimeField(null=True, blank=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"Payment for Order {self.order.order_id}"

# Regular Products Models
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Product(models.Model):
    SIZE_CHOICES = [
        ('xs', 'XS'),
        ('s', 'Small'),
        ('m', 'Medium'),
        ('l', 'Large'),
        ('xl', 'XL'),
        ('xxl', 'XXL'),
    ]
    
    COLOR_CHOICES = [
        ('black', 'Black'),
        ('white', 'White'),
        ('red', 'Red'),
        ('blue', 'Blue'),
        ('green', 'Green'),
        ('yellow', 'Yellow'),
        ('purple', 'Purple'),
        ('pink', 'Pink'),
        ('gray', 'Gray'),
        ('navy', 'Navy'),
    ]
    
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    available_sizes = models.CharField(max_length=200, help_text='Comma-separated sizes (xs,s,m,l,xl,xxl)')
    available_colors = models.CharField(max_length=200, help_text='Comma-separated colors')
    stock_quantity = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    def get_available_sizes(self):
        if self.available_sizes:
            return [size.strip() for size in self.available_sizes.split(',')]
        return []
    
    def get_available_colors(self):
        if self.available_colors:
            return [color.strip() for color in self.available_colors.split(',')]
        return []
    
    def is_in_stock(self):
        return self.stock_quantity > 0

class Cart(models.Model):
    session_key = models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Cart {self.id}"
    
    def get_total_price(self):
        return sum(item.get_total_price() for item in self.items.all())
    
    def get_total_items(self):
        return sum(item.quantity for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.CharField(max_length=10)
    color = models.CharField(max_length=20)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['cart', 'product', 'size', 'color']
    
    def __str__(self):
        return f"{self.product.name} - {self.size}/{self.color} x{self.quantity}"
    
    def get_total_price(self):
        return self.product.price * self.quantity

class RegularOrder(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Payment'),
        ('confirmed', 'Order Confirmed'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    order_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Order {self.order_id} - {self.customer_name}"

class RegularOrderItem(models.Model):
    order = models.ForeignKey(RegularOrder, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.CharField(max_length=10)
    color = models.CharField(max_length=20)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price at time of order
    
    def __str__(self):
        return f"{self.product.name} x{self.quantity}"
    
    def get_total_price(self):
        return self.price * self.quantity

class RegularOrderShipping(models.Model):
    order = models.OneToOneField(RegularOrder, on_delete=models.CASCADE, related_name='shipping_address')
    full_name = models.CharField(max_length=100)
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default='India')
    phone_number = models.CharField(max_length=20)
    
    def __str__(self):
        return f"Shipping for Order {self.order.order_id}"

class RegularOrderPayment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('upi', 'UPI (PhonePe, Google Pay, Paytm)'),
        ('net_banking', 'Net Banking'),
        ('paypal', 'PayPal'),
        ('google_pay', 'Google Pay'),
        ('paytm', 'Paytm Wallet'),
        ('razorpay', 'Razorpay'),
        ('cod', 'Cash on Delivery'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    order = models.OneToOneField(RegularOrder, on_delete=models.CASCADE, related_name='payment_details')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    cardholder_name = models.CharField(max_length=100, blank=True)
    card_last_four = models.CharField(max_length=4, blank=True)
    transaction_id = models.CharField(max_length=100, blank=True)
    payment_date = models.DateTimeField(null=True, blank=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"Payment for Order {self.order.order_id}"
