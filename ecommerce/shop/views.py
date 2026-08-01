from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from .forms import (ContactForm, CustomDesignForm, NewsletterForm, ShippingAddressForm, 
                   PaymentDetailsForm, AddToCartForm, RegularCheckoutForm)
from .models import (CustomOrder, ShippingAddress, PaymentDetails, Category, Product, 
                    Cart, CartItem, RegularOrder, RegularOrderItem, RegularOrderShipping, RegularOrderPayment, Design)
from .email_utils import send_otp_email, send_order_confirmation_email
from decimal import Decimal
import json

def home(request):
    newsletter_form = NewsletterForm()
    
    if request.method == 'POST' and 'newsletter_submit' in request.POST:
        newsletter_form = NewsletterForm(request.POST)
        if newsletter_form.is_valid():
            email = newsletter_form.cleaned_data['email']
            messages.success(request, f'Thank you! {email} has been subscribed to our newsletter.')
            return redirect('home')
    
    return render(request, 'home.html', {'newsletter_form': newsletter_form})

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process the form data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            
            # In a real app, you'd save to database or send email
            messages.success(request, f'Thank you {name}! Your message has been sent. We\'ll get back to you soon.')
            return redirect('contact')
    else:
        form = ContactForm()
    
    return render(request, 'contact.html', {'form': form})

def custom_design(request):
    # Get all active designs
    designs = Design.objects.filter(is_active=True)
    
    if request.method == 'POST':
        form = CustomDesignForm(request.POST, request.FILES)
        if form.is_valid():
            # Get selected design if any
            selected_design_id = form.cleaned_data.get('selected_design')
            selected_design = None
            if selected_design_id:
                try:
                    selected_design = Design.objects.get(id=selected_design_id)
                except Design.DoesNotExist:
                    pass
            
            # Create the order
            order = CustomOrder(
                customer_name=form.cleaned_data['customer_name'],
                customer_email=form.cleaned_data['customer_email'],
                clothing_type=form.cleaned_data['clothing_type'],
                size=form.cleaned_data['size'],
                color=form.cleaned_data['color'],
                price_range=form.cleaned_data['price_range'],
                fabric_type=form.cleaned_data['fabric_type'],
                selected_design=selected_design,
                design_placement=form.cleaned_data['design_placement'],
                design_text=form.cleaned_data['design_text'],
                design_description=form.cleaned_data['design_description'],
                design_upload=form.cleaned_data.get('design_upload'),
                quantity=form.cleaned_data['quantity']
            )
            order.save()
            
            # Store order ID in session for checkout
            request.session['pending_order_id'] = str(order.order_id)
            
            messages.success(request, f'Great! Your custom design is ready. Now let\'s complete your order with shipping and payment details.')
            return redirect('checkout')
    else:
        form = CustomDesignForm()
    
    return render(request, 'custom_design.html', {'form': form, 'designs': designs})

def checkout(request):
    # Get pending order from session
    order_id = request.session.get('pending_order_id')
    if not order_id:
        messages.error(request, 'No pending order found. Please create a design first.')
        return redirect('custom_design')
    
    try:
        order = CustomOrder.objects.get(order_id=order_id, status='pending')
    except CustomOrder.DoesNotExist:
        messages.error(request, 'Order not found or already processed.')
        return redirect('custom_design')
    
    if request.method == 'POST':
        shipping_form = ShippingAddressForm(request.POST, prefix='shipping')
        payment_form = PaymentDetailsForm(request.POST, prefix='payment')
        
        if shipping_form.is_valid() and payment_form.is_valid():
            # Save shipping address
            shipping_address = ShippingAddress(
                order=order,
                full_name=shipping_form.cleaned_data['full_name'],
                address_line_1=shipping_form.cleaned_data['address_line_1'],
                address_line_2=shipping_form.cleaned_data['address_line_2'],
                city=shipping_form.cleaned_data['city'],
                state=shipping_form.cleaned_data['state'],
                postal_code=shipping_form.cleaned_data['postal_code'],
                country=shipping_form.cleaned_data['country'],
                phone_number=shipping_form.cleaned_data['phone_number']
            )
            shipping_address.save()
            
            # Save payment details (in a real app, you'd process payment here)
            payment_details = PaymentDetails(
                order=order,
                payment_method=payment_form.cleaned_data['payment_method'],
                cardholder_name=payment_form.cleaned_data.get('cardholder_name', ''),
                card_last_four=payment_form.cleaned_data.get('card_number', '')[-4:] if payment_form.cleaned_data.get('card_number') else '',
                amount_paid=order.total_price
            )
            
            # Simulate payment processing
            if payment_form.cleaned_data['payment_method'] in ['upi', 'net_banking', 'paypal', 'google_pay', 'paytm', 'razorpay']:
                payment_details.payment_status = 'completed'
                payment_details.transaction_id = f'TXN_{order.order_id.hex[:8].upper()}'
                payment_details.payment_date = timezone.now()
                order.status = 'confirmed'
            elif payment_form.cleaned_data['payment_method'] == 'cod':
                payment_details.payment_status = 'pending'
                payment_details.transaction_id = f'COD_{order.order_id.hex[:8].upper()}'
                order.status = 'confirmed'
            else:
                # For card payments, simulate processing
                payment_details.payment_status = 'completed'
                payment_details.transaction_id = f'TXN_{order.order_id.hex[:8].upper()}'
                payment_details.payment_date = timezone.now()
                order.status = 'confirmed'
            
            payment_details.save()
            order.save()
            
            # Generate and send OTP
            otp_code = order.generate_otp()
            send_otp_email(order, otp_code)
            
            # Clear session
            if 'pending_order_id' in request.session:
                del request.session['pending_order_id']
            
            messages.success(request, 'Order placed successfully! Please check your email for verification code.')
            return redirect('order_confirmation', order_id=order.order_id)
    else:
        shipping_form = ShippingAddressForm(prefix='shipping')
        payment_form = PaymentDetailsForm(prefix='payment')
    
    context = {
        'order': order,
        'shipping_form': shipping_form,
        'payment_form': payment_form
    }
    return render(request, 'checkout.html', context)

