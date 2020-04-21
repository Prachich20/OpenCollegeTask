import json
from utilities import Common
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
app.debug = True
parsed_locations = json.load(open('locations.json'))['locations']


@app.route('/', methods=['GET'])
def dropdown():
    """method to fill dropdown"""
    locations = Common().load(parsed_locations)
    return render_template('index.html', locations_data=locations)


@app.route('/add', methods=['GET'])
def add_location():
    """method to view favorites"""
    lat = request.args.get('latitude')
    long = request.args.get('longitude')
    name = request.args.get('name')
    json_object = {
        "name": name,
        "latitude": lat,
        "longitude": long,
    }
    with open('locations.json') as f:
        data = json.load(f)
        if not any(d['name'] == name for d in data['locations']):
            data["locations"].append(json_object)
            with open('locations.json', 'w') as f:
                json.dump(data, f)
            f.close()
    locations = Common().load(data['locations'])
    return render_template('index.html', locations_data=locations)


@app.route("/getphotos/<pagenumber>/", methods=['GET'])
def getPhotos(pagenumber):
    """method to search photos by location"""
    location = request.args.get('locations')
    if request.args.get('locations') is not None:
        parsed_locations = json.load(open('locations.json'))['locations']
        lat = [item['latitude'] for item in parsed_locations if item['name'] == location]
        long = [item['longitude'] for item in parsed_locations if item['name'] == location]
    else:
        lat = request.args.get('latitude')
        long = request.args.get('longitude')

    if request.args.get('favorite'):
        # method to add favorites
        Common().favorites(fav_latitude=lat, fav_longitude=long)

    data = Common().flickr(lat, long, pagenumber)
    geo = {
        'latitude': lat,
        'longitude': long,
        'location': location
    }
    if "photo" in data:
        for item in data["photo"]:
            item["url"] = 'http://farm' + str(item['farm']) + '.static.flickr.com/' + item['server'] + '/' + \
                          str(item['id']) + '_' + item['secret'] + '_m.jpg'
        return render_template('images.html', photos_data=data["photo"], page=data["page"], geo=geo)
    else:
        return render_template('images.html', message=data, page=0, geo=geo)


@app.route('/favorites', methods=['GET'])
def favorite():
    """method to view favorites"""
    with open('favorites.json') as f:
        fav_json = json.load(f)
        fav_lst = list(fav_json['favorites'])
    f.close()
    return render_template('favorites.html', fav=fav_lst)


if __name__ == "__main__":
    app.run()
