import requests

url = 'http://127.0.0.1:8000/api/register/businessman/'

data = {
    'email': 'valerashk3@gmail.com',
    'password': 'babacapa',
    'password_confirmation': 'babacapa',
    'interest_sectors': ['IT', 'Finance'],
    'business_range': 'yes',
    'receive_interesting_offers': True
}

response = requests.post(url, json=data)

print(response.status_code)
print(response.json())