def order_confirmation(request, order_id):
    order = get_object_or_404(CustomOrder, order_id=order_id)
    
    context = {
        'order': order,
        'shipping_address': order.shipping_address,
        'payment_details': order.payment_details
    }
    return render(request, 'order_confirmation.html', context)

# Product Views
def shop(request):
    """Display all products with filtering and pagination"""
    products = Product.objects.filter(is_active=True)
    categories = Category.objects.all()
    
    # Filter by category
    category_slug = request.GET.get('category')
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    # Price range filter
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    
    if price_min:
        try:
            price_min = float(price_min)
            products = products.filter(price__gte=price_min)
        except ValueError:
            pass
    
    if price_max:
        try:
            price_max = float(price_max)
            products = products.filter(price__lte=price_max)
        except ValueError:
            pass
    
    # Pagination
    paginator = Paginator(products, 12)  # Show 12 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'current_category': category_slug,
        'search_query': search_query,
        'price_min': price_min,
        'price_max': price_max,
        'cart_count': get_cart_count(request)
    }
    return render(request, 'shop.html', context)

def product_detail(request, slug):
    """Display product details and handle add to cart"""
    product = get_object_or_404(Product, slug=slug, is_active=True)
    
    if request.method == 'POST':
        form = AddToCartForm(request.POST)
        if form.is_valid():
            size = form.cleaned_data['size']
            color = form.cleaned_data['color']
            quantity = form.cleaned_data['quantity']
            
            # Validate size and color are available
            available_sizes = product.get_available_sizes()
            available_colors = product.get_available_colors()
            
            if size not in available_sizes:
                messages.error(request, 'Selected size is not available.')
            elif color not in available_colors:
                messages.error(request, 'Selected color is not available.')
            elif quantity > product.stock_quantity:
                messages.error(request, f'Only {product.stock_quantity} items available.')
            else:
                # Add to cart
                cart = get_or_create_cart(request)
                cart_item, created = CartItem.objects.get_or_create(
                    cart=cart,
                    product=product,
                    size=size,
                    color=color,
                    defaults={'quantity': quantity}
                )
                
                if not created:
                    cart_item.quantity += quantity
                    cart_item.save()
                
                messages.success(request, f'{product.name} added to cart!')
                return redirect('cart')
    else:
        form = AddToCartForm()
    
    # Filter form choices based on product availability
    available_sizes = product.get_available_sizes()
    available_colors = product.get_available_colors()
    
    form.fields['size'].choices = [(size, size.upper()) for size in available_sizes]
    form.fields['color'].choices = [(color, color.title()) for color in available_colors]
    
    context = {
        'product': product,
        'form': form,
        'cart_count': get_cart_count(request)
    }
    return render(request, 'product_detail.html', context)

def cart(request):
    """Display cart contents"""
    cart = get_or_create_cart(request)
    cart_items = cart.items.all()
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'cart_count': get_cart_count(request)
    }
    return render(request, 'cart.html', context)

def update_cart(request, item_id):
    """Update cart item quantity"""
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id)
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity > 0 and quantity <= cart_item.product.stock_quantity:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, 'Cart updated successfully!')
        else:
            messages.error(request, 'Invalid quantity.')
    
    return redirect('cart')

def remove_from_cart(request, item_id):
    """Remove item from cart"""
    cart_item = get_object_or_404(CartItem, id=item_id)
    product_name = cart_item.product.name
    cart_item.delete()
    messages.success(request, f'{product_name} removed from cart.')
    return redirect('cart')

