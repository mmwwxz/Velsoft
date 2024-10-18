from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('product_list/', views.product_list_view, name='product_list'),
    path('product_detail/<int:pk>/', views.product_detail_view, name='detail'),
    path('product_create/', views.product_create_view, name='create'),
    path('product_report_list/', views.product_report_list_view, name='report'),
    path('sold_product_detail/<int:pk>/', views.sold_product_detail_view, name='sold_product_detail'),
    # User interaction
    path('login/', views.user_login_views, name='login'),
    path('logout/', views.user_logout_view, name='logout'),
    path('register/', views.user_sign_up_view, name='register')
]
