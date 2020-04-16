from flask import request
import requests
import json
import os

flickr_api = 'https://www.flickr.com/services/rest/?method=flickr.photos.search'


def favorites():
    """method to add favorites"""
    json_object = {
        "url": request.args.get('url'),
        "latitude": request.args.get('Latitude'),
        "longitude": request.args.get('Longitude'),
    }
    with open('favorites.json') as f:
        data = json.load(f)
    data["favorites"].append(json_object)
    with open('favorites.json', 'w') as f:
        json.dump(data, f)
    f.close()


def flickr(latitude, longitude, page):
    """method to pull data from flickr"""
    payload = {
        "lat": latitude,
        "lon": longitude,
        "format": 'json',
        "nojsoncallback": 1,
        "per_page": 10,
        "page": page
    }
    response = requests.get(flickr_api + "&api_key=" + os.environ['API_KEY'], params=payload)
    if response.status_code == 200:
        if 'message' in response.json():
            return response.json()["message"]
        else:
            return response.json()["photos"]
    else:
        return response.json()["message"]
