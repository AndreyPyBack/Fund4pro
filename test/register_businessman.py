import requests

# URL для регистрации бизнесмена
url = 'http://127.0.0.1:8000/api/businessman/register/'

# Данные для регистрации бизнесмена
data = {
    'email': 'businessman@example.com',
    'password': 'password123',
    'password_confirmation': 'password123',
    'interest_sectors': ['IT', 'Finance'],
    'business_range': 'yes',
    'receive_interesting_offers': True
}

# Отправка POST-запроса
response = requests.post(url, json=data)

# Печать ответа сервера
print(response.status_code)
print(response.json())
