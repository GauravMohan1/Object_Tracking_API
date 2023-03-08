# Object_Tracking_API

### How to Run
1. The first step is to install redis. On a mac system run "brew install redis"
2. Then unzip the files and navigate to the directory in terminal.
3. The next step is to create a virtual environment to run the application.
  - Make sure you have a python version >= 3.7
  - Run "python -m venv venv" to create a virtual environment within the folder
  - Run "source venv/bin/activate"
4. Once the venv has been activated run "pip install -r requirements.txt" to get all the packages
5. After the dependencies have been installed, run "redis-server" to start the Redis db
6. In a seperate terminal window navigate to the project directory run "source venv/bin/activate" and then run "celery -A main.celery worker --loglevel=info" This will start up the Celery worker process that listens for tasks on the Celery queue.
7. Finally in a different terminal window navigate to the project directory, activate the venv, and run "python main.py". This will run the Flask application. Navigate to "http://127.0.0.1:5000/" to interact with the front-end. 
8. Input a URL and provide a source name and submit the request. This will make a call to the '/push' endpoint and add the celery task to a table underneath along with a status that updates as the process function runs by making continuous calls to the '/status' endpoint until the task finishes. When the process is completed click the Task Results link to see the output from the object tracking. This will make a call to the '/query' endpoint to check if the task is successful and return the data output in a seperate task-specific page with the taskId and a scrollable box with the object tracking results. Click back on the browser to navigate back to the home page to submit more requests or view the results of a different task. You may need to reload the browser to update the status.
9. The results output is formatted as a dictionary with the keys being the unique idenitifier assigned to objects from SORT pointing to an inner list of dictionaries sorted by each frame the object is detected in (asceding) along with the class labels and bounding box values. Here is an example output for one frame of an object.
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
        
10. To test the functionality of each endpoint in a seperate terminal or within a python environment such as Visual Studio Code, run the "python test.py" This will iteratively submit each of the sample video urls to the flask app and test each of the endpoints for each url that is processed. 
