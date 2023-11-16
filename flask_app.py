from flask import Flask, jsonify, request, render_template
import json
from geopy.distance import geodesic

app = Flask(__name__)

# Load the data from the JSON file
with open('data.json') as f:
    data = json.load(f)

# GET all links
@app.route('/')
def get_links():
    return render_template('index.html')

# POST new location to the given car
@app.route('/data/<int:car_id>', methods=['POST'])
def post_location(car_id):
    # Get the request data
    location = request.get_json()
    # Find the car with the given ID
    car = next((car for car in data['cars'] if car['id'] == car_id), None)
    if car:
        # Add the new location to the car's locations list
        car['locations'].append(location)
        # Write the updated data to the JSON file
        with open('data.json', 'w') as f:
            json.dump(data, f, indent=4)
        return jsonify({'message': 'Location added successfully.'}), 200
    else:
        return jsonify({'error': 'Car not found.'}), 404

# POST a new car to the data.json file
@app.route('/data/cars', methods=['POST'])
def post_car():
    # Get the request data
    car = request.get_json()
    # Add the new car to the data
    data['cars'].append(car)
    # Write the updated data to the JSON file
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)
    return jsonify({'message': 'Car added successfully.'}), 200

# GET a map of all the locations in order for a given car
@app.route('/map/id/<int:car_id>')
def map(car_id):
    with open('data.json') as f:
        data = json.load(f)
    for car in data['cars']:
        if car['id'] == car_id:
            coordinates = [location['coordinates'] for location in car['locations']]
            print(coordinates)
            break
    return render_template('map.html', coordinates=coordinates)

# GET a map of the latest locations of all cars
@app.route('/map/latest')
def get_latest_map():
    # Get the latest location of each car
    latest_locations = []
    for car in data['cars']:
        latest_location = max(car['locations'], key=lambda x: x['timestamp'])
        latest_locations.append({'latitude': latest_location['coordinates']['latitude'], 'longitude': latest_location['coordinates']['longitude']})
    print(latest_locations)
    return render_template('map.html', coordinates=latest_locations)

# GET the furthest location from a hardcoded one for all cars
@app.route('/map/furthest')
def get_furthest_map():
    # Hardcoded location
    reference_location = (37.7749, -122.4194)
    # Get the furthest location of each car
    furthest_locations = []
    for car in data['cars']:
        furthest_location = max(car['locations'], key=lambda x: geodesic(reference_location, (x['coordinates']['latitude'], x['coordinates']['longitude'])).km)
        furthest_locations.append({'latitude': furthest_location['coordinates']['latitude'], 'longitude': furthest_location['coordinates']['longitude']})
    return render_template('map.html', coordinates=furthest_locations)

if __name__ == '__main__':
    app.run(debug=True)
