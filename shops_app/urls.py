from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('shops', views.shops_list, name='shops_list'),
    path('edit_shop/', views.add_or_edit_shop, name='edit_shop'),
    path('edit_shop/<int:shop_id>/', views.add_or_edit_shop, name='edit_shop'),
    path('delete_shop/<int:shop_id>/', views.delete_shop, name='delete_shop'),
    path('nearby_shops/', views.nearby_shops, name='nearby_shops')
]