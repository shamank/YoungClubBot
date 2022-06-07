import logging
from datetime import date

import aiogram.contrib.fsm_storage.memory
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from keyboards import keyboards
from config import BOT_TOKEN
from database import dbase
from functions import *
from states import *
import mail


# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
storage = aiogram.contrib.fsm_storage.memory.MemoryStorage()

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, storage=storage)

db = dbase()


# ______________________ [/info, /help] ______________________ #
@dp.message_handler(state='*', commands=['info', 'help'])
async def info(message: types.Message):
    text = """
Данный бот предназначен для учеников и преподаватель юношеского клуба GOLD.

Пользователи могут стать учениками, пройдя полностью регистрицаю и записавшись хотя бы на 1 секцию.

Здесь ученики могут оставить заявку на поступление в новую секцию, просмотреть свои занятия.

Преподаватели могут отправлять уведомления для своих учеников, просматривать свое расписание.

Если бот перестал отвечать, попробуйте ввести команду /start.
Лицо, ответственное за разработку и работу бота: @Golden_Good_Boy
    """
    await message.answer(text)


# ______________________ [/start] ______________________ #
@dp.message_handler(state='*', commands=['start', 'cancel'])
async def bot_start(message: types.Message, state: FSMContext):
    await state.finish()
    await state.reset_data()
    text = """
Бот юношеского клуба "GOLD"

Введите команду /info для подробной информации о боте
        """

    if db.is_user_login(message.from_user.id):
        role = str(db.get_role(message.from_user.id))
        rm = keyboards.login_menu[role]
        st = 'auth-' + role

    else:
        rm = keyboards.unlogin_kb
        st = 'unauth'
        text += "\nДля использования бота, необходимо зарегистрироваться/залогиниться"


    await state.set_state(st)
    await message.answer(text, reply_markup=rm)


# ______________________ UNAUTH ______________________ #
@dp.message_handler(state='unauth')
async def main_menu(message: types.Message, state: FSMContext):
    if message.text == '✍ Регистрация':
        await RegistrationForm.Email.set()
        text = """
Добро пожаловать в регистрацию!

Введите свою почту (вам придет код-подтверждение)
        """
        await message.answer(text, reply_markup=keyboards.rm_kb)

    elif message.text == '🗝 Вход':
        await LoginForm.Email.set()
        text = """
*Авторизация*

Для доступа к боту необходима авторизация

Введите Email и пароль в двух сообщениях
        """
        await message.answer(text, reply_markup=keyboards.rm_kb)

    elif message.text == '📃 Просмотр графика занятий':
        lessons = db.get_all_lessons()
        text = print_lessons(lessons)
        await message.answer(text)


