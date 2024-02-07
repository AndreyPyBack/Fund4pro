import requests

# URL вашего API для регистрации инвестора
url = 'http://127.0.0.1:8000/api/interest-sectors/'


response = requests.get(url)

# Печатаем ответ сервера
print(response.status_code)
print(response.json())