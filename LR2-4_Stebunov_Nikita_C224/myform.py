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

    # �������� ������������ ����� ������������ ����� email (�� ����� 64 ��������)
    if '@' in email:  # ��������, ��� ������ '@' ������������
        subject_part = email.split('@')[0]  # ���������� ����� �� '@'
        if len(subject_part) > 64:
            response.status = 400
            return "������������ ����� email ������� �������. ������������ ����� � 64 �������."
    else:
        response.status = 400
        return "Email ������ ��������� ������ '@'."

    # �������� ����� �����
    if len(username) < 3:
        response.status = 400
        return "��� ������ ���� ������� �� 3-x ��������."

    # ��������, ��� ����� ����� �� ������� �������
    if len(username) >= 70:
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
    
    # ��������� ������� ���� � ������� YYYY-MM-DD
    current_date = datetime.now().strftime('%Y-%m-%d')
    
    # ��������, ���������� �� ������ ��� ����� email
    if email in questions:
        # ��������, ��������� �� ��� ������������ � ������, ������� ���������� ��� ����� email
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

    pdb.set_trace()

    # ����������� ��������� � ������ ������������ � ����� ���������
    return f"�������, {username}!<br>����� ����� ��������� �� ����� {email}.<br>���� ���������: {current_date}"