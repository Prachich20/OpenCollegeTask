import json
from utilities import favorites, flickr
from flask import Flask, render_template, request

app = Flask(__name__)
app.debug = True

parsed_json = json.load(open('locations.json'))


@app.route('/', methods=['GET'])
def dropdown():
    """method to fill dropdown"""
    locations = []
    for item in parsed_json['locations']:
        locations.append(item)
    locations.append('Select location')
    return render_template('index.html', locations_data=locations)


@app.route("/getphotos/<pagenumber>/", methods=['GET'])
def getPhotos(pagenumber):
    """method to search photos by location"""
    if (request.args.get('Latitude') != '' and request.args.get('Longitude') != '') or (request.args.get('locations') == ''):
        latitude = request.args.get('Latitude')
        longitude = request.args.get('Longitude')
    elif request.args.get('locations') != '':
        latitude = [item['latitude'] for item in parsed_json['locations'] if
                    item['name'] == request.args.get('locations')]
        longitude = [item['longitude'] for item in parsed_json['locations'] if
                     item['name'] == request.args.get('locations')]
    data = flickr(latitude, longitude, pagenumber)

    if request.args.get('favorite'):
        # method to add favorites
        favorites()

    if "photo" in data:
        for item in data["photo"]:
            item["url"] = 'http://farm' + str(item['farm']) + '.static.flickr.com/' \
                          + item['server'] + '/' + str(item['id']) + '_' + item['secret'] + '_m.jpg'
        return render_template('images.html', photos_data=data["photo"], page=data["page"], latitude=latitude, longitude=longitude)
    else:
        return render_template('images.html', message=data, page=0, latitude=latitude, longitude=longitude)


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