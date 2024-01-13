import frappe
import googlemaps
import requests
import time


# Define the API endpoint URL
url = 'https://maps.googleapis.com/maps/api/geocode/json'
endpoint = 'https://maps.googleapis.com/maps/api/place/textsearch/json'


# Define API key (replace with your actual API key)
api_key = "YOUR_API_KEY"

# create a object
gmaps = googlemaps.Client(key=api_key)

# function that retrieve city name following street address(5 city name)
@frappe.whitelist()
def mapss(user_inputs=None):
	data = []
	try:
		place_result = gmaps.places_autocomplete(input_text=user_inputs, offset=None , 
												 types="street_address",components={"country": ["AU"]}, language='en')
		for place in place_result:
				des = place["description"]
				city_names = des.split(',')[1].strip()
				data.append(city_names)
        
	except googlemaps.exceptions.ApiError as e:
		if 'INVALID_REQUEST' in str(e):
			print("please! check your input")
		
	return data

@frappe.whitelist()
def places(user_input=None):
    params = {
              'query':user_input,
              'key': api_key
       }
    all_places = []
    adrs = []
    response = requests.get(endpoint, params = params)
    data = response.json()
    places = data.get('results', [])
    all_places.extend(places)
    for plc in all_places:
          address = plc.get('formatted_address')
          city_names = address.split(',')[1].strip()
          adrs.append(city_names)
    return adrs

# places(user_input='32 revees street')


# function that retrieve post code following city name. 
@frappe.whitelist()
def mapess(usr_inp=None):
    try:
        place_result = gmaps.places_autocomplete(usr_inp, offset=None, 
                                                    components= {'country': ['AU']}, radius=50000, language='en')
        for entry in place_result:
            placeid = entry['place_id']

        params = {
            "place_id": placeid,
            "key": api_key
        }
        response = requests.get(url, params=params)
        data = response.json()
        for comp in data['results'][0]['address_components']:
            postal_code = comp['short_name']

        
    except googlemaps.exceptions.ApiError as e:
        if 'INVALID_REQUEST' in str(e):
            print("Nai")

    return postal_code


