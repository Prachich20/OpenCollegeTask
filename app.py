import json
from utilities import Common
from flask import Flask, render_template, request

app = Flask(__name__)
app.debug = True

parsed_locations = json.load(open('locations.json'))['locations']


@app.route('/', methods=['GET'])
def dropdown():
    """method to fill dropdown"""
    locations = []
    for item in parsed_locations:
        locations.append(item)
    locations.append('Select location')
    return render_template('index.html', locations_data=locations)


@app.route("/getphotos/<pagenumber>/", methods=['GET'])
def getPhotos(pagenumber):
    """method to search photos by location"""
    location = request.args.get('locations')
    if request.args.get('locations') is not None:
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
    fav_lst = []
    for item in fav_json['favorites']:
        fav_lst.append(item)
    f.close()
    return render_template('favorites.html', fav=fav_lst)


if __name__ == "__main__":
    app.run()
