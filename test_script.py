import requests


url = "http://localhost:5000/get_form"

# Замените f_name1, f_name2 и их значения на фактические данные
data = {
    # 'name': 'Жулик',
    # 'date': '2023-11-08',
    # 'phone': '+7 999 111 22 33',
    # 'email': 'email@mail.com',
    
    "f_name1": "+1 555 111 22 33",
    "f_name2": "sus@vich.ru",
    "f_name3": "Daddy",
    "f_name4": "2000-01-01"
}

headers = {'Content-Type': 'application/json'}
response = requests.post(url, json=data, headers=headers)

# Вывод ответа от сервера
print(response.text)
