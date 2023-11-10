import requests
import json
# import related models here
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from dotenv import find_dotenv, load_dotenv
import os
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions
from requests.auth import HTTPBasicAuth

load_dotenv(dotenv_path='../server/.env')

IAM_API_KEY = os.environ.get("IAM_API_KEY")
NLU_URL = os.environ.get("NLU_URL")
NLU_API_KEY = os.environ.get("NLU_API_KEY")

# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    params = dict()
    try:
        if 'api_key' in kwargs:
            params["text"] = kwargs["text"]
            params["version"] = kwargs["version"]
            params["features"] = kwargs["features"]
            params["return_analyzed_text"] = kwargs["return_analyzed_text"]
            response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth('apikey', kwargs["api_key"]))
        else:
            response = requests.get(url, params=params, headers={'Content-Type': 'application/json'}, timeout=0.5)
    except Exception as e:
        print(e)
        return
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url,json_payload, **kwargs):
    print(kwargs)
    print("POST from {} ".format(url))
    try:
        response = requests.post(url,params=kwargs,json=json_payload)
        print(response.text, "hello")
        return json.loads(response.text)
    except Exception as e:
        print(e)
        return

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    json_result = get_request(url)
    if json_result:
        for dealer in json_result:
            if dealer and isinstance(dealer, dict):
                dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                        id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                        short_name=dealer["short_name"],
                        st=dealer["st"], zip=dealer["zip"])
                results.append(dealer_obj)
    return results

def get_dealer_by_id(url, dealer_id):
    # Call get_request with the dealer_id param
    json_result = get_request(url, dealer_id=dealer_id)

    # Create a CarDealer object from response
    dealer = json_result[0]
    dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                           id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                           short_name=dealer["short_name"],
                           st=dealer["st"], zip=dealer["zip"])
    return dealer_obj

def get_dealer_by_state(url, dealer_state):
    # Call get_request with the dealer_id param
    json_result = get_request(url, dealer_state=dealer_state)

    # Create a CarDealer object from response
    dealer = json_result[0]
    dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                           id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                           short_name=dealer["short_name"],
                           st=dealer["st"], zip=dealer["zip"])
    return dealer_obj

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(url, **kwargs):
    results = []
    json_result = get_request(url, dealerId=kwargs['dealer_id'])
    if json_result:
        for review in json_result:
            review_obj = DealerReview(
                dealership=review['dealership'],
                name=review['name'],
                purchase=review['purchase'],
                review=review['review'],
                purchase_date=review['purchase_date'],
                car_make=review['car_make'],
                car_model=review['car_model'],
                car_year=review['car_year'],
                sentiment=analyze_review_sentiments(review['review']),
                id=review['_id'],
            )
            results.append(review_obj)
    return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(dealerreview):
    version = '2022-04-07'
    authenticator = IAMAuthenticator(NLU_API_KEY)
    natural_language_understanding = NaturalLanguageUnderstandingV1(version=version, authenticator=authenticator)
    natural_language_understanding.set_service_url(NLU_URL)
    response = natural_language_understanding.analyze(text=dealerreview, features=Features(sentiment=SentimentOptions(targets=[dealerreview]))).get_result()
    label = response['sentiment']['document']['label']
    return label
