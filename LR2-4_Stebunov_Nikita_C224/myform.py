# -*- coding: cp1251 -*-
from bottle import post, request, response
import re
from datetime import datetime
import pdb

@post('/home', method='post')
def my_form():
    # Создание словаря для хранения пар email-вопрос
    questions = {}

    # Получение данных из формы
    question = request.forms.get('QUEST', '').strip()
    email = request.forms.get('ADRESS', '').strip()
    username = request.forms.get('USERNAME', '').strip()
    
    # Проверка заполненности полей
    if not email or not username or not question:
        response.status = 400  # Установка статуса кода 400 для неверного запроса
        return "Все поля должны быть заполнены. Пожалуйста, заполните поля email, имя пользователя и вопрос."
    
    # Проверка максимальной длины email (не более 254 символов)
    if len(email) > 254:
        response.status = 400
        return "Email слишком длинный. Максимальная длина — 254 символа."

    # Список разрешенных доменов
    allowed_domains = ['gmail.com', 'mail.ru', 'inbox.ru', 'yandex.ru']
    
    # Паттерн для проверки адреса электронной почты
    domain_pattern = '|'.join(re.escape(domain) for domain in allowed_domains)
    pattern = rf'^[a-zA-Z0-9_.+-]+@({domain_pattern})$'
    
    # Проверка формата электронной почты
    if not re.match(pattern, email):
        # Установка статуса кода 400 для неверного запроса
        response.status = 400
        return "Неверный формат адреса электронной почты. Пожалуйста, попробуйте снова!"

    # Сохранение emailа и вопроса в словарь
    questions[email] = question

    # Получение текущей даты в формате YYYY-MM-DD
    access_date = datetime.now().strftime('%Y-%m-%d')
    
    # Использование pdb для отладки и проверки словаря
    print("Отладка началась:")
    pdb.set_trace()  # Установка точки останова для проверки словаря
    
    # Возвращение сообщения с именем пользователя и датой обращения
    return f"Спасибо, {username}!<br>Ответ будет отправлен на почту {email}.<br>Дата обращения: {access_date}"