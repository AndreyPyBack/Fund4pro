import requests

# URL для логина пользователя
url = 'http://127.0.0.1:8000/api/login/'

# Данные для аутентификации пользователя
data = {
    'email': 'admin',
    'password': '315920it'
}

# Отправка POST-запроса
response = requests.post(url, json=data)

# Печать ответа сервера
print(response.status_code)
print(response.json())
