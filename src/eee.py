import os,json
path = os.path.join('../data/','user_settings.json')
with open (path, 'r') as file:
    data = json.load(file)
    print(data)
