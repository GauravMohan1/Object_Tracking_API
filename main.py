from flask import Flask, jsonify, request, render_template
from celery import Celery
from celery.result import AsyncResult
from celery import app

import cv2
import torch
from sort import Sort
import numpy as np
import requests
import time
import json
import redis

app = Flask(__name__)

redis_client = redis.Redis(host='localhost', port=6379, db=0)


app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379'
app.debug = True


celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'], backend=app.config['CELERY_RESULT_BACKEND'])
celery.conf.update(app.config)

@celery.task()
def process(video_url):
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
    tracker = Sort()

    response = requests.get(str(video_url))
    with open('video.mp4', 'wb') as f:
        f.write(response.content)
    cap = cv2.VideoCapture('video.mp4')

    frame_count = 0
    video_dict = {}
    while True: 
        ret, frame = cap.read()
        if not ret:
            break


        results = model(frame, size=640)
        outputs = results.pandas().xyxy[0]

        bboxes = outputs[['xmin', 'ymin', 'xmax', 'ymax']].values
        class_names = outputs['name'].tolist()

        tracked_objects = tracker.update(bboxes)

        for obj, class_name in zip(tracked_objects, class_names):
            key = str(obj[4])
            if key in video_dict:
                new_dict = {
                    "class": class_name,
                    "frame_number": frame_count,
                    "positions": {
                        "x1": round(obj[0], 0),
                        "x2": round(obj[2], 0),
                        "y1": round(obj[1], 0),
                        "y2": round(obj[3], 0),
                    }
                }
                video_dict[key].append(new_dict)
            else:
                video_dict[key] = [
                    {
                        "class": class_name,
                        "frame_number": frame_count,
                        "positions": {
                            "x1": round(obj[0], 0),
                            "x2": round(obj[2], 0),
                            "y1": round(obj[1], 0),
                            "y2": round(obj[3], 0),
                        }
                    }
                ]
        frame_count += 1
    
    cap.release()
    cv2.destroyAllWindows()
    return video_dict

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/push', methods=['POST'])
def push():
    source_name = request.form['source_name']
    video_url = request.form['source_url']
    task = process.delay(video_url)
    return {'id': task.id, 'status': 'queued', 'source_name': source_name}, 202


@app.route('/status/<string:task_id>', methods=['GET'])
def task_status(task_id):
    result = AsyncResult(task_id, app=celery)
    status = None
    if result.ready():
        if result.successful():
            status = 'finished'
        else:
            status = 'error'
    else:
        status = 'processing'

    return jsonify({'status': status})

@app.route('/query/<string:task_id>', methods=['GET'])
def get_video_results(task_id):
    result = AsyncResult(task_id, app=celery)
    if result.ready():
        if result.successful():
            results = result.result
            response = json.dumps(results, indent=4)
        else:
            response = {'error': 'Task failed'}
    else:
        response = {'status': 'Task pending'}
    return response

@app.route('/list', methods=['GET'])
def list():
    ids = []
    task_ids = redis_client.keys("celery-task-meta-*")
    # Print the task IDs
    for task_id in task_ids:
        task = str(task_id.decode('utf-8'))
        task = task.split('celery-task-meta-')[1]
        ids.append(task)
    return ids

@app.route('/results/<task_id>', methods=['GET'])
def get_results(task_id):
    results = get_video_results(task_id)

    return render_template('results.html', task_id=task_id, results=results)

# define routes and functions for each endpoint here

if __name__ == '__main__':
    app.run(debug=True)
