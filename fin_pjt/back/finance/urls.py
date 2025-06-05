# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('deposits/', views.deposit_products_list, name='deposit-products-list'), 
    path('deposits/<str:fin_prdt_cd>/', views.deposit_product_detail, name='deposit-product-detail'),  
    path('deposit-options/', views.deposit_options_list, name='deposit-options-list'),
    path('deposit-options/<str:fin_prdt_cd>/', views.deposit_options_detail, name='deposit-options-detail'),
    path('savings/', views.saving_products_list, name='saving-products-list'),
    path('saving-options/', views.saving_options_list, name='saving-options-list'),
    path('saving-options/<str:fin_prdt_cd>/', views.saving_options_detail, name='saving-options-detail'),
    path('get-product-code/', views.get_product_code, name='get-product-code'),
]
