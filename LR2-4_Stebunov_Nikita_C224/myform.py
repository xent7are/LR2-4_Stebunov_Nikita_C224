# -*- coding: cp1251 -*-
from bottle import post, request, response
import re
from datetime import datetime
import pdb
import json
import os

JSON_FILE_NAME = 'questions.json'

# Функция для загрузки данных из JSON-файла
def load_json_data():
    if os.path.exists(JSON_FILE_NAME):
        try:
            with open(JSON_FILE_NAME, 'r', encoding='utf-8') as json_file:
                # Чтение файла, преобразование JSON в Python-объект (словарь)
                return json.load(json_file)
        except FileNotFoundError:
            # Файл мог быть удален
            return {}
        except json.JSONDecodeError:
            # Обработка случая, если JSON-файл поврежден или пуст
            print(f"Ошибка: файл {JSON_FILE_NAME} содержит некорректную структуру JSON. Возврат пустого словаря.")
            return {}
        except Exception as e:
            # Обработка других ошибок
            print(f"Ошибка при чтении {JSON_FILE_NAME}: {str(e)}")
            return {}
    return {}

# Функция для сохранения данных в JSON-файл
def save_json_data(data):
    try:
        with open(JSON_FILE_NAME, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
    except IOError:
        # Ошибка ввода-вывода
        print(f"Ошибка ввода-вывода при записи в {JSON_FILE_NAME}.")
        raise
    except Exception as e:
        # Обработка других ошибок
        print(f"Ошибка при записи в {JSON_FILE_NAME}: {str(e)}")
        raise

@post('/home', method='post')
def my_form():
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

    # Проверка длины имени
    if len(username) < 3:
        response.status = 400
        return "Имя должно быть минимум из 3-x символов."

    # Проверка, что длина имени не слишком большая
    if len(question) >= 70:
        response.status = 400
        return "Ваше имя слишком длинное."

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

    # Проверка длины для вопроса
    if len(question) <= 3:
        response.status = 400
        return "Вопрос должен содержать более 3 символов."
    
    # Проверка, что длина вопроса не слишком большая
    if len(question) >= 1000:
        response.status = 400
        return "Ваш вопрос слишком длинный."
    
    # Проверка, что вопрос не состоит только из цифр
    if question.isdigit():
        response.status = 400
        return "Вопрос не может состоять только из цифр."

    # Загрузка текущих данных из файла
    questions = load_json_data()
    
    # Создание словаря с данными нового вопроса
    new_question = {"question": question, "username": username, "date": datetime.now().strftime('%Y-%m-%d')}
    
    # Проверка, есть ли уже записи для этого email в словаре
    if email in questions:
        for q in questions[email]:
            if q["question"] == question:
                response.status = 400
                return "Этот вопрос уже был задан ранее."
        questions[email].append(new_question)
    else:
        questions[email] = [new_question]
    
    # Сохранение обновленных данных
    save_json_data(questions)

    # Получение текущей даты в формате YYYY-MM-DD
    access_date = datetime.now().strftime('%Y-%m-%d')
    
    # Возвращение сообщения с именем пользователя и датой обращения
    return f"Спасибо, {username}!<br>Ответ будет отправлен на почту {email}.<br>Дата обращения: {access_date}"