from bottle import post, request, response
import re
from datetime import datetime

@post('/home', method='post')
def my_form():
    
    # Получение данных из формы
    question = request.forms.get('QUEST', '').strip()
    email = request.forms.get('ADRESS', '').strip()
    username = request.forms.get('USERNAME', '').strip()
    
     # Проверка заполненности полей
    if not email or not username or not question:
        response.status = 400  # Установка статуса кода 400 для неверного запроса
        return "All fields must be filled in. Please fill in the email, username, and question fields."
    
    # Проверка максимальной длины email (не более 254 символов)
    if len(email) > 254:
        response.status = 400
        return "Email is too long. Maximum length is 254 characters."

    # Список разрешенных доменов
    allowed_domains = ['gmail.com', 'mail.ru', 'inbox.ru', 'yandex.ru']
    
    # Паттерн для проверки адреса электронной почты
    domain_pattern = '|'.join(re.escape(domain) for domain in allowed_domains)
    pattern = rf'^[a-zA-Z0-9_.+-]+@({domain_pattern})$'
    
    # Проверка формата электронной почты
    if not re.match(pattern, email):
        # Установка статуса кода 400 для неверного запроса
        response.status = 400
        return "Incorrect email address format. Please try again!"

    # Получение текущей даты в формате YYYY-MM-DD
    access_date = datetime.now().strftime('%Y-%m-%d')

     # Возвращение сообщения с именем пользователя и датой обращения
    return f"Thanks, {username}!<br>The answer will be sent to the mail {email}.<br>Access Date: {access_date}"