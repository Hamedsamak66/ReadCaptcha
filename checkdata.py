import requests

url = 'http://127.0.0.1:5000/predict'
files = {'file': open('labeling_project/image_labeler/static/images/7404_2_Left.png', 'rb')}
response = requests.post(url, files=files)
print(response.json())
        

    