# -*- coding: cp1251 -*-
from bottle import post, request, response
import re
from datetime import datetime
import pdb
import json
import os

JSON_FILE_NAME = 'questions.json'

# ������� ��� �������� ������ �� JSON-�����
def load_json_data():
    if os.path.exists(JSON_FILE_NAME):
        try:
            with open(JSON_FILE_NAME, 'r', encoding='utf-8') as json_file:
                # ������ �����, �������������� JSON � Python-������ (�������)
                return json.load(json_file)
        except FileNotFoundError:
            # ���� ��� ���� ������
            return {}
        except json.JSONDecodeError:
            # ��������� ������, ���� JSON-���� ��������� ��� ����
            print(f"������: ���� {JSON_FILE_NAME} �������� ������������ ��������� JSON. ������� ������� �������.")
            return {}
        except Exception as e:
            # ��������� ������ ������
            print(f"������ ��� ������ {JSON_FILE_NAME}: {str(e)}")
            return {}
    return {}

# ������� ��� ���������� ������ � JSON-����
def save_json_data(data):
    try:
        with open(JSON_FILE_NAME, 'w', encoding='utf-8') as json_file:
            # ���������� ������ � JSON
            json.dump(data, json_file, ensure_ascii=False, indent=4)
    except IOError:
        # ������ �����-������
        print(f"������ �����-������ ��� ������ � {JSON_FILE_NAME}.")
        raise
    except Exception as e:
        # ��������� ������ ������
        print(f"������ ��� ������ � {JSON_FILE_NAME}: {str(e)}")
        raise

# ������� ��� �������� ����� ������������
def validate_username(username):
    username = username.strip()
    if not username:
        return False, "��� �� ����� ���� ������."
    if any(char.isdigit() for char in username):
        return False, "��� �� ����� ��������� �����."
    # �������� �� ������������� ������ ���������� ���� � �������
    if not re.match(r'^[a-zA-Z-]+$', username):
        return False, "��� ������ ��������� ������ ���������� ����� � ������. ������� �������, � ���������, �� ��������������."
    letters_count = sum(char.isalpha() for char in username)
    if letters_count < 2:
        return False, "��� ������ ��������� ������� 2 �����."
    # ��������, ��� ����� ����� �� ������� �������
    if len(username) >= 70:
        return False, "���� ��� ������� �������."
    return True, username

# ������� ��� �������� ������ ����������� �����
def validate_email(email):
    email = email.strip()
    if not email:
        return False, "Email �� ����� ���� ������."
    # ��������, ��� ������ '@' ������������
    if '@' not in email:
        return False, "Email ������ ��������� ������ '@'."
    subject_part = email.split('@')[0]
    # �������� ����� ������������ ����� email (������� 3 �������, �������� 64 �������)
    if len(subject_part) < 3:
        return False, "������������ ����� email ������� ��������. ����������� ����� � 3 �������."
    if len(subject_part) > 64:
        return False, "������������ ����� email ������� �������. ������������ ����� � 64 �������."
    # ������ ����������� �������
    allowed_domains = ['gmail.com', 'mail.ru', 'inbox.ru', 'yandex.ru']
    # ������� ��� �������� ������ ����������� ����� (������ ���������� �������)
    domain_pattern = '|'.join(re.escape(domain) for domain in allowed_domains)
    pattern = rf'^[a-zA-Z0-9_.+-]+@({domain_pattern})$'
    if not re.match(pattern, email):
        return False, f"Email ������ ���� �� ���������� ����� � ��������������� ������� (��������, user@gmail.com). ���������� ������: {', '.join(allowed_domains)}."
    return True, email

# ������� ��� �������� �������
def validate_question(question):
    question = question.strip()
    if not question:
        return False, "������ �� ����� ���� ������."
    # ��������, ��� ������ �� ������� ������ �� ����
    if question.isdigit():
        return False, "������ �� ����� �������� ������ �� ����."
    # �������� �� ������������� ������ ���������� ����, ���� � ��������
    if not re.match(r'^[a-zA-Z0-9\s.,!?+-]+$', question):
        return False, "������ ������ ��������� ������ ���������� �����, ����� � �������. ������� �������, � ���������, �� ��������������."
    letters_count = sum(char.isalpha() for char in question)
    if letters_count < 3:
        return False, "������ ������ ��������� ������� 3 �����."
    # �������� ����� ��� �������
    if len(question) <= 3:
        return False, "������ ������ ��������� ����� 3 ��������."
    # ��������, ��� ����� ������� �� ������� �������
    if len(question) >= 1000:
        return False, "��� ������ ������� �������."
    return True, question

# ������� ��� ��������� POST-������� �� �����
@post('/home', method='post')
def my_form():
    # ��������� ������ �� �����
    question = request.forms.get('QUEST', '').strip()
    email = request.forms.get('ADRESS', '').strip()
    username = request.forms.get('USERNAME', '').strip()
    
    # �������� ������������� �����
    if not email or not username or not question:
        # ��������� ������� ���� 400 ��� ��������� �������
        response.status = 400
        return "��� ���� ������ ���� ���������. ����������, ��������� ���� email, ��� ������������ � ������."
    
    username_valid, username_result = validate_username(username)
    if not username_valid:
        # ��������� ������� ���� 400 ��� ��������� �������
        response.status = 400
        return username_result
    
    email_valid, email_result = validate_email(email)
    if not email_valid:
        # ��������� ������� ���� 400 ��� ��������� �������
        response.status = 400
        return email_result
    
    question_valid, question_result = validate_question(question)
    if not question_valid:
        # ��������� ������� ���� 400 ��� ��������� �������
        response.status = 400
        return question_result
    
    # �������� ������� ������ �� �����
    questions = load_json_data()
    
    # ��������� ������� ���� � ������� YYYY-MM-DD
    current_date = datetime.now().strftime('%Y-%m-%d')
    
    # ��������, ���������� �� ������ ��� ����� email
    if email in questions:
        # ��������, ��������� �� ��� ������������ � ������, ������� ��������� ��� ����� email
        if questions[email]["username"] != username:
            response.status = 400
            return "��� ������������ �� ��������� � ���������� email."
        # ��������, ���������� �� ��� ���� ������ � ������������ (���������� �� ����)
        for date, question_list in questions[email]["questions_by_date"].items():
            # ������ �� ���� ����� � ������� �������� ��� ����� email
            if question in question_list:
                response.status = 400
                return "���� ������ ��� ��� ����� ����� ���� �������������."
        # ���� ������� ���, ���������� ��� � ������� ����
        if current_date in questions[email]["questions_by_date"]:
            questions[email]["questions_by_date"][current_date].append(question)
        else:
            questions[email]["questions_by_date"][current_date] = [question]
    else:
        # �������� ����� ������
        questions[email] = {
            "username": username,
            "questions_by_date": {
                current_date: [question]
            }
        }
    
    # ���������� ����������� ������
    save_json_data(questions)
    
    # ����������� ��������� � ������ ������������ � ����� ���������
    return f"�������, {username}!<br>����� ����� ��������� �� ����� {email}.<br>���� ���������: {current_date}"