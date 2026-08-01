from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your Name'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'your.email@example.com'
        })
    )
    subject = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Subject'
        })
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Tell us about your project or ask any questions...'
        })
    )

class CustomDesignForm(forms.Form):
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
    
    customer_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your Name'
        })
    )
    
    customer_email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'your.email@example.com'
        })
    )
    
    clothing_type = forms.ChoiceField(
        choices=CLOTHING_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    size = forms.ChoiceField(
        choices=SIZE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    color = forms.ChoiceField(
        choices=COLOR_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    price_range = forms.ChoiceField(
        choices=PRICE_RANGE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Price Range'
    )
    
    fabric_type = forms.ChoiceField(
        choices=FABRIC_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Fabric Type'
    )
    
    selected_design = forms.IntegerField(
        required=False,
        widget=forms.HiddenInput(attrs={'id': 'selected_design_id'}),
        label='Selected Design'
    )
    
    design_placement = forms.ChoiceField(
        choices=PLACEMENT_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Design Placement',
        initial='front'
    )
    
    design_text = forms.CharField(
        max_length=500,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter text for your design (optional)'
        })
    )
    
    design_upload = forms.FileField(
        required=False,
        label='Upload Design',
        help_text='Upload your design file (.pdf, .jpeg, .png)',
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.pdf,.jpeg,.jpg,.png'
        })
    )
    
    design_description = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Describe your custom design idea...'
        })
    )
    
    quantity = forms.IntegerField(
        min_value=1,
        max_value=100,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '1'
        })
    )

class NewsletterForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email for updates'
        })
    )

class ShippingAddressForm(forms.Form):
    full_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Full Name'
        })
    )
    address_line_1 = forms.CharField(
        max_length=255,
        label='Address Line 1',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Street Address'
        })
    )
    address_line_2 = forms.CharField(
        max_length=255,
        label='Address Line 2',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Apartment, suite, etc. (optional)'
        })
    )
    city = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'City'
        })
    )
    state = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'State/Province'
        })
    )
    postal_code = forms.CharField(
        max_length=20,
        label='ZIP/Postal Code',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'ZIP/Postal Code'
        })
    )
    country = forms.CharField(
        max_length=100,
        initial='India',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Country'
        })
    )
    phone_number = forms.CharField(
        max_length=20,
        label='Phone Number',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Phone Number'
        })
    )

class PaymentDetailsForm(forms.Form):
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
    
    payment_method = forms.ChoiceField(
        choices=PAYMENT_METHOD_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Payment Method'
    )
    
    # Credit/Debit Card fields
    cardholder_name = forms.CharField(
        max_length=100,
        required=False,
        label='Cardholder Name',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Name on Card'
        })
    )
    card_number = forms.CharField(
        max_length=19,
        required=False,
        label='Card Number',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '1234 5678 9012 3456',
            'maxlength': '19'
        })
    )
    expiry_month = forms.ChoiceField(
        choices=[(str(i).zfill(2), str(i).zfill(2)) for i in range(1, 13)],
        required=False,
        label='Expiry Month',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    expiry_year = forms.ChoiceField(
        choices=[(str(i), str(i)) for i in range(2024, 2035)],
        required=False,
        label='Expiry Year',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    cvv = forms.CharField(
        max_length=4,
        required=False,
        label='CVV',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'CVV',
            'maxlength': '4'
        })
    )
    
    def clean(self):
        cleaned_data = super().clean()
        payment_method = cleaned_data.get('payment_method')
        
        # Validate card fields if credit/debit card is selected
        if payment_method in ['credit_card', 'debit_card']:
            required_fields = ['cardholder_name', 'card_number', 'expiry_month', 'expiry_year', 'cvv']
            for field in required_fields:
                if not cleaned_data.get(field):
                    self.add_error(field, 'This field is required for card payments.')
        
        return cleaned_data

class AddToCartForm(forms.Form):
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
    
    size = forms.ChoiceField(
        choices=SIZE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    color = forms.ChoiceField(
        choices=COLOR_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    quantity = forms.IntegerField(
        min_value=1,
        max_value=10,
        initial=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '1',
            'max': '10'
        })
    )
    
class RegularCheckoutForm(forms.Form):
    customer_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your Full Name'
        })
    )
    customer_email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'your.email@example.com'
        })
    )
