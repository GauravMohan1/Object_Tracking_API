## Documentation

The following sections will explain how to install and interact with the Objectc Tracking Engine

## Installation
We will be using Redis in this project.
Redis requires [brew](https://brew.sh/) to install.

Install Redis.
```sh
brew install redis
```
#### 1. Install redis. 
```bash
brew install redis
```
#### 2. You can also download redis directly from the following link: http://download.redis.io/redis-stable.tar.gz
#### 3. The next step is to create a virtual environment to run the application.
  - Make sure you have a python version >= 3.7. Run the following lines in terminal to create a virtual environment.
```bash
python -m venv venv
source venv/bin/activate
```
#### 4. Once the venv has been activated run the following command to get all the dependancies. 
```bash
pip install -r requirements.txt
```
#### 5. After the dependencies have been installed, start the Redis db
```bash
redis-server
```
#### 6. In a separate terminal window navigate to the project directory with the venv activated. Start up the Celery worker process that listens for tasks on the Celery queue.
```bash
celery -A main.celery worker --loglevel=info
```
#### 7. Finally in a different terminal window navigate to the project directory, activate the venv, and run. This will run the Flask application. 
- Navigate to http://127.0.0.1:5000/ to interact with the front-end. 
```bash
python main.py
```
## Inference
#### 1. Input a URL and provide a source name and submit the request. 
#### 2. This will make a call to the **/push** endpoint and add the celery task to a table underneath along with a status.
#### 3. The status updates as the process function runs by making continuous calls to the **/status** endpoint until the task finishes. 
#### 4. When the process is completed click the <u>Task Results</u> link to see the output from the object tracking. This will make a call to the **/query** endpoint to check if the task is successful and return the data output in a separate task-specific page with the taskId and a scrollable box with the object tracking results. 
#### 5. Click back on the browser to navigate back to the home page to submit more requests or view the results of a different task. You may need to reload the browser to update the status.
#### 6. The results output is formatted as a dictionary with the keys being the unique identifier assigned to objects from SORT pointing to an inner list of dictionaries sorted by each frame the object is detected in (ascending) along with the class labels and bounding box values. Here is an example output for one frame of an object.
```python
{"23.0": [
        {
            "class": "person",
            "frame_number": 0,
            "positions": {
                "x1": 530.0,
                "x2": 611.0,
                "y1": 1163.0,
                "y2": 1541.0
            }
        },
        ...
        ]}
```

## Testing
#### To test the functionality of each endpoint in a separate terminal run:
```bash
python test.py
```
##### This will iteratively submit each of the sample video urls to the flask app and test each of the endpoints for each url that is processed and print out the response for each endpoint request.
