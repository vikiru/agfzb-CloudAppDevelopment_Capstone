import requests
import json
# import related models here
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from dotenv import find_dotenv, load_dotenv
import os
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
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
    params["text"] = kwargs["text"]
    params["version"] = kwargs["version"]
    params["features"] = kwargs["features"]
    params["return_analyzed_text"] = kwargs["return_analyzed_text"]
    try:
        if NLU_API_KEY:
            response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth('apikey', NLU_API_KEY))
        else:
            response = requests.get(url, params=params)
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
        dealers = json_result["rows"]
        for dealer in dealers:
            dealer_doc = dealer['doc']
            print(dealer_doc)
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)
    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(url, **kwargs):
    results = []
    json_result = get_request(url, dealerId=kwargs['dealer_id'])
    if json_result:
        reviews = json_result["docs"]
        for review in reviews:
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
    return_analyzed_text = True
    text = dealerreview
    features = {"sentiment":{}}
    response = get_request(NLU_URL, text=text, return_analyzed_text=return_analyzed_text, features=features, version=version)
    print(response)
