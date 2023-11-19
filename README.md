[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/2sZOX9xt)


# Log Aggregation and Viewing System

## Project Overview

The Log Aggregation and Viewing System is a comprehensive solution for collecting, storing, and visualizing log data from various servers. The system is built using MongoDB as the database, Flask as the backend framework in Python, and a web-based user interface employing HTML, CSS, JavaScript, and Bootstrap.

## Feature

### Log Aggregation Server (Python)

* Log Reception:
  * The Flask server is designed to accept log files from various servers through HTTP requests.
  * Logs are sent to the server's endpoint, typically at http://localhost:3000/.
  * Received log data in the format of JSON :
    ```
      {
          "level": "error",
          "message": "Failed to connect to DB",
          "resourceId": "server-1234",
          "timestamp": "2023-09-15T08:00:00Z",
          "traceId": "abc-xyz-123",
          "spanId": "span-456",
          "commit": "5e5342f",
          "metadata": {
            "parentResourceId": "server-0987"
          }
      }
    ```
* MongoDB Integration:
  * Log data is stored in MongoDB, providing a scalable and efficient solution for data storage
  * MongoDB connection details, such as the URI, are configurable in the server's settings. (constant.py)

### Web-based UI (HTML, CSS, JavaScript, Bootstrap)

* Log Viewing:
  * Users can view logs through an intuitive web interface.
  * Logs are displayed in a user-friendly format, making it easy to analyze information.

* Filtering and Searching:
  * Advanced filtering options allow users to narrow down logs based on various criteria such as level, message, resourceId, timestamp, traceId, spanId, commit, and metadata.parentResourceId.
  * A search functionality enables users to quickly find specific log entries.

* Responsive Design:
  * The user interface is designed using Bootstrap and is responsive, ensuring a seamless experience across different devices and screen sizes.
 

### Project Structure

* Log Ingestor (Python):
  * The Python module included in this project is responsible for receiving log files from various servers. It listens for incoming log data on port number 3000.
  * To use this module, ensure that your servers are configured to send log data to the designated endpoint, typically at http://localhost:3000.

* Backend (Flask):
  * The Flask server handles incoming log requests and interacts with MongoDB to store and retrieve log data.
  * Configuration files allow easy customization of server settings.

* Frontend (HTML, CSS, JavaScript, Bootstrap):
  * The web-based UI provides an interactive dashboard for users to explore and analyze log data.

* Database (MongoDB):
  * MongoDB is used to store log entries efficiently and provides a flexible schema for future expansion.

    
### Setup Instruction

1. Clone the repository
   ```
    git clone https://github.com/dyte-submissions/november-2023-hiring-voilentKiller0.git
   ```
2. Install required library
   ```
    pip install -r requirements.txt
   ```
3. Run the ingestor.py script to get log data.
   ```
    python ./ingestor.py
   ```
4. (Optional) Run dummyServers.py script to send the dummy log to the 3000 port number for getting dummy log data.
   ```
    python dummyServer.py
   ```
5. Run the app.py
   ```
    python app.py
   ```

### Sample Output

![image](https://github.com/dyte-submissions/november-2023-hiring-voilentKiller0/assets/55941465/aec86b79-2a30-484f-a3a5-7d6c4faf28b1)

![image](https://github.com/dyte-submissions/november-2023-hiring-voilentKiller0/assets/55941465/cf3e02df-fd60-40de-94a9-1a3225ea8ab3)


### Usage

1. Sending Logs:
   * Configure various servers to send logs to the Flask server endpoint.
    
2. Viewing Logs:
   * Explore logs using filtering and search features.

### Future Enhancements
  * Real-time log streaming.
  * Integration with external/internal authentication providers.
  * Enhanced visualization options for log data.
  * Efficient searching in NoSQL

### Contact Me

[LinkedIn](https://www.linkedin.com/in/chandreshwar-vishwakarma-a57588196/)
