from aiogram.dispatcher.filters.state import State, StatesGroup


class RegistrationForm(StatesGroup):
    Email = State()
    ActivateEmail = State()
    Password = State()
    Password2 = State()
    EmailCode = State()


class LoginForm(StatesGroup):
    Email = State()
    Password = State()


class ChangeEmail(StatesGroup):
    CheckPassword = State()
    NewEmail = State()
    CheckCode = State()


class ChangePassword(StatesGroup):
    OldPassword = State()
    NewPassword = State()
    NewPassword2 = State()


class MakeAlert(StatesGroup):
    ChooseSection = State()
    MakeMessage = State()
    Accept = State()


class SignUp_Section(StatesGroup):
    ChooseSection = State()


class ReportState(StatesGroup):
    MakeMessage = State()
    Accept = State()


class ReportAnswer(StatesGroup):
    MakeMessage = State()
    Accept = State()


class AddDeleteTutor(StatesGroup):
    Email = State()
    Accept = State()

class AddTutorToSection(StatesGroup):
    Section = State()
    Tutor = State()
    Accept = State()

