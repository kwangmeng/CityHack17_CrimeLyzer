import json
from urllib.request import urlopen
url = 'https://randomuser.me/api/?results=5'
response = urlopen(url).read().decode('utf8')
remote_data = json.loads(response)

image_list = []
for result in remote_data['results']:
    print(result['picture']['large'])
    image_list.append(result['picture']['large']);
