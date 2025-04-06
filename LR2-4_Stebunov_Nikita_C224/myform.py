from bottle import post, request, response
import re
from datetime import datetime

@post('/home', method='post')
def my_form():
    
    # ��������� ������ �� �����
    question = request.forms.get('QUEST', '').strip()
    email = request.forms.get('ADRESS', '').strip()
    username = request.forms.get('USERNAME', '').strip()
    
     # �������� ������������� �����
    if not email or not username or not question:
        response.status = 400  # ��������� ������� ���� 400 ��� ��������� �������
        return "All fields must be filled in. Please fill in the email, username, and question fields."
    
    # �������� ������������ ����� email (�� ����� 254 ��������)
    if len(email) > 254:
        response.status = 400
        return "Email is too long. Maximum length is 254 characters."

    # ������ ����������� �������
    allowed_domains = ['gmail.com', 'mail.ru', 'inbox.ru', 'yandex.ru']
    
    # ������� ��� �������� ������ ����������� �����
    domain_pattern = '|'.join(re.escape(domain) for domain in allowed_domains)
    pattern = rf'^[a-zA-Z0-9_.+-]+@({domain_pattern})$'
    
    # �������� ������� ����������� �����
    if not re.match(pattern, email):
        # ��������� ������� ���� 400 ��� ��������� �������
        response.status = 400
        return "Incorrect email address format. Please try again!"

    # ��������� ������� ���� � ������� YYYY-MM-DD
    access_date = datetime.now().strftime('%Y-%m-%d')

     # ����������� ��������� � ������ ������������ � ����� ���������
    return f"Thanks, {username}!<br>The answer will be sent to the mail {email}.<br>Access Date: {access_date}"