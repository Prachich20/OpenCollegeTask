from flask import request
import requests
import json
import os

flickr_api = 'https://www.flickr.com/services/rest/?method=flickr.photos.search'
# key = os.environ['API_KEY']
key = '8bb681989754de8208c7a3d6b0416f55'


class Common:

    def favorites(self, fav_latitude, fav_longitude):
        """method to add favorites"""
        url_ = request.args.get('url')
        json_object = {
            "url": url_,
            "latitude": fav_latitude,
            "longitude": fav_longitude,
        }
        with open('favorites.json') as f:
            data = json.load(f)
        data["favorites"].append(json_object)
        with open('favorites.json', 'w') as f:
            json.dump(data, f)
        f.close()

    def flickr(self, latitude, longitude, page):
        """method to pull data from flickr"""
        payload = {
            "lat": latitude,
            "lon": longitude,
            "format": 'json',
            "nojsoncallback": 1,
            "per_page": 10,
            "page": page
        }
        response = requests.get(flickr_api + "&api_key=" + key, params=payload)
        if response.status_code == 200:
            if 'message' in response.json():
                return response.json()["message"]  # No photos
            else:
                return response.json()["photos"]
        else:
            return response.json()["message"]  # error message