# ______________________LOGIN______________________#
@dp.message_handler(state=LoginForm.Email)
async def login1(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Email'] = message.text
    await LoginForm.next()


@dp.message_handler(state=LoginForm.Password)
async def login2(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        psd = encrypt_password(message.text)
        email = data['Email']
    isCorrect, user = db.login(email, psd, message.from_user.id)
    if isCorrect:
        await state.finish()
        await state.reset_data()

        if user[-2]:
            st = dp.current_state(chat=user[-2])
            await bot.send_message(user[-2], '[Внимание!]\n\nБыл произведен вход с другого устройства', reply_markup=keyboards.rm_kb)
            await st.set_state('unauth')

        role = str(db.get_role(message.from_user.id))
        rm = keyboards.login_menu[role]

        await state.set_state('auth-'+role)
        await message.answer('Вы успешно вошли в систему!', reply_markup=rm)
        await message.delete()
    else:
        await message.answer('Ошибка авторизации! Неверный email или пароль\n\nВведите email')
        await LoginForm.previous()


# ______________________REGISTRATION______________________ #
@dp.message_handler(state=RegistrationForm.Email)
async def reg_1(message: types.Message, state: FSMContext):
    code = generate_code(length=4)
    mail.send_email(TO=message.text, msg=mail.generate_reg_mail(message.text, code))
    async with state.proxy() as data:
        data['EmailCode'] = str(code)
        data['Email'] = message.text
    await RegistrationForm.next()
    await message.answer('Введите код подтверждения')


@dp.message_handler(state=RegistrationForm.ActivateEmail, commands='again')
async def reg_2(message: types.Message, state: FSMContext):
    code = generate_code(length=4)
    async with state.proxy() as data:
        user_email = data['Email']
    mail.send_email(TO=user_email, msg=mail.generate_reg_mail(user_email, code))
    await state.update_data(EmailCode=(code))
    await message.answer('Новое письмо отправлено!\n\nВведите код подтверждения')


@dp.message_handler(state=RegistrationForm.ActivateEmail)
async def reg_3(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        code = data['EmailCode']
    if code == message.text:
        await state.update_data(ActivateEmail=True)
        await RegistrationForm.next()
        await message.answer('Почта подтверждена!\n\nПридумайте пароль')

    else:
        await message.answer('Неверный код подтверждения! Повторите попытку или введите /again, чтобы отправить письмо еще раз')


@dp.message_handler(state=RegistrationForm.Password)
async def reg_4(message: types.Message, state: FSMContext):
    if is_correct_password(message.text):
        async with state.proxy() as data:
            data['Password'] = message.text

        await message.answer('*Пароль был принят* \n\nПожалуйста, повторите пароль еще раз')
        await RegistrationForm.next()
    else:
        await message.answer('В пароле допустимы только буквы латиницы и цифры.\nМинимальная длина пароля: 6 символов\n\nПовторите попытку еще раз')
    await message.delete()


@dp.message_handler(state=RegistrationForm.Password2)
async def reg_5(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        psd = data['Password']
        email = data['Email']
    if message.text == psd:
        await message.answer('Регистрация прошла успешно!', reply_markup=keyboards.login_menu_kb_unstudent)
        await message.delete()
        await state.finish()
        await state.reset_data()
        await state.set_state('auth-0')

        psd = encrypt_password(psd)
        db.create_new_user(email, psd, message.from_user.id)


    else:
        await RegistrationForm.previous()
        await message.answer('Пароли не совпадают, попробуйте еще\n\nВведите пароль')
        await message.delete()


# ______________________ AUTH ______________________ #
@dp.message_handler(state='auth-0')
async def auth_0(message: types.Message, state: FSMContext):

    if message.text == '⏰ Мои занятия':
        lessons = list(db.get_my_lessons(message.from_user.id))
        text = print_lessons(lessons)
        await message.answer(text)

    elif message.text == '🧑‍💻 Профиль':
        user_data = db.get_me(message.from_user.id)
        text = print_profile(user_data)
        await message.answer(text)

    elif message.text == '⚙ Настройки':
        await state.set_state('settings')
        await message.answer(message.text, reply_markup=keyboards.settings_kb)

    elif message.text == '🖋 Записаться в секцию':
        user = db.get_me(message.from_user.id)
        if None not in user:
            await SignUp_Section.ChooseSection.set()
            sections = db.get_sections_not_users(message.from_user.id)
            subjects = [i[1] for i in sections]
            rm = keyboards.make_sections_kb(subjects)
            async with state.proxy() as data:
                data['sections'] = sections
            await message.answer('Выберите секцию, на которую хотите записаться', reply_markup=rm)
        else:
            await message.answer('Для начала полностью заполните профиль!')

    elif message.text == '📃 Просмотр графика занятий':
        lessons = db.get_all_lessons()
        text = print_lessons(lessons)
        await message.answer(text)

    elif message.text == '📬 Задать вопрос / сообщить об ошибке':
        await ReportState.MakeMessage.set()
        await message.answer('Напишите ваше сообщение\n\n[Введите /cancel для отмены]', reply_markup=keyboards.rm_kb)

    elif message.text == '📖 Просмотреть ответы':
        my_reports = db.show_answers_by_user_id(db.get_user_by_telegram(message.from_user.id))
        await message.answer(print_my_answers(my_reports))

@dp.message_handler(state='auth-1')
async def auth_1(message: types.Message, state: FSMContext):

    if message.text == '⏰ Мои занятия':
        lessons = list(db.get_my_lessons(message.from_user.id))
        text = print_lessons(lessons)
        await message.answer(text)

    elif message.text == '🧑‍💻 Профиль':
        user_data = db.get_me(message.from_user.id)
        text = print_profile(user_data)
        await message.answer(text)

    elif message.text == '⚙ Настройки':
        await state.set_state('settings')
        await message.answer(message.text, reply_markup=keyboards.settings_kb)

    elif message.text == '🖋 Записаться в секцию':
        user = db.get_me(message.from_user.id)
        if None not in user:
            await SignUp_Section.ChooseSection.set()
            sections = db.get_sections_not_users(message.from_user.id)
            subjects = [i[1] for i in sections]
            rm = keyboards.make_sections_kb(subjects)
            async with state.proxy() as data:
                data['sections'] = sections
            await message.answer('Выберите секцию, на которую хотите записаться', reply_markup=rm)
        else:
            await message.answer('Для начала полностью заполните профиль!')


    elif message.text == '📃 Просмотр графика занятий':
        lessons = db.get_all_lessons()
        text = print_lessons(lessons)
        await message.answer(text)

    elif message.text == '📬 Задать вопрос / сообщить об ошибке':
        await ReportState.MakeMessage.set()
        await message.answer('Напишите ваше сообщение\n\n[Введите /cancel для отмены]', reply_markup=keyboards.rm_kb)

    elif message.text == '📖 Просмотреть ответы':
        my_reports = db.show_answers_by_user_id(db.get_user_by_telegram(message.from_user.id))
        await message.answer(print_my_answers(my_reports))


@dp.message_handler(state='auth-2')
async def auth_2(message: types.Message, state: FSMContext):

    if message.text == '⏰ Мои предметы':
        lessons = list(db.get_my_lessons_tutor(message.from_user.id))
        text = print_lessons(lessons)
        await message.answer(text)

    elif message.text == '📢 Создать объявление':
        lessons = db.get_my_lessons_tutor(message.from_user.id)
        lessons = (i[0] for i in lessons)
        rm = keyboards.make_alert_kb(lessons)
        await message.answer('Выберите, участникам какой секции хотите отправить сообщение', reply_markup=rm)
        await MakeAlert.ChooseSection.set()

    elif message.text == '🧑‍💻 Профиль':
        user_data = db.get_me(message.from_user.id)
        text = print_profile(user_data)
        await message.answer(text)

    elif message.text == '⚙ Настройки':
        await state.set_state('settings')
        await message.answer(message.text, reply_markup=keyboards.settings_kb)

    elif message.text == '📃 Просмотр графика занятий':
        lessons = db.get_all_lessons()
        text = print_lessons(lessons)
        await message.answer(text)

    elif message.text == '📬 Задать вопрос / сообщить об ошибке':
        await ReportState.MakeMessage.set()
        await message.answer('Напишите ваше сообщение\n\n[Введите /cancel для отмены]', reply_markup=keyboards.rm_kb)

    elif message.text == '📖 Просмотреть ответы':
        my_reports = db.show_answers_by_user_id(db.get_user_by_telegram(message.from_user.id))
        await message.answer(print_my_answers(my_reports))


@dp.message_handler(state='auth-3')
async def auth_3(message: types.Message, state: FSMContext):

    if message.text == '👨🏻‍🏫 Преподаватели':
        await state.set_state('work_with_tutors')
        await message.answer(message.text, reply_markup=keyboards.work_with_tutors)

    elif message.text == '👨🏻‍🎓 Ученики':
        pass

    elif message.text == '🔬 Репорты':
        reports = db.check_reports()
        async with state.proxy() as data:
            data['reports'] = reports
        text = print_report_by_id(reports[0]) + f'\nСтраница: {1}'
        await message.answer(text, reply_markup=keyboards.generate_inline_kb(0))

    elif message.text == '🧑‍💻 Профиль':
        user_data = db.get_me(message.from_user.id)
        text = print_profile(user_data)
        await message.answer(text)

    elif message.text == '⚙ Настройки':
        await state.set_state('settings')
        await message.answer(message.text, reply_markup=keyboards.settings_kb)

    elif message.text == '📢 Создать объявление':
        lessons = db.get_all_lessons()
        lessons = (i[0] for i in lessons)
        rm = keyboards.make_alert_kb(lessons)
        await message.answer('Выберите, участникам какой секции хотите отправить сообщение', reply_markup=rm)
        await MakeAlert.ChooseSection.set()

    elif message.text == '📬 Задать вопрос / сообщить об ошибке':
        await ReportState.MakeMessage.set()
        await message.answer('Напишите ваше сообщение\n\n[Введите /cancel для отмены]', reply_markup=keyboards.rm_kb)

    elif message.text == '📖 Просмотреть ответы':
        my_reports = db.show_answers_by_user_id(db.get_user_by_telegram(message.from_user.id))
        await message.answer(print_my_answers(my_reports))


# ______________________ WORK WITH TUTORS ____________________ #
@dp.message_handler(state='work_with_tutors')
async def work_with_tutors_1(message: types.Message, state: FSMContext):
    if message.text == 'Назначить':
        await AddDeleteTutor.Email.set()
        await message.answer('🔴 Введите Email пользователя, которого хотите сделать преподавателем', reply_markup=keyboards.rm_kb)

        async with state.proxy() as data:
            data['action'] = 'Назначить'

    elif message.text == 'Убрать':
        await AddDeleteTutor.Email.set()
        await message.answer('🔴 Введите Email пользователя, у которого хотите отобрать права преподавателя', reply_markup=keyboards.rm_kb)

        async with state.proxy() as data:
            data['action'] = 'Убрать'

    elif message.text == '🧾 Показать всех преподавателей':
        tutors = db.show_all_tutors()
        print(tutors)
        text = print_tutors(tutors)
        await message.answer(text)


    elif message.text == 'Добавить на секцию':
        sections = tuple((i[0] for i in db.get_all_lessons()))
        kb = keyboards.make_sections_kb(sections)
        await message.answer('Выберите секцию, на которую хотите добавить преподавателя', reply_markup=kb)
        async with state.proxy() as data:
            data['sections'] = sections
        await AddTutorToSection.Section.set()

    elif message.text == '🔙 Назад':
        await message.answer(message.text, reply_markup=keyboards.login_menu['3'])
        await state.reset_data()
        await state.set_state('auth-3')


@dp.message_handler(state=AddTutorToSection.Section)
async def add_tutor_to_section_1(message: types.Message, state: FSMContext):
    section = message.text
    tutors = db.get_tutors_with_emails()
    async with state.proxy() as data:
        sections = data['sections']
        data['section'] = section
        data['tutors'] = tutors

    if section in sections:
        await AddTutorToSection.next()
        await message.answer('Напишите Email преподавателя, который будет вести секцию.\n\nВажно! Если у секции уже есть преподаватель, он будет заменен', reply_markup=keyboards.make_tutors_with_email(tutors))
    else:
        await message.answer('Ошибка в выборе секции. Выберите секцию из списка!')


@dp.message_handler(state=AddTutorToSection.Tutor)
async def add_tutor_to_section_2(message: types.Message, state: FSMContext):
    tutor = message.text
    async with state.proxy() as data:
        section = data['section']
        tutors = data['tutors']
        data['tutor'] = tutor

    if tutor in (i[0] + ' ' + i[1] + ' (' + i[2] + ')' for i in tutors):
        await AddTutorToSection.next()
        email = tutor.split(' ')[2].lstrip('(').rstrip(')')
        user = db.get_user_by_email(email)
        print(email)
        print(user)
        async with state.proxy() as data:
            data['user'] = user
        text = f"""
[Подтвердите действие]

[Пользователь]

- ID: {user[0]}
- {user[1]} {user[2]}
- {user[3]}
- {user[4]}

[Действие]: 
Сделать преподавателем для секции "{section}"
            """
        await message.answer(text, reply_markup=keyboards.edit_accept_cancel_kb)
    else:
        await message.answer('Ошибка в выборе преподавателя. Выберите преподавателя из списка!')


@dp.message_handler(state=AddTutorToSection.Accept)
async def add_tutor_to_section_3(message: types.Message, state: FSMContext):
    if message.text == '✅ Подтвердить':
        async with state.proxy() as data:
            user = data['user']
            section = data['section']
        admin = db.get_me(message.from_user.id)[:2]
        db.add_tutor_to_section(user[0], section)
        user_tg = user[-1]

        if user_tg:
            text = f"""
[Внимание!]

Вы были добавлены на секцию {section} как преподаватель!

[Администратор]: {admin[0]} {admin[1]}

                    """
            await bot.send_message(user_tg, text=text)
        await state.finish()
        await state.reset_data()
        role = 3
        await state.set_state('auth-' + str(role))
        await message.answer(f'Пользователь был добавлен как преподаватель в секцию {section}!', reply_markup=keyboards.login_menu[str(role)])

    elif message.text == '✏ Изменить (вернуться назад)':
        await AddTutorToSection.previous()
        await message.answer('🔘 Выберите преподавателя еще раз')

    elif message.text == '❌ Отменить':
        await state.finish()
        await state.reset_data()
        role = 3
        await state.set_state('auth-' + str(role))
        await message.answer('Возвращаемся в главное меню', reply_markup=keyboards.login_menu[str(role)])


@dp.message_handler(state=AddDeleteTutor.Email)
async def AddDeleteTutor_1(message: types.Message, state: FSMContext):
    email = message.text
    user = db.get_user_by_email(email)
    async with state.proxy() as data:
        action = data['action']
        data['user'] = user

    try:
        user_role = user[-2]
        if action == 'Назначить' and user_role not in ['Новый пользователь', 'Ученик']:
            raise Exception
        if action == 'Убрать' and user_role in ['Новый пользователь', 'Ученик', 'Администратор']:
            raise Exception
    except Exception as e:
        await message.answer('Ошибка!\nПользователь не найден или действие не может быть совершенно.\nПовторите попытку или введите /cancel для отмены')
        return

    text = f"""
[Подтвердите действие]

[Пользователь]

- ID: {user[0]}
- {user[1]} {user[2]}
- {user[3]}
- {user[4]}

[Действие]: {action}
    """
    await message.answer(text, reply_markup=keyboards.edit_accept_cancel_kb)
    await AddDeleteTutor.next()



@dp.message_handler(state=AddDeleteTutor.Accept)
async def AddDeleteTutor_2(message: types.Message, state: FSMContext):
    if message.text == '✅ Подтвердить':
        async with state.proxy() as data:
            user = data['user']
            action = data['action']
        admin = db.get_me(message.from_user.id)[:2]

        if action == 'Назначить':
            db.change_user_role_by_email(user[3], 2)
        elif action == 'Убрать':
            db.change_user_role_by_email(user[3], 1)

        user_tg = user[-1]

        if user_tg:
            current_role = db.get_rolename_by_telegram_id(user[-1])
            text = f"""
[Внимание!]

Ваша роль была изменена!
Текущая роль: {current_role}

[Администратор]: {admin[0]} {admin[1]}

                """
            await bot.send_message(user_tg, text=text, reply_markup=keyboards.login_menu[current_role])
        await state.finish()
        await state.reset_data()
        role = db.get_role(message.from_user.id)
        await state.set_state('auth-' + str(role))
        await message.answer('Роль пользователя была изменена!', reply_markup=keyboards.login_menu[str(role)])

    elif message.text == '✏ Изменить (вернуться назад)':
        await AddDeleteTutor.previous()
        await message.answer('🔘 Введите Email еще раз')

    elif message.text == '❌ Отменить':
        await state.finish()
        await state.reset_data()
        role = db.get_role(message.from_user.id)
        await state.set_state('auth-' + str(role))
        await message.answer('Возвращаемся в главное меню', reply_markup=keyboards.login_menu[str(role)])

# ______________________ REPORT QUERY CALLBACK ____________________ #
@dp.callback_query_handler(Text(startswith="rep"), state='auth-3')
async def report_callback(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        reports = data['reports']
    text = ''
    report_index = int(call.data.split('_')[2])

    if call.data.startswith('rep_answer_'):
        await bot.send_message(call.from_user.id, 'Напишите ответ на сообщение', reply_markup=keyboards.rm_kb)
        await ReportAnswer.MakeMessage.set()
        async with state.proxy() as data:
            data['report_index'] = report_index

    if report_index > 0:
        if call.data.startswith('rep_back_'):
            try:
                text = print_report_by_id(reports[report_index-1])
                report_index -= 1
                text += f'\n\tСтраница: {report_index+1}'
            except IndexError:
                text = "\n[Конец списка!]\n"
                report_index = -1
    elif report_index == 0:
        if call.data.startswith('rep_back_'):
            text = "\n[Конец списка!]\n"
            report_index = -1

    if call.data.startswith('rep_next_'):
        try:
            text = print_report_by_id(reports[report_index+1])
            report_index += 1
            text += f'\nСтраница: {report_index+1}'
        except IndexError as e:
            print(e)
            text = "\n[Конец списка!]\n"
            report_index = len(reports)
    try:
        await call.message.edit_text(text, reply_markup=keyboards.generate_inline_kb(report_index))
    except Exception as e:
        if not call.data.startswith('rep_answer'):
            await call.answer(text='Список репортов окончен!')
    await call.answer()


# ______________________ REPORT ANSWER ____________________ #
@dp.message_handler(state=ReportAnswer.MakeMessage)
async def report_answer_1(message: types.Message, state: FSMContext):
    msg = message.text
    async with state.proxy() as data:
        data['message'] = msg
        report_index = data['report_index']
        reports = data['reports']
    text = f"""
[Подтвердите отправку сообщения]

[Репорт]: 
{print_report_by_id(reports[report_index])}

[Ответ]: 
{msg}
        """

    await message.answer(text, reply_markup=keyboards.edit_accept_cancel_kb)
    await ReportAnswer.next()

@dp.message_handler(state=ReportAnswer.Accept)
async def report_answer_2(message: types.Message, state: FSMContext):
    if message.text == '✅ Подтвердить':
        async with state.proxy() as data:
            reports = data['reports']
            report_index = data['report_index']
            msg = data['message']
        admin_id = db.get_user_by_telegram(message.from_user.id)
        db.make_answer_on_report(reports[report_index][0], admin_id, msg)

        user_tg = db.get_telegram_by_user_id(reports[report_index][1])[0]
        print('user_tg', user_tg)
        admin = db.get_me(message.from_user.id)[:2]
        if user_tg:
            txt = f"""
Поступил ответ на ваш вопрос!
[Ваше обращение]
{reports[report_index][-2]}

[Администратор]: {admin[0]} {admin[1]}

[Ответ]

{msg}
            """
            await bot.send_message(user_tg, txt)

        await state.finish()
        await state.reset_data()
        role = db.get_role(message.from_user.id)
        await state.set_state('auth-' + str(role))
        await message.answer('Сообщение было отправлено!', reply_markup=keyboards.login_menu[str(role)])

    elif message.text == '✏ Изменить (вернуться назад)':
        await ReportAnswer.previous()
        await message.answer('Введите сообщение еще раз', reply_markup=keyboards.rm_kb)

    elif message.text == '❌ Отменить':
        await state.finish()
        await state.reset_data()
        role = db.get_role(message.from_user.id)
        await state.set_state('auth-' + str(role))
        await message.answer('Возвращаемся в главное меню', reply_markup=keyboards.login_menu[str(role)])

# ______________________ CHOOSE_SECTION ______________________ #
@dp.message_handler(state=SignUp_Section.ChooseSection)
async def signup_section_1(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        sections = data['sections']
    print(sections)
    temp = {i[1]: i[0] for i in sections}
    if message.text in temp.keys():
        db.make_new_contract(db.get_user_by_telegram(message.from_user.id), temp[message.text])
        await state.finish()
        await state.reset_data()
        role = str(db.get_role(message.from_user.id))
        if role == '0':
            db.change_user_role_by_telegram(message.from_user.id, 1)
            role = '1'
        await state.set_state('auth-'+role)
        await message.answer(f'Вы успешно записались на секцию "{message.text}"!\nВам могут написать на почту для уточнения деталей.', reply_markup=keyboards.login_menu[role])

    else:
        await message.answer('Ошибка, повторите попытку еще раз')


# ______________________ MAKE_ALERT ______________________ #
@dp.message_handler(state=MakeAlert.ChooseSection)
async def make_alert_1(message: types.Message, state: FSMContext):
    group = message.text
    telegrams = ''
    tgs = db.get_telegrams_for_alert(group)

    async with state.proxy() as data:
        data['group'] = group
        data['telegrams'] = tgs
    await message.answer('Введите сообщение', reply_markup=keyboards.rm_kb)
    await MakeAlert.next()


@dp.message_handler(state=MakeAlert.MakeMessage)
async def make_alert_2(message: types.Message, state: FSMContext):
    msg = message.text
    async with state.proxy() as data:
        data['message'] = msg
        group = data['group']

    text = f"""
[Подтвердите отправку сообщения]

[Группа]: {group}

[Сообщение]: {msg}
    """

    await message.answer(text, reply_markup=keyboards.edit_accept_cancel_kb)
    await MakeAlert.next()


@dp.message_handler(state=MakeAlert.Accept)
async def make_alert_3(message: types.Message, state: FSMContext):
    if message.text == '✅ Подтвердить':
        async with state.proxy() as data:
            telegrams = data['telegrams']
            msg = data['message']

        tutor = db.get_me(message.from_user.id)
        if tutor[-1] == 'Преподаватель':

            text = f"""
    [Сообщение от преподавателя]
    Преподаватель: {' '.join(tutor[:2])}
    
    Сообщение:
    {msg}
            """
        else:
            text = f"""
            [Сообщение от администратора]
            Администратор: {' '.join(tutor[:2])}

            Сообщение:
            {msg}
                    """
        for i in telegrams:
            print(i[0])
            if i[0]:
                await bot.send_message(i[0], text)
        await state.finish()
        await state.reset_data()
        role = db.get_role(message.from_user.id)
        await state.set_state('auth-'+str(role))
        await message.answer('Сообщение было отправлено!', reply_markup=keyboards.login_menu[str(role)])
    elif message.text == '✏ Изменить (вернуться назад)':
        await MakeAlert.previous()
        await message.answer('Введите сообщение еще раз')
    elif message.text == '❌ Отменить':
        await state.finish()
        await state.reset_data()
        role = db.get_role(message.from_user.id)
        await state.set_state('auth-'+ str(role))
        await message.answer('Возвращаемся в главное меню', reply_markup=keyboards.login_menu[str(role)])


# ______________________ MAKE REPORT ______________________ #
@dp.message_handler(state=ReportState.MakeMessage)
async def report_state_1(message: types.Message, state: FSMContext):
    report = message.text
    async with state.proxy() as data:
        data['report'] = report
    text = f"""
[Подтвердите отправку сообщения]

[Сообщение]: 
{report}
        """
    await ReportState.next()
    await message.answer(text, reply_markup=keyboards.edit_accept_cancel_kb)


@dp.message_handler(state=ReportState.Accept)
async def report_state_2(message: types.Message, state: FSMContext):
    if message.text == '✅ Подтвердить':
        async with state.proxy() as data:
            report = data['report']
        user_id = db.get_user_by_telegram(message.from_user.id)
        await state.finish()
        await state.reset_data()

        db.make_new_report(user_id, report)

        role = db.get_role(message.from_user.id)
        await state.set_state('auth-'+str(role))
        await message.answer('Сообщение было отправлено!', reply_markup=keyboards.login_menu[str(role)])

    elif message.text == '✏ Изменить (вернуться назад)':
        await ReportState.previous()
        await message.answer('Введите новое сообщение')

    elif message.text == '❌ Отменить':
        await state.finish()
        await state.reset_data()
        role = db.get_role(message.from_user.id)
        await state.set_state('auth-'+str(role))
        await message.answer('Возвращаемся в главное меню', reply_markup=keyboards.login_menu[str(role)])

# ______________________ SETTINGS ______________________ #
@dp.message_handler(state='settings')
async def settings(message: types.Message, state: FSMContext):
    if message.text == 'Изменить имя':
        await message.answer('Введите новое имя', reply_markup=keyboards.rm_kb)
        await state.set_state('change_firstname')

    elif message.text == 'Изменить фамилию':
        await message.answer('Введите новую фамилию', reply_markup=keyboards.rm_kb)
        await state.set_state('change_lastname')

    elif message.text == 'Изменить дату рождения':
        await message.answer('Введите новую дату в формате дд.мм.гггг', reply_markup=keyboards.rm_kb)
        await state.set_state('change_birthday')

    elif message.text == 'Изменить почту':
        await ChangeEmail.CheckPassword.set()
        await message.answer('Введите старый пароль', reply_markup=keyboards.rm_kb)

    elif message.text == 'Изменить пароль':
        await ChangePassword.OldPassword.set()
        await message.answer('Введите старый пароль', reply_markup=keyboards.rm_kb)

    elif message.text == 'Выйти из аккаунта':
        db.logout(message.from_user.id)
        await state.set_state('unauth')
        await message.answer('Вы успешно вышли из аккаунта!', reply_markup=keyboards.unlogin_kb)

    elif message.text == '🔙 Назад':
        role = str(db.get_role(message.from_user.id))
        await state.set_state('auth-'+role)
        await message.answer(message.text, reply_markup=keyboards.login_menu[role])


# ______________________ CHANGE_FIRST_NAME ______________________ #
@dp.message_handler(state='change_firstname')
async def change_firstname(message: types.Message, state: FSMContext):
    if message.text.isalpha():
        db.change_user_firstname(message.text, message.from_user.id)
        await message.answer('Имя было успешно изменено!', reply_markup=keyboards.settings_kb)
        await state.set_state('settings')
    else:
        await message.answer('Неккоректное имя. Используйте только буквы алфавита')


# ______________________ CHANGE_LAST_NAME ______________________ #
@dp.message_handler(state='change_lastname')
async def change_lastname(message: types.Message, state: FSMContext):
    if message.text.isalpha():
        db.change_user_lastname(message.text, message.from_user.id)
        await message.answer('Фамилия была успешна изменена!', reply_markup=keyboards.settings_kb)
        await state.set_state('settings')
    else:
        await message.answer('Неккоректное фамилия. Используйте только буквы алфавита')


# ______________________ CHANGE_BIRTHDAY ______________________ #
@dp.message_handler(state='change_birthday')
async def change_birthday(message: types.Message, state: FSMContext):
    s = [int(i) for i in reversed(message.text.split('.'))]
    try:
        d = date(*s)
        db.change_user_birthday(d, message.from_user.id)
        await message.answer('Дата рождения была успешно изменена!', reply_markup=keyboards.settings_kb)
        await state.set_state('settings')

    except:
        await message.answer('Ошибка. Вероятно, введена дата в неправильном формате.\n\nПример корректной даты: 01.06.2022')


# ______________________ CHANGE_EMAIL ______________________ #
@dp.message_handler(state=ChangeEmail.CheckPassword)
async def change_email(message: types.Message, state: FSMContext):
    password = db.get_password(message.from_user.id)
    if encrypt_password(message.text) == password:
        async with state.proxy() as data:
            data['Email'] = message.text
        await ChangeEmail.next()

        await message.answer('Успешно!\nВведите новую почту (на нее придет код-подтверждение)')
    else:
        await message.answer('Неверный пароль! Попробуйте еще раз')
    await message.delete()


@dp.message_handler(state=ChangeEmail.NewEmail)
async def change_email(message: types.Message, state: FSMContext):
    code = generate_code(6)
    async with state.proxy() as data:
        data['Email'] = message.text
        data['EmailCode'] = code
    mail.send_email(TO=message.text, msg=mail.generate_reg_mail(message.text, code))
    await message.answer('Введите код из сообщения')
    await ChangeEmail.next()


@dp.message_handler(state=ChangeEmail.CheckCode, commands='again')
async def change_email_again(message: types.Message, state: FSMContext):
    code = generate_code(length=4)
    async with state.proxy() as data:
        user_email = data['Email']
        data['EmailCode'] = code
    mail.send_email(TO=user_email, msg=mail.generate_reg_mail(user_email, code))
    await message.answer('Новое письмо отправлено!\n\nВведите код подтверждения')


@dp.message_handler(state=ChangeEmail.CheckCode)
async def change_email(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        code = data['EmailCode']
        email = data['Email']
    if code == message.text:
        db.change_user_email(email, message.from_user.id)
        await message.answer('Почта была успешно изменена!', reply_markup=keyboards.settings_kb)
        await state.finish()
        await state.reset_data()
        await state.set_state('settings')
    else:
        await message.answer('Неверный код подтверждения! Повторите попытку или введите /again, чтобы отправить письмо еще раз')


# ______________________ CHANGE_PASSWORD ______________________ #
@dp.message_handler(state=ChangePassword.OldPassword)
async def change_password(message: types.Message, state: FSMContext):
    oldpassword = db.get_password(message.from_user.id)
    if oldpassword == encrypt_password(message.text):

        await ChangePassword.next()
        await message.answer('Придумайте новый пароль')
    else:
        await message.answer('Неверный пароль, повторите попытку еще раз')
    await message.delete()


@dp.message_handler(state=ChangePassword.NewPassword)
async def change_password2(message: types.Message, state: FSMContext):

    if is_correct_password(message.text):
        async with state.proxy() as data:
            data['NewPassword'] = message.text

        await message.answer('Повторите пароль еще раз')
        await ChangePassword.next()
    else:
        await message.answer('В пароле допустимы только буквы латиницы и цифры.\nМинимальная длина пароля: 6 символов\n\nПовторите попытку еще раз')

    await message.delete()


@dp.message_handler(state=ChangePassword.NewPassword2)
async def change_password3(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        prev_password = data['NewPassword']
    if prev_password == message.text:
        db.change_user_password(encrypt_password(message.text), message.from_user.id)
        await message.answer('Пароль успешно изменен!', reply_markup=keyboards.settings_kb)
        await state.finish()
        await state.reset_data()
        await state.set_state('settings')
    else:
        await message.answer('Пароли не совпадают.\n\nВведите новый пароль еще раз')
        await ChangePassword.previous()
    await message.delete()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)