def regular_checkout(request):
    """Checkout for regular products"""
    cart = get_or_create_cart(request)
    cart_items = cart.items.all()
    
    if not cart_items:
        messages.error(request, 'Your cart is empty.')
        return redirect('shop')
    
    if request.method == 'POST':
        checkout_form = RegularCheckoutForm(request.POST, prefix='checkout')
        shipping_form = ShippingAddressForm(request.POST, prefix='shipping')
        payment_form = PaymentDetailsForm(request.POST, prefix='payment')
        
        if checkout_form.is_valid() and shipping_form.is_valid() and payment_form.is_valid():
            # Create order
            order = RegularOrder(
                customer_name=checkout_form.cleaned_data['customer_name'],
                customer_email=checkout_form.cleaned_data['customer_email'],
                total_amount=cart.get_total_price()
            )
            order.save()
            
            # Create order items
            for cart_item in cart_items:
                RegularOrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    size=cart_item.size,
                    color=cart_item.color,
                    quantity=cart_item.quantity,
                    price=cart_item.product.price
                )
                
                # Update stock
                cart_item.product.stock_quantity -= cart_item.quantity
                cart_item.product.save()
            
            # Save shipping address
            RegularOrderShipping.objects.create(
                order=order,
                full_name=shipping_form.cleaned_data['full_name'],
                address_line_1=shipping_form.cleaned_data['address_line_1'],
                address_line_2=shipping_form.cleaned_data['address_line_2'],
                city=shipping_form.cleaned_data['city'],
                state=shipping_form.cleaned_data['state'],
                postal_code=shipping_form.cleaned_data['postal_code'],
                country=shipping_form.cleaned_data['country'],
                phone_number=shipping_form.cleaned_data['phone_number']
            )
            
            # Save payment details
            RegularOrderPayment.objects.create(
                order=order,
                payment_method=payment_form.cleaned_data['payment_method'],
                cardholder_name=payment_form.cleaned_data.get('cardholder_name', ''),
                card_last_four=payment_form.cleaned_data.get('card_number', '')[-4:] if payment_form.cleaned_data.get('card_number') else '',
                payment_status='completed',
                transaction_id=f'REG_{order.order_id.hex[:8].upper()}',
                payment_date=timezone.now(),
                amount_paid=order.total_amount
            )
            
            # Update order status
            order.status = 'confirmed'
            order.save()
            
            # Clear cart
            cart_items.delete()
            
            messages.success(request, 'Order placed successfully!')
            return redirect('regular_order_confirmation', order_id=order.order_id)
    else:
        checkout_form = RegularCheckoutForm(prefix='checkout')
        shipping_form = ShippingAddressForm(prefix='shipping')
        payment_form = PaymentDetailsForm(prefix='payment')
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'checkout_form': checkout_form,
        'shipping_form': shipping_form,
        'payment_form': payment_form,
        'cart_count': get_cart_count(request)
    }
    return render(request, 'regular_checkout.html', context)

def regular_order_confirmation(request, order_id):
    """Order confirmation for regular orders"""
    order = get_object_or_404(RegularOrder, order_id=order_id)
    
    context = {
        'order': order,
        'cart_count': get_cart_count(request)
    }
    return render(request, 'regular_order_confirmation.html', context)

def verify_otp(request, order_id):
    """Verify OTP for order confirmation"""
    if request.method == 'POST':
        try:
            order = get_object_or_404(CustomOrder, order_id=order_id)
            data = json.loads(request.body)
            entered_otp = data.get('otp_code', '').strip()
            
            if not entered_otp:
                return JsonResponse({'success': False, 'error': 'Please enter OTP code'})
            
            success, message = order.verify_otp(entered_otp)
            
            if success:
                # Send order confirmation email
                send_order_confirmation_email(order)
                return JsonResponse({'success': True, 'message': message})
            else:
                return JsonResponse({'success': False, 'error': message})
                
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid request format'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': 'An error occurred. Please try again.'})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

def resend_otp(request, order_id):
    """Resend OTP for order confirmation"""
    if request.method == 'POST':
        try:
            order = get_object_or_404(CustomOrder, order_id=order_id)
            
            # Generate new OTP
            otp_code = order.generate_otp()
            
            # Send OTP email
            if send_otp_email(order, otp_code):
                return JsonResponse({'success': True, 'message': 'New OTP sent successfully'})
            else:
                return JsonResponse({'success': False, 'error': 'Failed to send OTP. Please try again.'})
                
        except Exception as e:
            return JsonResponse({'success': False, 'error': 'An error occurred. Please try again.'})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

# Helper functions
def get_or_create_cart(request):
    """Get or create cart for the session"""
    if not request.session.session_key:
        request.session.create()
    
    session_key = request.session.session_key
    cart, created = Cart.objects.get_or_create(session_key=session_key)
    return cart

def get_cart_count(request):
    """Get total items in cart"""
    try:
        cart = get_or_create_cart(request)
        return cart.get_total_items()
    except:
        return 0
