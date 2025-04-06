# -*- coding: cp1251 -*-
from bottle import post, request, response
import re
from datetime import datetime
import pdb

@post('/home', method='post')
def my_form():
    # �������� ������� ��� �������� ��� email-������
    questions = {}

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

    # ���������� email� � ������� � �������
    questions[email] = question

    # ��������� ������� ���� � ������� YYYY-MM-DD
    access_date = datetime.now().strftime('%Y-%m-%d')
    
    # ������������� pdb ��� ������� � �������� �������
    print("������� ��������:")
    pdb.set_trace()  # ��������� ����� �������� ��� �������� �������
    
    # ����������� ��������� � ������ ������������ � ����� ���������
    return f"�������, {username}!<br>����� ����� ��������� �� ����� {email}.<br>���� ���������: {access_date}"