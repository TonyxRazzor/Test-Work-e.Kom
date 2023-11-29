from flask import Flask, request, jsonify, render_template, redirect
from tinydb import TinyDB
import phonenumbers
import re
import datetime


app = Flask(__name__)

db = TinyDB('database.json')



# Пример тестовой базы данных с шаблонами форм
db.insert({
    "name": "MyForm",
    "user_name": "text",
    "email": "email"
})

db.insert({
    "name": "OrderForm",
    "order_date": "date",
    "phone": "phone",
    "product_name": "text"
})

def find_matching_template(db, form_data):
    for template in db.all():
        matching_fields = {field: template[field] for field in form_data if field in template}
        if matching_fields:
            return template

    return None

def validate_and_type_fields(form_data):
    typed_fields = {}
    for field, value in form_data.items():
        if field_type := validate_date(value):
            typed_fields[field] = field_type
        elif field_type := validate_phone(value):
            typed_fields[field] = field_type
        elif field_type := validate_email(value):
            typed_fields[field] = field_type
        else:
            typed_fields[field] = "text"
    print(f"Validated and typed fields: {typed_fields}")
    return typed_fields

def validate_date(date):
    date_formats = ['%d.%m.%Y', '%Y-%m-%d']
    for fmt in date_formats:
        try:
            # Попробуем распарсить дату для каждого формата
            datetime.datetime.strptime(date, fmt)
            return 'date'
        except ValueError:
            pass
    return None


def validate_phone(phone):
    # Удаление пробелов из номера телефона
    phone = phone.replace(" ", "")
    print(f"Phone after removing spaces: {phone}")
    
    try:
        parsed_phone = phonenumbers.parse(phone, "RU")
        print(f"Parsed phone: {parsed_phone}")
        return "phone"  # Вернуть "phone" независимо от действительности номера
    except phonenumbers.NumberParseException:
        return None




def validate_email(email):
    # Простая проверка email с использованием регулярного выражения
    email_pattern = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
    return "email" if email_pattern.match(email) else None

def parse_request_data(request):
    try:
        if request.method == 'POST':
            if request.content_type == 'application/json':
                return request.get_json(force=True)
            elif request.form:
                return request.form.to_dict()
        elif request.method == 'GET':
            return request.args.to_dict()
    except Exception as e:
        print(f"Failed to parse request data: {e}")
        return {}

@app.route('/get_form', methods=['POST', 'GET'])
def get_form():
    if request.method == 'POST':
        try:
            form_data = request.get_json(force=True)
        except Exception as e:
            print(f"Failed to parse JSON: {e}")
            form_data = request.form.to_dict()
    else:
        form_data = request.args.to_dict()
    
    data = form_data
    
    # Поиск совпадающего шаблона формы
    best_matching_template = None
    best_matching_score = 0

    for template in db.all():
        template_fields = {key: template[key] for key in template.keys() if key != 'name'}
    
        matching_score = sum(
            key in data and (
                (key == 'date' and validate_date(data[key]) == 'date') or
                (key == 'phone' and validate_phone(data[key]) == 'phone') or
                (key == 'email' and validate_email(data[key]) == 'email') or
                (key == 'text')
            )
            for key in template_fields if template_fields[key] is not None
        )
    
        if matching_score > best_matching_score:
            best_matching_score = matching_score
            best_matching_template = template['name']

    # Если совпадающий шаблон найден, вернуть его имя
    if best_matching_template:
        return jsonify({'template_name': best_matching_template})

    # Если совпадений нет, произвести типизацию полей
    field_types = {}
    for field, value in data.items():
        current_field_type = None
        if validate_date(value):
            current_field_type = 'date'
        elif validate_phone(value):
            print(f"Valid phone number: {value}")
            current_field_type = 'phone'
        elif validate_email(value):
            current_field_type = 'email'
        else:
            current_field_type = 'text'
        field_types[field] = current_field_type

    # Если типы полей определены, вернуть их
    if field_types:
        return jsonify(field_types)

    # В противном случае вернуть сообщение об отсутствии данных
    return jsonify({'message': 'No matching template or field types found'})



@app.route('/templates', methods=['GET'])
def view_templates():
    templates = db.all()
    return render_template('templates.html', templates=templates)

@app.route('/add_template', methods=['GET', 'POST'])
def add_template():
    if request.method == 'POST':
        new_template = {
            'name': request.form.get('name'),
            'date': request.form.get('date'),
            'phone': request.form.get('phone'),
            'email': request.form.get('email')
            # Добавьте поля в соответствии с вашими требованиями
            }
        db.insert(new_template)
        return redirect('/templates')
    return render_template('add_template.html')

@app.route('/edit_template/<int:template_id>', methods=['GET', 'POST'])
def edit_template(template_id):
    template = db.get(doc_id=template_id)
    if template is None:
        # Если шаблон не найден, вернуть ошибку 404
        return render_template('404.html'), 404

    if request.method == 'POST':
        # Обновите поля в соответствии с вашими требованиями
        updated_fields = {
        'name': request.form.get('name'),
        'date': request.form.get('date'),
        'phone': request.form.get('phone'),
        'email': request.form.get('email')
        }
        db.update(updated_fields, doc_ids=[template_id])
        print(f"Updated Fields: {updated_fields}")
        return redirect('/templates')
    return render_template('edit_template.html', template=template)

if __name__ == '__main__':
    app.run(debug=True)
