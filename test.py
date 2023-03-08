import requests
import json
import time

# set the base URL for the API endpoints
base_url = "http://127.0.0.1:5000"

sample_videos = ["https://storage.googleapis.com/sieve-public-videos/celebrity-videos/dwyane_basketball.mp4", 
                 "https://storage.googleapis.com/sieve-public-videos/celebrity-videos/obama_interview.mp4", 
                 "https://storage.googleapis.com/sieve-public-videos/celebrity-videos/elon_podcast.mp4"]

# test the /push endpoint
push_url = f"{base_url}/push"
for url in sample_videos:
    push_data = {"source_name": "test_video", "source_url": str(url)}
    push_response = requests.post(push_url, data=push_data)
    print('Status code:', push_response.status_code)
    print('Response content:', json.loads(push_response.content))

    # test the /status endpoint
    task_id = json.loads(push_response.content)["id"]
    status_url = f"{base_url}/status/{task_id}"
    status_response = requests.get(status_url)
    time.sleep(2)
    status = json.loads(status_response.content)
    print("Status Response:", status['status'])
    while status['status'] != "finished":
        status_response = requests.get(status_url)
        time.sleep(5)
        status = json.loads(status_response.content)
        print("Status Response:", status['status'])

    
    # test the /list endpoint
    list_url = f"{base_url}/list"
    list_response = requests.get(list_url)
    id_list = json.loads(list_response.content)
    print("List Response:", id_list)

    # test the /query endpoint
    query_url = f"{base_url}/query/{task_id}"
    query_response = requests.get(query_url)
    time.sleep(5)
    print("Query Response:", json.loads(query_response.content))

print("Test Completed")
