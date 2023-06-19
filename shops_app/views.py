from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from .models import Shop
from .forms import ShopForm
from .utilities import calculate_distance


def home(request):
    """
    Render a page that displays a form which the users can use
    to search for nearby shops.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered response with the 'home.html' template.

    """
    return render(request, 'home.html', context={'title': "Find nearby shops"})


class CustomLoginView(auth_views.LoginView):
    """
    Custom login view that extends the default Django LoginView.

    This custom view allows for additional context variables to be passed to the login template,
    enabling dynamic customization of the page title.
    """

    def get_context_data(self, **kwargs):
        """
        Retrieves the context data to be passed to the login template.

        Additional context variables, the 'title', has be added to provide dynamic customization.

        Returns:
            dict: A dictionary containing the context data.
        """
        context = super().get_context_data(**kwargs)
        context['title'] = "Login" 
        return context


def register(request):
    """
    View function for user registration.

    Handles both GET and POST requests. If the request is a POST, it validates
    the registration form, saves the user, logs in the user, and redirects to the home page.
    If the form is invalid, it displays the validation errors.
    If the request is a GET, it renders the registration form.

    Args:
        request: The HTTP request object.

    Returns:
        A rendered registration template or a redirect to the home page.

    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username = username, password = password)
            login(request, user)
            return redirect('home')
        else:
            # Form is invalid, display errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form, 'title': "Register"})


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
    return render(request, 'shops_list.html', context={'shops': shops, 'title': "Shops List"})


@login_required
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
    
    return render(request, 'edit_shop.html', {'form': form, 'title': "Add or edit shop"})


@login_required
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
    
    return render(request, 'nearby_shops.html', context={'shops': shops_within_radius, 'radius': search_radius, 'title': "Nearby Shops Results"})
