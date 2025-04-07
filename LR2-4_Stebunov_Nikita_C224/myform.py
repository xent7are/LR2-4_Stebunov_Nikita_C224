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
            # Сохранение данных в JSON
            json.dump(data, json_file, ensure_ascii=False, indent=4)
    except IOError:
        # Ошибка ввода-вывода
        print(f"Ошибка ввода-вывода при записи в {JSON_FILE_NAME}.")
        raise
    except Exception as e:
        # Обработка других ошибок
        print(f"Ошибка при записи в {JSON_FILE_NAME}: {str(e)}")
        raise

# Функция для проверки имени пользователя
def validate_username(username):
    username = username.strip()
    if not username:
        return False, "Имя не может быть пустым."
    if any(char.isdigit() for char in username):
        return False, "Имя не может содержать цифры."
    # Проверка на использование только английских букв и дефисов
    if not re.match(r'^[a-zA-Z-]+$', username):
        return False, "Имя должно содержать только английские буквы и дефисы. Русские символы, к сожалению, не поддерживаются."
    letters_count = sum(char.isalpha() for char in username)
    if letters_count < 2:
        return False, "Имя должно содержать минимум 2 буквы."
    # Проверка, что длина имени не слишком большая
    if len(username) >= 70:
        return False, "Ваше имя слишком длинное."
    return True, username

# Функция для проверки адреса электронной почты
def validate_email(email):
    email = email.strip()
    if not email:
        return False, "Email не может быть пустым."
    # Проверка, что символ '@' присутствует
    if '@' not in email:
        return False, "Email должен содержать символ '@'."
    subject_part = email.split('@')[0]
    # Проверка длины преддоменной части email (минимум 3 символа, максимум 64 символа)
    if len(subject_part) < 3:
        return False, "Преддоменная часть email слишком короткая. Минимальная длина — 3 символа."
    if len(subject_part) > 64:
        return False, "Преддоменная часть email слишком длинная. Максимальная длина — 64 символа."
    # Список разрешенных доменов
    allowed_domains = ['gmail.com', 'mail.ru', 'inbox.ru', 'yandex.ru']
    # Паттерн для проверки адреса электронной почты (только английские символы)
    domain_pattern = '|'.join(re.escape(domain) for domain in allowed_domains)
    pattern = rf'^[a-zA-Z0-9_.+-]+@({domain_pattern})$'
    if not re.match(pattern, email):
        return False, f"Email должен быть на английском языке и соответствовать формату (например, user@gmail.com). Допустимые домены: {', '.join(allowed_domains)}."
    return True, email

# Функция для проверки вопроса
def validate_question(question):
    question = question.strip()
    if not question:
        return False, "Вопрос не может быть пустым."
    # Проверка, что вопрос не состоит только из цифр
    if question.isdigit():
        return False, "Вопрос не может состоять только из цифр."
    # Проверка на использование только английских букв, цифр и символов
    if not re.match(r'^[a-zA-Z0-9\s.,!?+-]+$', question):
        return False, "Вопрос должен содержать только английские буквы, цифры и символы. Русские символы, к сожалению, не поддерживаются."
    letters_count = sum(char.isalpha() for char in question)
    if letters_count < 3:
        return False, "Вопрос должен содержать минимум 3 буквы."
    # Проверка длины для вопроса
    if len(question) <= 3:
        return False, "Вопрос должен содержать более 3 символов."
    # Проверка, что длина вопроса не слишком большая
    if len(question) >= 1000:
        return False, "Ваш вопрос слишком длинный."
    return True, question

# Функция для обработки POST-запроса от формы
@post('/home', method='post')
def my_form():
    # Получение данных из формы
    question = request.forms.get('QUEST', '').strip()
    email = request.forms.get('ADRESS', '').strip()
    username = request.forms.get('USERNAME', '').strip()
    
    # Проверка заполненности полей
    if not email or not username or not question:
        # Установка статуса кода 400 для неверного запроса
        response.status = 400
        return "Все поля должны быть заполнены. Пожалуйста, заполните поля email, имя пользователя и вопрос."
    
    username_valid, username_result = validate_username(username)
    if not username_valid:
        # Установка статуса кода 400 для неверного запроса
        response.status = 400
        return username_result
    
    email_valid, email_result = validate_email(email)
    if not email_valid:
        # Установка статуса кода 400 для неверного запроса
        response.status = 400
        return email_result
    
    question_valid, question_result = validate_question(question)
    if not question_valid:
        # Установка статуса кода 400 для неверного запроса
        response.status = 400
        return question_result
    
    # Загрузка текущих данных из файла
    questions = load_json_data()
    
    # Получение текущей даты в формате YYYY-MM-DD
    current_date = datetime.now().strftime('%Y-%m-%d')
    
    # Проверка, существует ли запись для этого email
    if email in questions:
        # Проверка, совпадает ли имя пользователя с именем, которое сохранено для этого email
        if questions[email]["username"] != username:
            response.status = 400
            return "Имя пользователя не совпадает с владельцем email."
        # Проверка, существует ли уже этот вопрос у пользователя (независимо от даты)
        for date, question_list in questions[email]["questions_by_date"].items():
            # Проход по всем датам и спискам вопросов для этого email
            if question in question_list:
                response.status = 400
                return "Этот вопрос уже был задан ранее этим пользователем."
        # Если вопроса нет, добавление его в текущую дату
        if current_date in questions[email]["questions_by_date"]:
            questions[email]["questions_by_date"][current_date].append(question)
        else:
            questions[email]["questions_by_date"][current_date] = [question]
    else:
        # Создание новой записи
        questions[email] = {
            "username": username,
            "questions_by_date": {
                current_date: [question]
            }
        }
    
    # Сохранение обновленных данных
    save_json_data(questions)
    
    # Возвращение сообщения с именем пользователя и датой обращения
    return f"Спасибо, {username}!<br>Ответ будет отправлен на почту {email}.<br>Дата обращения: {current_date}"