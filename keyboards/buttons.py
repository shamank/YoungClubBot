from aiogram.types import KeyboardButton, InlineKeyboardButton

back_button = KeyboardButton('🔙 Назад')

register_button = KeyboardButton('✍ Регистрация')
login_button = KeyboardButton('🗝 Вход')

section_apply = KeyboardButton('📄 Вступить в секцию')

edit_button = KeyboardButton('✏ Изменить (вернуться назад)')
accept_button = KeyboardButton('✅ Подтвердить')
cancel_button = KeyboardButton('❌ Отменить')

# student
profile_button = KeyboardButton('🧑‍💻 Профиль')
report_button = KeyboardButton('📎 Задать вопрос / сообщить об ошибке')
show_answers = KeyboardButton('📖 Просмотреть ответы')

my_objects = KeyboardButton('⏰ Мои занятия')
sign_up_for_the_section = KeyboardButton('🖋 Записаться в секцию')


# tutor
my_lessons = KeyboardButton('⏰ Мои предметы')
send_all = KeyboardButton('Всем')

send_alert = KeyboardButton('📢 Создать объявление')

# admin
work_with_tutors = KeyboardButton('👨🏻‍🏫 Преподаватели')
work_with_students = KeyboardButton('👨🏻‍🎓 Ученики')
work_with_reports = KeyboardButton('🔬 Репорты')

check_contracts = KeyboardButton('📖 Просмотреть контракты')

show_all_tutors = KeyboardButton('🧾 Показать всех преподавателей')
show_all_students = KeyboardButton('🧾 Показать всех учеников')

add_tutor = KeyboardButton('Назначить')
delete_tutor = KeyboardButton('Убрать')
add_to_section = KeyboardButton('Добавить на секцию')



setting_button = KeyboardButton('⚙ Настроить профиль')
show_timetables_button = KeyboardButton('📃 Просмотр графика занятий')


change_firstname = KeyboardButton('Изменить имя')
change_lastname = KeyboardButton('Изменить фамилию')
change_birtday = KeyboardButton('Изменить дату рождения')
change_email = KeyboardButton('Изменить почту')
change_password = KeyboardButton('Изменить пароль')
exit_from_account = KeyboardButton('Выйти из аккаунта')

inline_bt_1 = InlineKeyboardButton(text='<<', callback_data='rep-back-0')
inline_bt_2 = InlineKeyboardButton('Ответить', callback_data='rep-answer-0')
inline_bt_3 = InlineKeyboardButton('>>', callback_data='rep-next-0')
