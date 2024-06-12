from cloudant.client import Cloudant
from cloudant.query import query
from flask import Flask, jsonify, request
import atexit
from dotenv import load_dotenv, dotenv_values

load_dotenv()

cloudant_username = CLOUDANT_USERNAME
cloudant_api_KEY = IAM_API_KEY
cloudant_url = CLOUDANT_URL
client = Cloudant.iam(cloudant_username, cloudant_api_KEY, connect=TRUE, url=cloudant_url)

session = client.session()
print('Databases:', client.all.dbs())

db = client['reviews']

app = Flask(__name__)

@app.route('/api/get_reviews', methods=['GET'])
def get_reviews():
    dealership_id = request.args.get('id')

    # Check for "id" parameter
    if dealership_id is None:
        return jsonify({"error": "Missing 'id' parameter must be an interger"}), 400

    # Convert "id" parameter to an interger
    try:   
        dealership_id = int(dealership_id)
    except ValueError:
        return jsonify({"error": "'id' parameter must be a interger"}), 400

    # Define the query based on the 'dealership' ID
    selector = {
        'dealership': dealership_id
    }

    # Execute the query using the query method
    result = db.get_query_result(selector)

    # Create a list to store the documents
    data_list = []

    # Iterate through the results and add documents to the list
    for doc in result:
        data_list.append(doc)

    # Return the data as JSON
    return jsonify(data_list)

@app.route('/api/post_review', methods=['POST'])
def post_review():
    if not request.json:
        abort(400, desription='Invalid JSON data')

    # Extract review data from request JSON
    review_data = request.json
    
    # Validate review data from request JSON
    required_fields = ['id', 'name', 'dealership', 'review', 'purchase', 'purchase_date', 'car_make', 'car_model', 'car_year']
    for field in required_fields:
        if field not in review_data:
            abort(400, desription="f'Missing required field: {field}'")
        
    # Save the review data as a new document in the Cloudant database
    db.create_document(review_data)

    return jsonify("message": "Review posted sucessfully"), 201

if __name__ == '__main__':
    app.run(debug=True)