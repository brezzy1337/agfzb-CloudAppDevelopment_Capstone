import requests
import json
from requests.auth import HTTPBasicAuth
from .models import CarDealer, DealerReview


# Functions for making HTTP GET requests
def get_request(url, api_key=False, **kwargs):
    print(f"GET from {url}")
    print(kwargs)
    response = None
    if api_key:
        # Basic authentication GET
        try:
            response = requests.get(url, headers={'Content-Type': 'application/json'}, 
                params=kwargs, auth=HTTPBasicAuth('apikey', api_key))
        except Exception as e:
            print("An error occurred while making GET request with API Key: {e}")
            return None
    else: 
        # No authentication GET
        try:
            response = request.get(url, headers={'Content-Type': 'application/json'},
                params=kwargs)
        except Exception as e:
            print("An error occurred while making GET request: {e}")
            return None

    if response and response.status_code == 200:
        try:
            json_data = response.json()
            print(f"With status {response.status_code}")
            return json_data
        except json.JSONDecodeError as e:
            print9 (f"Error parsing JSON response: {e}")
        # Retriveiving the response status code and content
        
    else:
        if response:
            print(f"Request failed with status {response.status_code}")
        else:
            print("No response received")
        return None
#        status_code = response.status_code
#        print(f"With status {status_code}")
#        json_data = json.loads(response.text)

#     return json_data

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

    if json_result:
        print("JSON RESULT:", json_result)
        # Get the row list in JSON as dealers
        # dealers = json_result[0]
        
        # First Run Node.js Server on 3000 Port 
        # Second Run Pyserver on 8000 Port then
        # copy the nodes server url running on port 3000 and place it in views file get_dealership
        
        #json_result = [{}, {}, {}...] So iterte over each document.
        
        for dealer in json_result:
            dealer_doc = dealer
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"], 
                                id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                short_name=dealer_doc["short_name"], st=dealer_doc["st"], state=dealer_doc["state"], zip=dealer_doc["zip"])
            results.append(dealer_obj)
        return results

    else:
        print("No data recieved from get request.")
        return []

# Get reviews by dealer id from a cloud function
def get_dealer_by_id_from_cf(url, dealer_id):
    results = [{}]

    url_with_id = "{url}?id={dealer_id}".format(url=url, dealer_id=dealer_id)
    json_result = get_request(url_with_id)
    # - Parse JSON results into a DealerView object list
    dealer = json_result
    # For each dealer in the response
    for dealer in dealer:
        print(dealer)
        dealer_doc = dealer
        # Create a CarDealer object with values in `doc` object
        dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
            id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
            short_name=dealer_doc["short_name"],
            st=dealer_doc["st"], zip=dealer_doc["zip"])
        results.append(dealer_obj)

    return results

# - Parse JSON results into a CarDealer object list
def get_dealer_reviews_from_cf(url, dealer_id):
    result = []
    json_result = get_request(url, dealerId=dealer_id)
    
    if json_result:
        reviews = json_result
        for single_review in reviews:
            # Creating a review object using the .get() method to avoid KeyError
            dealer_review = DealerReview(
                id=single_review.get('id', ''),
                name=single_review.get('name', ''),
                dealership=single_review.get('dealership', ''),
                review=single_review.get('review', ''),
                purchase=single_review.get('purchase', False),
                purchase_date=single_review.get('purchase_date', ''),
                car_make=single_review.get('car_make', ''),
                car_model=single_review.get('car_model', ''),
                car_year=single_review.get('car_year', ''),
                sentiment=""
            )

            # Analyzing the sentiment of the review text and saving it to the object attribute "sentiment"
            dealer_review.sentiment = analyze_review_sentiments(dealer_review.review)

            # Saving the review object to the list of results
            result.append(dealer_review)
            print("DEALER REVIEW", dealer_review)
        
        return result

    else:
        print("No data received from GET request.")
        return []

# analyze_review_sentiments` method to call Watson NLU and analyze text
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative

def analyze_review_sentiments(dealer_review):
    body =  {"text": dealer_review, "features": {"sentiment": {"document": True}}}
    print(dealer_review)
    response = requests.post(
        service_creditentials["url"] + "/v1/analyze?version=2019-07-12", # watson_url
        header={"Content-Type": "application/json"},
        json=body,
        auth=HTTPBasicAuth("apikey", service_creditentials["apikey"]), # watson_api_key
    )

    # Check if request was successful
    # if response.status_code == 200:
    if response:
        # sentiment = response.json()["sentiment"]["document"]["label"]
        sentiment = "Test"
        return sentiment
    return "Request Unsucessful"