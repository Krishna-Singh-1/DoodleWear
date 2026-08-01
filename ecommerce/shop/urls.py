from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('design/', views.custom_design, name='custom_design'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-confirmation/<uuid:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('verify-otp/<uuid:order_id>/', views.verify_otp, name='verify_otp'),
    path('resend-otp/<uuid:order_id>/', views.resend_otp, name='resend_otp'),
    
    # Shop URLs
    path('shop/', views.shop, name='shop'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart, name='cart'),
    path('cart/update/<int:item_id>/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('regular-checkout/', views.regular_checkout, name='regular_checkout'),
    path('regular-order-confirmation/<uuid:order_id>/', views.regular_order_confirmation, name='regular_order_confirmation'),
]
