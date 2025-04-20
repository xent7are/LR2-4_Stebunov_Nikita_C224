# -*- coding: cp1251 -*-
import unittest
from myform import validate_email

# Тестирование проверок электронной почты
class TestEmailValidation(unittest.TestCase):
    
    # Тест для проверки некорректных email
    def test_F_mail(self):
        # Список некорректных email для тестирования
        list_mail_uncor = [
            # Некорректная длина электронной почты
            "",                         # Пустая строка
            "            ",             # Строка из пробелов
            "a" * 250 + "@gmail.com",   # Длинный email (> 254 символов)
            "@mail.ru",                 # Нет преддоменной части
            "ns@mail.ru",               # Короткая преддоменная часть (2 символа)
            "a" * 65 + "@mail.ru",      # Длинная преддоменная часть (> 64 символов)
            "nikita.stebunov14@m.ru",   # Короткая доменная часть (3 символа)
            "test.email@" + "a" * 200 + ".com",  # Длинная доменная часть (> 190 символов)
            
            # Проверка наличия '@'
            "nikitamail.ru",            # Нет символа @

            # Проверка домена
            "nikita@GUAP.com",          # Несуществующий домен
            "StebunovN@gmail.ru",       # Несуществующий домен
            "nik14@GMAIL.COM",          # Заглавные буквы в домене

            # Проверка формата электронной почты
            "nikita@@gmail.com",        # Две '@' подряд
            "nik@stebunov@mail.ru",     # Символ '@' в преддоменной части
            "Никита@gmail.com",         # Есть русские символы
            "Stebunov nik@gmail.com",   # Есть пробелы
            "Nikita#224@yandex,ru"      # Недопустимые символы
        ]
        
        # Проход по каждому email в списке некорректных email
        for email in list_mail_uncor:
            # Извлечение булевого значения и сообщения из кортежа
            is_valid, message = validate_email(email)
            # Проверка, что функция возвращает False (email невалиден)
            self.assertFalse(is_valid)


    # Тест для проверки корректных email
    def test_T_mail(self):
        # Список некорректных email для тестирования
        list_mail_cor = [
            # Простые корректные электронные почты
            "nikita@gmail.com",             # Простой email с минимальной преддоменной частью (3 символа)
            "nikita.stebunov@mail.ru",      # Email с точкой и доменом mail.ru
            "user123@inbox.ru",             # Email с цифрами и доменом inbox.ru
            "test.user@yandex.ru",          # Email с точкой и доменом yandex.ru
            
            # Электронные почты с различными допустимыми символами
            "nikita_stebunov@gmail.com",    # Преддоменная часть с подчёркиванием
            "nikita-stebunov@mail.ru",      # Преддоменная часть с дефисом
            "nikita+stebunov@inbox.ru",     # Преддоменная часть с плюсом
            "n1k1t4.st3bun0v@yandex.ru",    # Преддоменная часть с цифрами и точкой
            
            # Граничные случаи
            "nik" + "a" * 61 + "@mail.ru",  # Максимальная длина преддоменной части (64 символа)
            
            # Проверка доменов
            "nikita.stebunov@inbox.ru",     # Домен из разрешенного списка
            "stebunov.nik@yandex.ru"        # Другой домен из разрешенного списка
        ]
        
        # Проход по каждому email в списке корректных email
        for email in list_mail_cor:
            # Извлечение булевого значения и сообщения из кортежа
            is_valid, message = validate_email(email)
            # Проверка, что функция возвращает True (email валиден)
            self.assertTrue(validate_email(email))

# Проверка, запущен ли файл напрямую
if __name__ == '__main__':
    # Запуск всех тестов в модуле
    unittest.main()