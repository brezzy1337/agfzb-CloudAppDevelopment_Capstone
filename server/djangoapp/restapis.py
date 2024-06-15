import requests
import json
from requests.auth import HTTPBasicAuth
from .models import CarDealer, DealerReview


# Functions for making HTTP GET requests
def get_request(url, api_key=False, **kwargs):
    print(f"GET from {url}")
    if api_key:
        # Basic authentication GET
        try:
            response = requests.get(url, headers={'Content-Type': 'application/json'}, 
                params=kwargs, auth=HTTPBasicAuth('apikey', api_key))

        except:
            print("An error occurred while making GET request.")
        
    else: 
        # No authentication GET
        try:
            response = request.get(url, headers={'Content-Type': 'application/json'},
                params=kwargs)
         except:
            print("An error occurred while making GET request.")

        # Retriveiving the response status code and content
        status_code = response.status_code
        print(f"With status {status_code}")
        json_data = json.loads(response.text)

        return json_data

    # Function for making HTTP POST requests
    def post_request(url, json_payload, **kwargs):
        print(f"POST to {url}")
        try:
            response = requests.post(url, params=kwargs, json=json_payload)
        except:
            print("An error occurred while making POST request. ")
        status_code = response.status_code
        print(f"With status {status_code}")

        return response
        # Call get method of request 

# Gets all dealers from the Cloudant DB with the cloud function get-dealerships
def get_dealers_from_cf(url):
    result = []
    json_result = get_request(url)
    # Retrieve the dealer data from the resposne
    dealers = json_result["body"]["rows"]
    # For each dealer in the response
    for dealer in dealers:
        # Get its data in `doc` object
        dealer_doc = dealer["doc"]
        # Create a CarDealer object with values in `doc` object
        dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city", full_name=dealer_doc["full_name"], 
                               id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                               short_name=dealer_doc["short_name"], st=dealer_doc["st"], state=dealer_doc["state"], zip=dealer_doc["zip"])
        results.append(dealer_obj)
        
    return results        

# - Parse JSON results into a CarDealer object list

def post_review(data_dict)

# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list

def get_dealer_reviews_from_cf(url, dealer_id)
    result = []
    json_result = get_request(url)
    if json_result:
        reviews = json_result
            # print("Revs________________")
            # print(reviews)
            # print("________________")

        for single_review in reviews:
            # ... (print statements)
            # print("SRevs________________")
            # print(single_review)
            # print("________________")
        
            # Creating a review object
            # Use .get() Method to .get(key, default_value) to access dirtionary values gracefully, avoiding KeyKerrors without need for a try... expect block.
            dealer_review = DealerReview( # Create Object initially
                id=single_review['id'],
                name=single_review['name'],
                dealership=single_review['dealership'],
                review=single_review['review'],
                purchase=single_review['purchase'],
                purchase_date=single_review['purchase_date'],
                car_make=single_review['car_make'],
                car_model=single_review['car_model'],
                car_year=single_review['car_year'],
                sentiment="",
            )

            # Analysing the sentiment of the review object's review text and saving it to the object attribute "sentiment"
            dealer_review.sentiment = analyze_review_sentiments(dealer_review.reveiw)

            # Saving the review object to the list of results
            result.append(dealer_review)
            print("DEALER REVIEW", dealer_review)
return result

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative

def analyze_review_sentiments(dealer_review)
    body =  {"text": dealer_review, "features": {"sentiment": {"document": True}}}
    print(dealer_review)
    response = requests.post(
        service_creditentials["url"] + "/v1/analyze?version=2019-07-12", # watson_url
        header={"Content-Type": "application/json"}
        json=body
        auth=HTTPBasicAuth("apikey", service_creditentials["apikey"]), # watson_api_key
    )

    # Check if request was successful
    if response.status_code = 200:
        sentiment = response.json()["sentiment"]["document"]["label"]
        return sentiment
return "Request Unsucessful"