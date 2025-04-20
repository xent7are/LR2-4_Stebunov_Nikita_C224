# -*- coding: cp1251 -*-
import unittest
from myform import validate_email

# ������������ �������� ����������� �����
class TestEmailValidation(unittest.TestCase):
    
    # ���� ��� �������� ������������ email
    def test_F_mail(self):
        # ������ ������������ email ��� ������������
        list_mail_uncor = [
            # ������������ ����� ����������� �����
            "",                         # ������ ������
            "            ",             # ������ �� ��������
            "a" * 250 + "@gmail.com",   # ������� email (> 254 ��������)
            "@mail.ru",                 # ��� ������������ �����
            "ns@mail.ru",               # �������� ������������ ����� (2 �������)
            "a" * 65 + "@mail.ru",      # ������� ������������ ����� (> 64 ��������)
            "nikita.stebunov14@m.ru",   # �������� �������� ����� (3 �������)
            "test.email@" + "a" * 200 + ".com",  # ������� �������� ����� (> 190 ��������)
            
            # �������� ������� '@'
            "nikitamail.ru",            # ��� ������� @

            # �������� ������
            "nikita@GUAP.com",          # �������������� �����
            "StebunovN@gmail.ru",       # �������������� �����
            "nik14@GMAIL.COM",          # ��������� ����� � ������

            # �������� ������� ����������� �����
            "nikita@@gmail.com",        # ��� '@' ������
            "nik@stebunov@mail.ru",     # ������ '@' � ������������ �����
            "������@gmail.com",         # ���� ������� �������
            "Stebunov nik@gmail.com",   # ���� �������
            "Nikita#224@yandex,ru"      # ������������ �������
        ]
        
        # ������ �� ������� email � ������ ������������ email
        for email in list_mail_uncor:
            # ���������� �������� �������� � ��������� �� �������
            is_valid, message = validate_email(email)
            # ��������, ��� ������� ���������� False (email ���������)
            self.assertFalse(is_valid)


    # ���� ��� �������� ���������� email
    def test_T_mail(self):
        # ������ ������������ email ��� ������������
        list_mail_cor = [
            # ������� ���������� ����������� �����
            "nikita@gmail.com",             # ������� email � ����������� ������������ ������ (3 �������)
            "nikita.stebunov@mail.ru",      # Email � ������ � ������� mail.ru
            "user123@inbox.ru",             # Email � ������� � ������� inbox.ru
            "test.user@yandex.ru",          # Email � ������ � ������� yandex.ru
            
            # ����������� ����� � ���������� ����������� ���������
            "nikita_stebunov@gmail.com",    # ������������ ����� � ��������������
            "nikita-stebunov@mail.ru",      # ������������ ����� � �������
            "nikita+stebunov@inbox.ru",     # ������������ ����� � ������
            "n1k1t4.st3bun0v@yandex.ru",    # ������������ ����� � ������� � ������
            
            # ��������� ������
            "nik" + "a" * 61 + "@mail.ru",  # ������������ ����� ������������ ����� (64 �������)
            
            # �������� �������
            "nikita.stebunov@inbox.ru",     # ����� �� ������������ ������
            "stebunov.nik@yandex.ru"        # ������ ����� �� ������������ ������
        ]
        
        # ������ �� ������� email � ������ ���������� email
        for email in list_mail_cor:
            # ���������� �������� �������� � ��������� �� �������
            is_valid, message = validate_email(email)
            # ��������, ��� ������� ���������� True (email �������)
            self.assertTrue(validate_email(email))

# ��������, ������� �� ���� ��������
if __name__ == '__main__':
    # ������ ���� ������ � ������
    unittest.main()