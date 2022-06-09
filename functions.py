import hashlib
import re
import random
import string

import openpyxl.styles
from openpyxl import Workbook

def encrypt_password(password: str):
    t = hashlib.sha256(password.encode())
    return t.hexdigest()


def is_correct_password(password: str):
    return bool(re.search(r"^[A-Za-z0-9]{6,}$", password))


def generate_code(length: int):
    values = [i for i in string.digits + string.ascii_letters]
    for i in range(4):
        random.shuffle(values)
    return ''.join([random.choice(values) for i in range(length)])


def print_profile(profile):
    cols = ('Имя', 'Фамилия', 'Дата рождения', 'Email', 'Роль')
    text = ''
    for key, value in zip(cols, profile):
        text += f'[{key}]: {value}\n-----\n'
    return text


def print_lessons(lessons):
    text = ''
    if len(lessons[0]) > 2:
        for i in lessons:
            l = '\n'.join(i[1].split('&'))
            text += f"""

[📍]
Секция: {i[0]}
Преподаватель: {i[2]} {i[3]}
График:
{l}
            """
    else:
        for i in lessons:
            l = '\n'.join(i[1].split('&'))
            text += f"""
[📍]
Секция: {i[0]}
График:
{l}
            """

    return text

def print_reports(reports):
    text = ''

    for i in reports:
        text += f"""
=========================
📫
[Номер репорта]: {i[0]}
[Пользователь]:
    - ID: {i[1]}
    - {i[2]} {i[3]}
    - {i[4]}
    
[Сообщение]:

{i[5]}

[Дата отправки]: {i[6]}
=========================
        """
    return text


def print_report_by_id(report):
    text = ''

    for i in (report,):
        text += f"""
📫
[ID репорта]: {i[0]}
[Пользователь]:
    - ID: {i[1]}
    - {i[2]} {i[3]}
    - {i[7]}
    - {i[4]}

[Сообщение]:

{i[5]}
[Дата]: {i[6]}
        """
    return text

def print_my_answers(reports):
    text = ''
    if len(reports) == 0:
        text = 'Ваши вопросы не найдены!'
        return text
    for i in reports:
        if i[3] == None:
            text += f"""
----------
[⛔ Вопрос не решён]
{i[1]} 
Отправлено: {i[2]}"""
        else:
            text += f"""
----------
[✅ Вопрос решён]
{i[1]} 
Отправлено: {i[2]}

[Ответ]
{i[4]}

Администратор: {i[5]} {i[6]}"""
    return text

def print_tutors(tutors):
    text = ''
    prev = ''
    for i in tutors:
        tutor_id = i[1]
        if tutor_id != prev:
            text += f"""
            
📍
[{i[2]} {i[3]}]
    - ID: {i[1]}
    - {i[4]}
    - {i[0]}"""
        else:
            text += f", {i[0]}"
        prev = tutor_id
    return text

def generate_excel(contracts, user_tg):
    filename = 'excels\\' + str(user_tg) + '.xlsx'

    wb = Workbook()
    ws = wb.active
    cols, conts = contracts

    ws.append(cols)

    for i in conts:
        ws.append(i)
    wb.save(filename)

    return filename

