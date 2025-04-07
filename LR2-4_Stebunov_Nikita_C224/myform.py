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

    # Проверка максимальной длины преддоменной части email (не более 64 символов)
    if '@' in email:  # Проверка, что символ '@' присутствует
        subject_part = email.split('@')[0]  # Извлечение части до '@'
        if len(subject_part) > 64:
            response.status = 400
            return "Преддоменная часть email слишком длинная. Максимальная длина — 64 символа."
    else:
        response.status = 400
        return "Email должен содержать символ '@'."

    # Проверка длины имени
    if len(username) < 3:
        response.status = 400
        return "Имя должно быть минимум из 3-x символов."

    # Проверка, что длина имени не слишком большая
    if len(username) >= 70:
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
    
    # Получение текущей даты в формате YYYY-MM-DD
    current_date = datetime.now().strftime('%Y-%m-%d')
    
    # Проверка, существует ли запись для этого email
    if email in questions:
        # Проверка, совпадает ли имя пользователя с именем, которое сохраненно для этого email
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

    pdb.set_trace()

    # Возвращение сообщения с именем пользователя и датой обращения
    return f"Спасибо, {username}!<br>Ответ будет отправлен на почту {email}.<br>Дата обращения: {current_date}"