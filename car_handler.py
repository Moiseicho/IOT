import threading
import requests
import time
import random
from datetime import datetime

# Define the base URL for the API
BASE_URL = 'http://localhost:5000'

# Define the number of threads to create
NUM_THREADS = 3

# Define the radius around Sofia
SOFIA_CENTER = (42.6977, 23.3219)
SOFIA_RADIUS = 0.1 # in degrees

# Define the function to send a POST request to create a new car and add a new location to it
def create_car_and_add_location():
    # Define the request data
    car_id = random.randint(1, 1000)
    car = {
        'id': car_id,
        'locations': [{
            'coordinates': {
                'longitude': SOFIA_CENTER[1] + random.uniform(-SOFIA_RADIUS, SOFIA_RADIUS),
                'latitude': SOFIA_CENTER[0] + random.uniform(-SOFIA_RADIUS, SOFIA_RADIUS)
            },
            'timestamp': datetime.utcnow().isoformat(),
            'device_id': f'{car_id}'
        }]
    }
    # Send the POST request
    response = requests.post(f'{BASE_URL}/data/cars', json=car)
    if response.status_code == 200:
        print(f'Car created successfully with id {car_id}.')
    else:
        print(f'Error creating car with id {car_id}.')
        
    time.sleep(120)
    while True:
        # Define the request data
        location = {
            'coordinates': {
                'longitude': SOFIA_CENTER[1] + random.uniform(-SOFIA_RADIUS, SOFIA_RADIUS),
                'latitude': SOFIA_CENTER[0] + random.uniform(-SOFIA_RADIUS, SOFIA_RADIUS)
            },
            'timestamp': datetime.utcnow().isoformat(),
            'device_id': f'{car_id}'
        }
        # Send the POST request
        response = requests.post(f'{BASE_URL}/data/{location["device_id"]}', json=location)
        if response.status_code == 200:
            print(f'Location added successfully for car with id {car_id}.')
        else:
            print(f'Error adding location for car with id {car_id}.')
        # Wait for 2 minutes before adding new locations
        time.sleep(120)

if __name__ == '__main__':
    # Create the threads
    threads = []
    for i in range(NUM_THREADS):
        thread = threading.Thread(target=create_car_and_add_location)
        threads.append(thread)
        thread.start()
    # Wait for the threads to finish
    for thread in threads:
        thread.join()
