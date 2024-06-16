from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
from .models import CarMake, CarModel
from .populate import initiate

from .restapis import get_dealers_from_cf, get_dealer_by_id_from_cf

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create an `about` view to render a static about page
def get_about_us(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)

# Create a `contact` view to return a static contact page
def get_contact_us(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact_us.html', context)

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    # If it is a GET request, just render the registration page
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    # If it is a POST request
    elif request.method == 'POST':
        # Get user information from request.POST
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            # Check if user already exists
            User.objects.get(username=username)
            user_exist = True
        except:
            # If not, simply log this is a new user
            logger.debug("{} is new user".format(username))
        # If it is a new user
        if not user_exist:
            # Create user in auth_user table
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            # Login the user and redirect to course list page
            login(request, user)
            return redirect("onlinecourse:popular_course_list")
        else:
            return render(request, 'djangoapp/registration.html', context)
  
# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/login.html', context)
    elif request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('psw')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("djangoapp:index")
        else:
            messages.error(request, "Username or password is incorrect")
            return redirect("djangoapp:login")

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    print("Log out the user `{}`".format(request.user.username))
    logout(request)
    return redirect("djangoapp:index")

def get_cars(request):
    count = CarMake.objects.filter().count()
    print(count)
    if(count == 0):
        initiate()
    car_models = CarModel.objects.select_related('car_make')
    cars = []
    for car_model in car_models:
        cars.append({"CarModel": car_model.name, "CarMake": car_model.car_make.name})
    return JsonResponse({"CarModels":cars})


# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = "https://devinphat97-8000.theiadockernext-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai"
        #url = "http://localhost:3000/dealerships/get" # Can replace with Cloud Function URL
        dealerships = get_dealers_from_cf(url)
        context["dealership_list"] = dealerships
        
        return render(request, 'djangoapp/index.html', context)

# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    print(request, dealer_id)
    if request.method == "GET":
        context = {}    
        url = f"http://127.0.0.1:5000/api/get_reviews?id={dealer_id}"
        # Get dealers from the URL
        reviews = get_dealer_reviews_from_cf(url)
        # Concat all dealer's short name
        dealer_names = " ".join([dealer.name for dealer in reviews])

        context = {"reviews" :reviews, "dealer_id": dealer_id}
        return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    # User must be logged in to post a review
    if request.user.is_authenticated or True:
        # Get request renders the page with the form for filling out a review
        if request.method == "GET":
            url = "http://localhost:3000/dealership/get"
            # Get dealer details from the API
            dealer = get_dealer_by_if_from_cf(url, dealer_id=dealer_id)
            # Extract dealer object at index 1: dealer[1]
            context = {
                "cars": CarModel.objects.all(),
                "dealer": dealer[1],
            }

    return render(request, 'django/add_review.html', context)

    # Post requests posts the content in the reveiw submission form to the Cloudant DB using the post_review Cloud Function
    if request.method == "POST":
        # Get data form the reqest
        review_post_json_data = request.Post # Loads data from the form
        print("AT POST REQUEST: ")
        print(request.POST)
        # Store data to review dictionary one by one
        review = {}
        review["id"] = review_post_json_data.get("id")
        review["name"] = review_post_json_data.get("name")
        review["dealership"] = dealer_id
        review["review"] = review_post_json_data.get("review")
        review["purchase"] = review_post_json_data.get("purchase")

        if review["purchase"]:
            purchase_date_str = review_post_json_data.get("purchase_date")
            if purchase_date_str:
                purchase_date = datetime.strptime(purchase_date_str, "%m/%d/%Y")
                review["purchase_date"] = purchase_date.strftime("%m/%d/%Y")
            else:  
                review["purchase_date"] = None
        else:
            review["purchase_date"] = None

        print("AT review:   ")
        print(review)
        car = get_object_or_404(CarModel, pk=review["id"])
        review["car_make"] = car.car_make.name
        review["car_model"] = car.name
        review["car_year"] = car.car_year.strftime("%Y")

        # make requests to this url: flask server: review.py
        url ="http://127.0.0.1:5000/api/post_review" # APU Cloud Function route
        json_payload = {"review": review} # Create a JSON payload that contains the review data

        # Performing a POST request with the review
        print("JSON PAYLOAD IS HERE:", json_payload)
        #After posting the review the user is redirected back to the dealer details page
        return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
    print("User must be authenticated before posting a review. Please log in.")
    return redirect("/djangoapp/login")