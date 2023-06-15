from django.shortcuts import render, get_object_or_404, redirect
from .models import Shop
from .forms import ShopForm
from .utilities import calculate_distance


def home(request):
    return render(request, 'home.html')

def shops_list(request):
    
    """
    Render a page that displays all the shops in the database as a table.
    Provides options to edit and delete shop entries.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered response with the 'shops_list.html' template.

    """
    shops = Shop.objects.all()
    return render(request, 'shops_list.html', context={'shops': shops})

def add_or_edit_shop(request, shop_id=None):
    
    """
    View function to edit or add a new shop.

    Args:
        request (HttpRequest): The HTTP request object.
        shop_id (int, optional): The ID of the shop to edit. Defaults to None.

    Returns:
        HttpResponse: The rendered response with the 'edit_shop.html' template.

    """

    if shop_id:
        item = get_object_or_404(Shop, pk=shop_id)
    else:
        item = None
    
    if request.method == 'POST':
        form = ShopForm(request.POST, instance=item)
        if form.is_valid():
            item = form.save()
            return redirect('shops_list')
    else:
        form = ShopForm(instance=item)
    
    return render(request, 'edit_shop.html', {'form': form})

def delete_shop(request, shop_id):
    """
    View function to delete an existing shop entry.

    Args:
        request (HttpRequest): The HTTP request object.
        shop_id (int): The ID of the shop to delete.

    Returns:
        HttpResponseRedirect: Redirects to the 'shops_list' URL.

    """
    shop = Shop.objects.get(pk=shop_id)
    shop.delete()
    return redirect('shops_list')

def nearby_shops(request):
    """
    View function that returns an HTML page with a list of stores located within
    the specified radius from the user's current location.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered response with the 'nearby_shops.html' template,
                      including the list of shops within the specified radius and the radius itself.

    """

    # Getting the values submitted by the user
    curr_latitude = float(request.POST.get('latitude'))
    curr_longitude = float(request.POST.get('longitude'))
    city = request.POST.get('city')
    search_radius = int(request.POST.get('search_radius'))
    
    # Querying the db for all the avaialble shops
    shops = Shop.objects.filter(city=city)

    shops_within_radius = []

    for shop in shops:
        # Calculating the disatnce between the shop and current user location
        distance = calculate_distance(curr_latitude, curr_longitude, shop.latitude, shop.longitude)
        if distance <= search_radius:
            shop.distance = distance
            shops_within_radius.append(shop)
    
    return render(request, 'nearby_shops.html', context={'shops': shops_within_radius, 'radius': search_radius})