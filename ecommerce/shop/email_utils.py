from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def send_otp_email(order, otp_code):
    """Send OTP verification email to customer"""
    try:
        subject = f'Verify Your Order - {order.order_id}'
        
        # Create HTML email content
        html_message = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f4f4f4; }}
                .container {{ max-width: 600px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 10px; }}
                .header {{ text-align: center; margin-bottom: 30px; }}
                .otp-box {{ background-color: #f8f9fa; padding: 20px; border-radius: 8px; text-align: center; margin: 20px 0; }}
                .otp-code {{ font-size: 32px; font-weight: bold; color: #007bff; letter-spacing: 8px; }}
                .footer {{ margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee; text-align: center; color: #666; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1 style="color: #333;">DoodleWear</h1>
                    <h2 style="color: #007bff;">Order Verification Required</h2>
                </div>
                
                <p>Dear {order.customer_name},</p>
                
                <p>Thank you for your order! To complete your order confirmation, please verify your email address using the code below:</p>
                
                <div class="otp-box">
                    <p style="margin: 0; color: #333;">Your verification code is:</p>
                    <div class="otp-code">{otp_code}</div>
                    <p style="margin: 10px 0 0 0; color: #666; font-size: 14px;">This code is valid for 10 minutes</p>
                </div>
                
                <p><strong>Order Details:</strong></p>
                <ul>
                    <li>Order ID: {order.order_id}</li>
                    <li>Product: {order.get_clothing_type_display()} - Custom Design</li>
                    <li>Quantity: {order.quantity}</li>
                    <li>Total: ₹{order.total_price}</li>
                </ul>
                
                <p>If you didn't place this order, please ignore this email or contact our support team.</p>
                
                <div class="footer">
                    <p>Thank you for choosing DoodleWear!</p>
                    <p>Need help? Contact us at support@doodlewear.com</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Create plain text version
        plain_message = f"""
DoodleWear - Order Verification Required

Dear {order.customer_name},

Thank you for your order! To complete your order confirmation, please verify your email address using the code below:

Your verification code is: {otp_code}
(This code is valid for 10 minutes)

Order Details:
- Order ID: {order.order_id}
- Product: {order.get_clothing_type_display()} - Custom Design
- Quantity: {order.quantity}
- Total: ₹{order.total_price}

If you didn't place this order, please ignore this email or contact our support team.

Thank you for choosing DoodleWear!
Need help? Contact us at support@doodlewear.com
        """
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@doodlewear.com'),
            recipient_list=[order.customer_email],
            html_message=html_message,
            fail_silently=False
        )
        
        logger.info(f"OTP email sent successfully to {order.customer_email} for order {order.order_id}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send OTP email to {order.customer_email}: {str(e)}")
        return False

def send_order_confirmation_email(order):
    """Send order confirmation email after successful OTP verification"""
    try:
        subject = f'Order Confirmed - {order.order_id}'
        
        html_message = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f4f4f4; }}
                .container {{ max-width: 600px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 10px; }}
                .header {{ text-align: center; margin-bottom: 30px; }}
                .success-box {{ background-color: #d4edda; padding: 20px; border-radius: 8px; text-align: center; margin: 20px 0; border: 1px solid #c3e6cb; }}
                .order-details {{ background-color: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0; }}
                .footer {{ margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee; text-align: center; color: #666; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1 style="color: #333;">DoodleWear</h1>
                    <h2 style="color: #28a745;">Order Confirmed!</h2>
                </div>
                
                <div class="success-box">
                    <h3 style="color: #155724; margin: 0;">✅ Your order has been confirmed and is now being processed</h3>
                </div>
                
                <p>Dear {order.customer_name},</p>
                
                <p>Congratulations! Your custom design order has been successfully confirmed and verified. We're excited to start working on your unique piece.</p>
                
                <div class="order-details">
                    <h3 style="margin-top: 0;">Order Details</h3>
                    <p><strong>Order ID:</strong> {order.order_id}</p>
                    <p><strong>Product:</strong> {order.get_clothing_type_display()} - Custom Design</p>
                    <p><strong>Size:</strong> {order.get_size_display()}</p>
                    <p><strong>Color:</strong> {order.get_color_display()}</p>
                    <p><strong>Quantity:</strong> {order.quantity}</p>
                    <p><strong>Total Amount:</strong> ₹{order.total_price}</p>
                    <p><strong>Status:</strong> {order.get_status_display()}</p>
                </div>
                
                <p><strong>What happens next?</strong></p>
                <ol>
                    <li>Our design team will review your requirements</li>
                    <li>We'll create your custom design</li>
                    <li>Your order will be printed and prepared</li>
                    <li>We'll ship it to your address</li>
                    <li>You'll receive tracking information via email</li>
                </ol>
                
                <p><strong>Estimated delivery:</strong> 7-10 business days</p>
                
                <div class="footer">
                    <p>Thank you for choosing DoodleWear!</p>
                    <p>Need help? Contact us at support@doodlewear.com</p>
                    <p>Track your order status anytime by contacting us with your Order ID</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        plain_message = f"""
DoodleWear - Order Confirmed!

Dear {order.customer_name},

Congratulations! Your custom design order has been successfully confirmed and verified. We're excited to start working on your unique piece.

Order Details:
- Order ID: {order.order_id}
- Product: {order.get_clothing_type_display()} - Custom Design
- Size: {order.get_size_display()}
- Color: {order.get_color_display()}
- Quantity: {order.quantity}
- Total Amount: ₹{order.total_price}
- Status: {order.get_status_display()}

What happens next?
1. Our design team will review your requirements
2. We'll create your custom design
3. Your order will be printed and prepared
4. We'll ship it to your address
5. You'll receive tracking information via email

Estimated delivery: 7-10 business days

Thank you for choosing DoodleWear!
Need help? Contact us at support@doodlewear.com
Track your order status anytime by contacting us with your Order ID
        """
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@doodlewear.com'),
            recipient_list=[order.customer_email],
            html_message=html_message,
            fail_silently=False
        )
        
        logger.info(f"Order confirmation email sent successfully to {order.customer_email} for order {order.order_id}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send order confirmation email to {order.customer_email}: {str(e)}")
        return False