from flask import Flask, render_template, request
from pymongo import MongoClient
import json
from datetime import datetime

from constant import (
    mongo_host,
    mongo_port,
    database_name,
    collection_name
)


# Create a MongoDB client
client = MongoClient(mongo_host, mongo_port)
db = client[database_name]
collection = db[collection_name]

app = Flask(__name__)


status = collection.find_one({"_id" : 1})


@app.route('/')
def home():
    levelType = ''
    messageType = ''
    resourceIdType = ''
    parentResourceIdType=''
    for level in status['levelType']:
        levelType += f'<option value="{level}">{level}</option> \n'
    for message in status['messageType']:
        messageType += f'<option value="{message}">{message}</option> \n'
    for resourceId in status['resourceIdType']:
        resourceIdType += f'<option value="{resourceId}">{resourceId}</option> \n'
    for parentResourceId in status['parentResourceIdType']:
        parentResourceIdType += f'<option value="{parentResourceId}">{parentResourceId}</option> \n'
        
        
    return render_template('index.html', levelType=levelType, messageType=messageType, resourceIdType=resourceIdType, parentResourceIdType=parentResourceIdType)

@app.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
        result = request.form
        query = { '_id': { '$ne': 1 }}
        
        if len(result.get('startdatetime')) == 0 and len(result.get('enddatetime')) == 0:
            for key, val in result.items():
                if len(val) > 0:
                    query[key] = val
        elif len(result.get('startdatetime')) > 0 and len(result.get('enddatetime')) > 0:
            for key, val in result.items():
                if len(val) == 0 or key != 'startdatetime' or key != 'enddatetime':
                    pass
                else:
                    query[key] = val
            start_timestamp = datetime.strptime(result.get('startdatetime')+":00Z", "%Y-%m-%dT%H:%M:%SZ")
            end_timestamp = datetime.strptime(result.get('enddatetime')+":00Z", "%Y-%m-%dT%H:%M:%SZ")
            query['timestamp'] = {'$gte' : start_timestamp, '$lt' : end_timestamp}
        else:
            return render_template('error.html')
        try:
            print (query)
            log_entries = collection.find(query)
            searchBy = ''
            
            for key, val in query.items():
                if key != '_id':
                    searchBy += f'{key}, '
                    
            searchBy = searchBy[:-2]
            
            return render_template('search_results.html', log_entries=log_entries, searchBy = searchBy)
        except Exception as e:
            print ("Error : ", e)
            return render_template('error.html')

if __name__ == '__main__':
    app.run(debug=True)