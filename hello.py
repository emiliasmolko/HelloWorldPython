from cloudant import Cloudant
from cloudant.result import Result, ResultByKey
from cloudant.error import CloudantException
from cloudant.query import Query
from flask import Flask, render_template, request, jsonify
import atexit
import os
import json


app = Flask(__name__)
db_name = 'gamesdb'
client = None
db = None

if 'VCAP_SERVICES' in os.environ:
    vcap = json.loads(os.getenv('VCAP_SERVICES'))
    print('Found VCAP_SERVICES',vcap)
    if 'cloudantNoSQLDB' in vcap:
        print('Found VCAP_SERVICES',vcap['cloudantNoSQLDB'])
        creds = vcap['cloudantNoSQLDB'][0]['credentials']
        user = creds['username']
        password = creds['password']
        url = 'https://' + creds['host']
        client = Cloudant(user, password, url=url, connect=True)
        db = client.create_database(db_name, throw_on_exists=False)
elif os.path.isfile('vcap-local.json'):
    with open('vcap-local.json') as f:
        vcap = json.load(f)
        print('Found local VCAP_SERVICES')
        creds = vcap['services']['cloudantNoSQLDB'][0]['credentials']
        user = creds['username']
        password = creds['password']
        url = 'https://' + creds['host']
        client = Cloudant(user, password, url=url, connect=True)
        db = client.create_database(db_name, throw_on_exists=False)


# When running this app on the local machine, default the port to 8000
port = int(os.getenv('PORT', 8000))

@app.route('/')
def home():
    return render_template('index.html')
	
@app.route('/api/games', methods=['GET'])
def get_games():
    if client:
        text = request.args.get('text')
        query = None
        if text and len(text)>3:
            query = Query(db, selector={"$text": text})
        else:
            query = Query(db, selector={'_id': {"$gt": 0}})
        dataFromDb = [];
        for doc in query()['docs']:
            dataFromDb.append(doc);
            print(doc);
        return jsonify(dataFromDb);
    else:
        print('No database')
        return jsonify([])


@app.route('/api/games', methods=['POST'])
def put_game():
	if client:
		age_from = request.json['age_from']
		age_to = request.json['age_to']
		title = request.json['title']
		author = request.json['author']
		description = request.json['description']
		players_from = request.json['players_from']
		players_to = request.json['players_to']
		time_from = request.json['time_from']
		time_to = request.json['time_to']
	
		db.create_document({"age_from": age_from, "age_to": age_to, "author": author, 
		"description": description,"players_from": players_from, 
		"players_to": players_to, "time_from": time_from, 
		"time_to": time_to, "title": title
		})
		return 'Game ' +title+' saved in repository.'
	else:
		print('No database')
		return 'Do not have access to repository!'

@atexit.register
def shutdown():
    if client:
        client.disconnect()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)
