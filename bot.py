import requests
import json
import datetime

params = (
    ('user_id', 'me'),
    ('tenant_id', '17a13ee4-2d0c-438e-978e-56efe5ec4948'),
    ('sport_id', 'PADEL'),
    ('local_start_min', '2021-03-09T00:00:00'),
    ('local_start_max', '2021-03-09T23:59:59'),
)

# response = requests.get('https://playtomic.io/api/v1/availability', headers=headers, params=params)
response = requests.get('https://playtomic.io/api/v1/availability', params=params)

print(json.dumps(response.json(), indent=4))

with open('response.txt', 'w') as outfile:
    json.dump(response.json(), outfile, indent=4)

