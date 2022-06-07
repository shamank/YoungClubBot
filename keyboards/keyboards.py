from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup
import keyboards.buttons as bt

rm_kb = ReplyKeyboardRemove()

unlogin_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(bt.register_button, bt.login_button).add(bt.show_timetables_button)

login_menu_kb_unstudent = ReplyKeyboardMarkup(resize_keyboard=True).add(bt.profile_button, bt.setting_button).add(bt.show_timetables_button).add(bt.sign_up_for_the_section).add(bt.report_button, bt.show_answers)
login_menu_kb_student = ReplyKeyboardMarkup(resize_keyboard=True).add(bt.my_objects, bt.sign_up_for_the_section).add(bt.profile_button, bt.setting_button).add(bt.show_timetables_button).add(bt.report_button, bt.show_answers)
login_menu_kb_tutor = ReplyKeyboardMarkup(resize_keyboard=True).add(bt.my_lessons, bt.send_alert).add(bt.profile_button, bt.setting_button).add(bt.show_timetables_button).add(bt.report_button, bt.show_answers)
login_menu_kb_admin = ReplyKeyboardMarkup(resize_keyboard=True).add(bt.work_with_tutors, bt.send_alert, bt.work_with_reports).add(bt.profile_button, bt.setting_button).add(bt.show_timetables_button).add(bt.report_button, bt.show_answers)

login_menu = {
    '0': login_menu_kb_unstudent,
    'Новый пользователь': login_menu_kb_unstudent,

    '1': login_menu_kb_student,
    'Ученик': login_menu_kb_student,

    '2': login_menu_kb_tutor,
    'Преподаватель': login_menu_kb_tutor,

    '3': login_menu_kb_admin,
    'Администратор': login_menu_kb_admin,
}


def make_alert_kb(lessons) -> ReplyKeyboardMarkup:
    result = ReplyKeyboardMarkup(resize_keyboard=True).add(bt.send_all)
    for i in lessons:
        button = bt.KeyboardButton(i)
        result.add(button)
    return result


def make_sections_kb(lessons):
    result = ReplyKeyboardMarkup(resize_keyboard=True)
    for i in lessons:
        button = bt.KeyboardButton(i)
        result.add(button)
    return result

edit_accept_cancel_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(bt.edit_button).add(bt.accept_button, bt.cancel_button)
settings_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(bt.change_firstname, bt.change_lastname, bt.change_birtday).add(bt.change_email, bt.change_password).add(bt.exit_from_account, bt.back_button)

def make_tutors_with_email(tuple):
    result = ReplyKeyboardMarkup(resize_keyboard=True)
    for i in tuple:
        button = bt.KeyboardButton(i[0] + ' ' + i[1] + ' (' + i[2] + ')')
        result.add(button)
    return result

def generate_inline_kb(current_id):
    current_id = str(current_id)
    inline_bt_1 = bt.InlineKeyboardButton(text='<<', callback_data='rep_back_'+current_id)
    inline_bt_2 = bt.InlineKeyboardButton('Ответить', callback_data='rep_answer_'+current_id)
    inline_bt_3 = bt.InlineKeyboardButton('>>', callback_data='rep_next_'+current_id)
    return InlineKeyboardMarkup().add(inline_bt_1, inline_bt_2, inline_bt_3)


work_with_tutors = ReplyKeyboardMarkup(resize_keyboard=True).add(bt.add_tutor, bt.delete_tutor).add(bt.show_all_tutors).add(bt.add_to_section, bt.back_button)
accept_work_tutors = ReplyKeyboardMarkup(resize_keyboard=True).add(bt.send_alert)