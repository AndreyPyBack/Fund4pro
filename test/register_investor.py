import requests


url = 'http://127.0.0.1:8000/api/register/investor/'

# Данные для регистрации инвестора
data = {
    'first_name': 'John',
    'last_name': 'Doeы',
    'email': 'email@454574545.com',
    'password': 'password',
    'password_confirmation': 'password',
    'interest_sectors': ['IT'],
    'investment_range': '100000-500000',
    'receive_interesting_offers': True
}

# Отправляем POST-запрос с данными в формате JSON
response = requests.post(url, json=data)

# Печатаем ответ сервера
print(response.status_code)
print(response.json())
