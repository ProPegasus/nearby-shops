from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('shops', views.shops_list, name='shops_list'),
    path('edit_shop/', views.add_or_edit_shop, name='edit_shop'),
    path('edit_shop/<int:shop_id>/', views.add_or_edit_shop, name='edit_shop'),
    path('delete_shop/<int:shop_id>/', views.delete_shop, name='delete_shop'),
    path('nearby_shops/', views.nearby_shops, name='nearby_shops')
]