import requests
import json
# import related models here
from requests.auth import HTTPBasicAuth


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


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative



