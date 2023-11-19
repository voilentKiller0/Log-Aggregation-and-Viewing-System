import socket
import json
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import cpu_count
import pymongo
from pymongo import MongoClient
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

status = None

# Whenever i got new type related to level, message and resourceId 
def information_update(log_entry):
    if log_entry['level'] not in status['levelType']:
        status['levelType'].append(log_entry['level'])
        collection.update_one({"_id" : 1}, {'$set' : {'levelType' : status['levelType']}})
        
    if log_entry['message'] not in status['messageType']:
        status['messageType'].append(log_entry['message'])
        collection.update_one({"_id" : 1}, {'$set' : {'messageType' : status['messageType']}})
        
    if log_entry['resourceId'] not in status['resourceIdType']:
        status['resourceIdType'].append(log_entry['resourceId'])
        collection.update_one({"_id" : 1}, {'$set' : {'resourceIdType' : status['resourceIdType']}})
        
    if log_entry['metadata']['parentResourceId'] not in status['parentResourceIdType']:
        status['parentResourceIdType'].append(log_entry['metadata']['parentResourceId'])
        collection.update_one({"_id" : 1}, {'$set' : {'parentResourceIdType' : status['parentResourceIdType']}})
        
        
        

# Function to handle incoming logs and save them to MongoDB
def handle_logs(data):
    try:
        # Assuming logs are in JSON format
        
        log_entry = json.loads(data)
        log_entry['timestamp'] = datetime.strptime(log_entry["timestamp"], "%Y-%m-%dT%H:%M:%SZ")
        
        if isinstance(log_entry, dict):
            # Update the information if new status is come
            information_update(log_entry)
            # Save log entry to MongoDB            
            collection.insert_one(log_entry)
            print("Log entry saved successfully.")
        else:
            print("Error: Log entry is not a dictionary.")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    except Exception as e:
        print(f"Error saving log entry to MongoDB: {e}")
        
        
        
# If first time collection is created then create an information that uses later
# If already present then fetch that information
if collection_name not in db.list_collection_names():
    collection.create_index([('level', pymongo.TEXT)])
    collection.create_index([('message', pymongo.HASHED)])
    collection.create_index([('resourceId', pymongo.HASHED)])
    collection.create_index([('metadata.parentResourceId', pymongo.HASHED)])
    collection.create_index([('timestamp', pymongo.ASCENDING)])
    data = {
        "_id" : 1,
        "levelType": [],
        "messageType": [],
        "resourceIdType": [],
        "parentResourceIdType" : []
    }
    collection.insert_one(data)
    
    status = data
else:
    status = collection.find_one({"_id" : 1})
    
    
    
# Function to handle a client connection
def handle_client(connection, address):
    try:
        print(f"Connection from {address}")
        # Receive the data in chunks
        data = ""
        while True:
            chunk = connection.recv(1024)
            if not chunk:
                break
            data += chunk.decode('utf-8')

        # Handle the received logs
        if data:
            handle_logs(data)
    finally:
        # Clean up the connection
        connection.close()

# Create a socket to listen on port 3000
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 3000)
server_socket.bind(server_address)
server_socket.listen(5)

print(f"Listening on port 3000...")

try:
    # Use a ThreadPoolExecutor for handling multiple connections concurrently
    print (cpu_count())
    with ThreadPoolExecutor(max_workers=cpu_count()) as executor: 
        while True:
            # Wait for a connection
            print("Waiting for a connection...")
            connection, client_address = server_socket.accept()
            
            # Submit the connection handling to the executor
            executor.submit(handle_client, connection, client_address)

except KeyboardInterrupt:
    print("Server shutting down.")
finally:
    # Close the server socket
    server_socket.close()
    # Close the MongoDB connection
    client.close()
  