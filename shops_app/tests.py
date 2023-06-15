from django.test import TestCase, Client
from django.urls import reverse
from django.shortcuts import get_object_or_404
from .models import Shop
from .forms import ShopForm

class ShopListViewTest(TestCase):
    def test_shops_list_view(self):
        # Create some sample shops
        shop1 = Shop.objects.create(
            shop_name='Shop 1',
            category='Food',
            city='Bangalore',
            latitude=10.1234,
            longitude=20.5678,
        )
        shop2 = Shop.objects.create(
            shop_name='Shop 2',
            category='Clothing',
            city='Bangalore',
            latitude=30.9876,
            longitude=40.5432,
        )

        # Get the URL for the shops_list view
        url = reverse('shops_list')

        # Send a GET request to the view
        response = self.client.get(url)

        # Assert that the response has a 200 status code
        self.assertEqual(response.status_code, 200)

        # Assert that the response uses the 'shops_list.html' template
        self.assertTemplateUsed(response, 'shops_list.html')

        # Assert that the shops are included in the response context
        expected_shops = [repr(shop1), repr(shop2)]
        actual_shops = [repr(shop) for shop in response.context['shops']]
        self.assertListEqual(expected_shops, actual_shops)

class AddOrEditShopViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.add_shop_url = reverse('edit_shop')

    def test_add_shop_view(self):
        # Send a GET request to the add shop view
        response = self.client.get(self.add_shop_url)

        # Assert that the response has a 200 status code
        self.assertEqual(response.status_code, 200)

        # Assert that the response uses the 'edit_shop.html' template
        self.assertTemplateUsed(response, 'edit_shop.html')

        # Assert that the form in the response context is an instance of ShopForm
        self.assertIsInstance(response.context['form'], ShopForm)

        # Assert that the form is not bound to any instance
        self.assertIsNone(response.context['form'].instance.pk)

        # Send a POST request with valid form data
        shop_data = {
            'shop_name': 'Shop 1',
            'category': 'Clothing',
            'city': 'Bangalore',
            'latitude': 10.1234,
            'longitude': 20.5678,
        }
        response = self.client.post(self.add_shop_url, data=shop_data)

        # Assert that the response redirects to the 'shops_list' view
        self.assertRedirects(response, reverse('shops_list'))

        # Assert that the shop was created in the database
        self.assertEqual(Shop.objects.count(), 1)
        shop = Shop.objects.first()
        self.assertEqual(shop.shop_name, 'Shop 1')

    def test_edit_shop_view(self):
        # Create a shop for editing
        shop = Shop.objects.create(
            shop_name='Shop 2',
            category='Clothing',
            city='Bangalore',
            latitude=10.1234,
            longitude=20.5678,
        )

        # Get the URL for editing the shop
        edit_shop_url = reverse('edit_shop', args=[shop.id])

        # Send a GET request to the edit shop view
        response = self.client.get(edit_shop_url)

        # Assert that the response has a 200 status code
        self.assertEqual(response.status_code, 200)

        # Assert that the response uses the 'edit_shop.html' template
        self.assertTemplateUsed(response, 'edit_shop.html')

        # Assert that the form in the response context is an instance of ShopForm
        self.assertIsInstance(response.context['form'], ShopForm)

        # Assert that the form is bound to the shop instance
        self.assertEqual(response.context['form'].instance, shop)

        # Send a POST request with valid form data to save the edits
        edited_shop_data = {
            'shop_name': 'Shop 2 Edited',
            'category': 'Clothing',
            'city': 'Bangalore',
            'latitude': 10.1234,
            'longitude': 20.5678,
        }
        response = self.client.post(edit_shop_url, data=edited_shop_data)

        # Assert that the response redirects to the 'shops_list' view
        self.assertRedirects(response, reverse('shops_list'))

        # Refresh the shop object from the database
        shop.refresh_from_db()

        # Assert that the shop was edited in the database
        self.assertEqual(shop.shop_name, 'Shop 2 Edited')


class NearbyShopsViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.nearby_shops_url = reverse('nearby_shops')

    def test_nearby_shops_view(self):
        # Create some sample shops in the same city
        city = 'Bangalore'
        shop1 = Shop.objects.create(
            shop_name='Shop 1',
            latitude=10.1234,
            longitude=20.5678,
            city=city,
        )
        shop2 = Shop.objects.create(
            shop_name='Shop 2',
            latitude=10.1223,
            longitude=20.5691,
            city=city,
        )
        shop3 = Shop.objects.create(
            shop_name='Shop 3',
            latitude=50.1234,
            longitude=60.5678,
            city='Bangalore',
        )

        # Send a POST request to the nearby_shops view with search parameters
        search_data = {
            'latitude': 10.1190,
            'longitude': 20.4450,
            'city': city,
            'search_radius': 14,  # Adjust the search radius as needed
        }
        response = self.client.post(self.nearby_shops_url, data=search_data)

        # Assert that the response has a 200 status code
        self.assertEqual(response.status_code, 200)

        # Assert that the response uses the 'nearby_shops.html' template
        self.assertTemplateUsed(response, 'nearby_shops.html')

        # Assert that the shops within the radius are included in the response context
        expected_shops = [repr(shop1), repr(shop2)]
        actual_shops = [repr(shop) for shop in response.context['shops']]
        self.assertListEqual(expected_shops, actual_shops)

        # Assert that the radius value is included in the response context
        self.assertEqual(response.context['radius'], search_data['search_radius'])