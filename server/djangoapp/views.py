from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .models import CarModel
# from .restapis import related methods
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    return render(request, 'djangoapp/about.html')


# Create a `contact` view to return a static contact page
def contact(request):
    return render(request, 'djangoapp/contact.html')


# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            return render(request, 'djangoapp/index.html', context)
    else:
        return render(request, 'djangoapp/index.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    print("Log out the user `{}`".format(request.user.username))
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.debug("{} is new user".format(username))
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...
def get_dealer_details(request, dealer_id, dealer_name):
    if request.method == "GET":
        context = {}
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/80dba8ac-9699-4879-a3ff-49b1c42351e5/review-package/get-review.json"
        # Get dealers from the URL
        context['reviews'] = get_dealer_reviews_from_cf(url,dealer_id=dealer_id)
        context['dealer'] = dealer_name
        return render(request,'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...
def add_review(request, dealer_id, dealer_name):
    if request.method == "GET":
        context = {}
        context['dealer'] = dealer_name
        cars = CarModel.objects.filter(id=int(dealer_id)).all()
        context['cars'] = cars
        return render(request, 'djangoapp/add_review.html',context)
    if request.method == "POST" and request.user.is_authenticated:
        car = CarModel.objects.get(pk=int(request.POST['car']))
        json_payload = {
            'dealership':dealer_id,
            'name': request.user.username,
            'review': request.POST['review'],
            'purchase': bool(request.POST.get('purchase',False)),
            'car_make': car.car_make.name,
            'car_model': car.name,
            'car_year': car.year.strftime("%Y"),
            'purchase_date': datetime.strptime(request.POST['date'], "%m/%d/%Y").isoformat()
        }
        url= "https://us-south.functions.appdomain.cloud/api/v1/web/80dba8ac-9699-4879-a3ff-49b1c42351e5/review-package/create-review"
        post_request(url=url, json_payload=json_payload)
        return redirect("djangoapp:dealer_details", dealer_id=dealer_id, dealer_name=dealer_name)
    else:
        return HttpResponse({"message":"Forbidden"})
