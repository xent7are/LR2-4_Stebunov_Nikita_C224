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
            json.dump(data, json_file, ensure_ascii=False, indent=4)
    except IOError:
        # ������ �����-������
        print(f"������ �����-������ ��� ������ � {JSON_FILE_NAME}.")
        raise
    except Exception as e:
        # ��������� ������ ������
        print(f"������ ��� ������ � {JSON_FILE_NAME}: {str(e)}")
        raise

@post('/home', method='post')
def my_form():
    # ��������� ������ �� �����
    question = request.forms.get('QUEST', '').strip()
    email = request.forms.get('ADRESS', '').strip()
    username = request.forms.get('USERNAME', '').strip()
    
    # �������� ������������� �����
    if not email or not username or not question:
        response.status = 400  # ��������� ������� ���� 400 ��� ��������� �������
        return "��� ���� ������ ���� ���������. ����������, ��������� ���� email, ��� ������������ � ������."
    
    # �������� ������������ ����� email (�� ����� 254 ��������)
    if len(email) > 254:
        response.status = 400
        return "Email ������� �������. ������������ ����� � 254 �������."

    # �������� ����� �����
    if len(username) < 3:
        response.status = 400
        return "��� ������ ���� ������� �� 3-x ��������."

    # ��������, ��� ����� ����� �� ������� �������
    if len(question) >= 70:
        response.status = 400
        return "���� ��� ������� �������."

    # ������ ����������� �������
    allowed_domains = ['gmail.com', 'mail.ru', 'inbox.ru', 'yandex.ru']
    
    # ������� ��� �������� ������ ����������� �����
    domain_pattern = '|'.join(re.escape(domain) for domain in allowed_domains)
    pattern = rf'^[a-zA-Z0-9_.+-]+@({domain_pattern})$'
    
    # �������� ������� ����������� �����
    if not re.match(pattern, email):
        # ��������� ������� ���� 400 ��� ��������� �������
        response.status = 400
        return "�������� ������ ������ ����������� �����. ����������, ���������� �����!"

    # �������� ����� ��� �������
    if len(question) <= 3:
        response.status = 400
        return "������ ������ ��������� ����� 3 ��������."
    
    # ��������, ��� ����� ������� �� ������� �������
    if len(question) >= 1000:
        response.status = 400
        return "��� ������ ������� �������."
    
    # ��������, ��� ������ �� ������� ������ �� ����
    if question.isdigit():
        response.status = 400
        return "������ �� ����� �������� ������ �� ����."

    # �������� ������� ������ �� �����
    questions = load_json_data()
    
    # �������� ������� � ������� ������ �������
    new_question = {"question": question, "username": username, "date": datetime.now().strftime('%Y-%m-%d')}
    
    # ��������, ���� �� ��� ������ ��� ����� email � �������
    if email in questions:
        for q in questions[email]:
            if q["question"] == question:
                response.status = 400
                return "���� ������ ��� ��� ����� �����."
        questions[email].append(new_question)
    else:
        questions[email] = [new_question]
    
    # ���������� ����������� ������
    save_json_data(questions)

    # ��������� ������� ���� � ������� YYYY-MM-DD
    access_date = datetime.now().strftime('%Y-%m-%d')
    
    # ����������� ��������� � ������ ������������ � ����� ���������
    return f"�������, {username}!<br>����� ����� ��������� �� ����� {email}.<br>���� ���������: {access_date}"