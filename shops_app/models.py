from django.db import models


class Shop(models.Model):
    """
    Database model for the entity Shop.

    Fields:
        shop_name (str): Name of the shop (less than 32 characters).
        category (str): Category of the shop.
        city (str): Location of the shop.
        latitude (float): Latitude in decimal degrees.
        longitude (float): Longitude in decimal degrees.
        created_at (datetime): Date and time of creation (automatically set).
        updated_at (datetime): Date and time of the last update (automatically updated).

    """
    category_choices = (
        ('Clothing', 'Clothing'),
        ('Groceries', 'Groceries'),
        ('Food', 'Food'),
        ('Others', 'Others')
    )

    city_choices = (
        ("Bangalore", "Bangalore"),
    )

    shop_name = models.CharField(max_length=32, help_text='Name of your shop (less than 32 characters)')
    category = models.CharField(choices=category_choices, max_length=32, help_text='Choose one of the following categories')
    city = models.CharField(choices=city_choices, max_length=128, help_text="Choose the location of your shop")
    latitude = models.FloatField(help_text='Latitude in decimal degrees')
    longitude = models.FloatField(help_text='Longitude in decimal degrees')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    
    def __str__(self) -> str:
        return self.shop_name