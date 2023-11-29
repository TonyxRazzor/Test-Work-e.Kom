from tinydb import TinyDB


db = TinyDB('database.json')

def populate_database():
    db.insert({'name': 'Template 1', 'email': 'email@example.com', 'phone': '+7234567890', 'date': '2022-01-01'})
    db.insert({'name': 'Template 2', 'email': 'email@example.com', 'phone': '+7987654321', 'date': '2022-02-02'})
    db.insert({'name': 'Template 3', 'email': 'email@example.com', 'phone': '+7876543210', 'date': '2022-03-03'})
    db.insert({'name': 'Template 4', 'email': 'email@example.com', 'phone': '+7876543210', 'date': '2022-04-04'})


populate_database()  # Вызов функции для наполнения базы данных