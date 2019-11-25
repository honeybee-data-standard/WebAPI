import flask
import json
from flask import request,jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    return "<h1>Bee Data Standard Example</h1>"

@app.route('/all',methods=['GET','POST'])
def api_all():
    if request.method == 'GET':
        with open('./BeeData.json', 'r') as jsonfile:
            data = jsonfile.read()
        obj = json.loads(data)
        return jsonify(obj)
    elif request.method == 'POST':
        data = request.get_json()
        
        apiaryID = data['apiary'][0]['apiaryID']
        beekeeperID = data['beekeeper']['beekeeperID']
        latitude = data['apiary'][0]['latitude']
        longitude = data['apiary'][0]['longitude']

        return '''
                The apiary ID is {}
                The beekeeper ID is {}
                The latitude is {}
                The longitude is {}'''.format(apiaryID, beekeeperID, latitude, longitude)
        
@app.route('/api/apiaries', methods=['GET'])
def api_apid():
    if 'apiaryID' in request.args:
        id = int(request.args['apiaryID'])
    else:
        return "Error: No id field provided. Please specify an id."
    with open('./BeeData.json', 'r') as jsonfile:
        data = jsonfile.read()
    obj = json.loads(data)
    results = []

    for x in range(len(obj)):
        d = obj[x]["apiary"]
        for i in range(len(d)):
            if d[i]["apiaryID"] == id:
                results.append(d[i])
    if len(results) == 0:
        return "Apiary ID does not exist"
    return jsonify(results)

@app.route('/api/beekeepers', methods=['GET'])
def api_beekid():
    if 'beekeeperID' in request.args:
        id = int(request.args['beekeeperID'])
    else:
        return "Error: No id field provided. Please specify an id."
    with open('./BeeData.json', 'r') as jsonfile:
        data = jsonfile.read()
    obj = json.loads(data)
    results = []
    for x in range(len(obj)):
        if obj[x]["beekeeper"]["beekeeperID"] == id:
            results.append(obj[x])
    return jsonify(results)

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

app.run()