import socket
import json
import time
import threading
import random

# Function to send JSON logs to the server
def send_logs(logs):
    try:
        # Create a socket connection
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('localhost', 3000)
        client_socket.connect(server_address)

        # Convert logs to JSON string
        json_logs = json.dumps(logs)

        # Send the JSON logs to the server
        client_socket.sendall(json_logs.encode('utf-8'))
        print("Logs sent successfully.")

    except Exception as e:
        print(f"Error sending logs: {e}")

    finally:
        # Close the socket connection
        client_socket.close()

# Example JSON logs
# sample_logs = {
#     "level": "error",
#     "message": "Failed to connect to server",
#     "resourceId": "server-1237",
#     "timestamp": "2023-09-15T08:00:00Z",
#     "traceId": "abc-xyz-123",
#     "spanId": "span-456",
#     "commit": "5e5342f",
#     "metadata": {
#         "parentResourceId": "server-0987"
#     }
# }

level = ['error', 'warning']
message = ['Failed to connect to Server', 'Failed to connect to DB', 'Failed to connect to network']
month = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
date = month + list(range(13, 30))
hours = month + list(range(13, 25))
minute = month + list(range(13, 61))

class DummyServer(threading.Thread):
    def run(self):
        for _ in range(50):
            log_gen = dict()
            log_gen['level'] = level[random.randint(0, 1)]
            log_gen['message'] = message[random.randint(0, 2)]
            log_gen['resourceId'] = f'server-{random.randint(1100, 1200)}'
            log_gen['timestamp'] = f'{random.randint(2020, 2023)}-{month[random.randint(0, 11)]}-{date[random.randint(0, 29)]}T{hours[random.randint(0, 24)]}:{minute[random.randint(0, 59)]}:00Z'
            log_gen['traceId'] = f'abc-def{random.randint(111, 999)}'
            log_gen['spanId'] = f'span-{random.randint(111, 999)}'
            log_gen['commit'] = f'{random.randint(0,10)}abcdef'
            log_gen['metadata'] = {"parentResourceId" : f'server-{random.randint(1100, 1200)}'}
            
            send_logs(log_gen)
        

threads = []

# Number of dummy server that send log data
for _ in range(0, 10):
    thread = DummyServer()
    thread.start()
    threads.append(thread)
    
for thread in threads:
    thread.join()

print("All dummy server have finished to send their logs")