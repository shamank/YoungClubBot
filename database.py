import pymysql
from config import DB_HOST, DB_PORT, DB_USER, DB_NAME, DB_USER_PASSWORD
from datetime import datetime

class dbase:
    def __init__(self):
        conn = self.mysql_connect()

    def mysql_connect(self):
        db = None
        try:
            db = pymysql.connect(
                host=DB_HOST,
                port=DB_PORT,
                user=DB_USER,
                password=DB_USER_PASSWORD,
                database=DB_NAME)
            print(f'Подключение к БД "{DB_NAME}" успешно установлено! \nВремя:{datetime.now()}\n')
        except Exception as e:
            print('Ошибка при подключении к базе данных!\nВремя:{}\n {}'.format(datetime.now(), e))
        return db

    def start_db(self):
        db = self.mysql_connect()
        try:
            sql = """            
                
                CREATE TABLE IF NOT EXISTS Role (
                  RoleID INT(10) UNIQUE,
                  Name VARCHAR(25) NOT NULL,
                  Description TEXT,
                  
                  PRIMARY KEY (RoleID)
                );
                
                INSERT INTO role 
                VALUES (0, 'Новый пользователь', 'Базовая роль, предоставляется при регистрации'),
                        (1, 'Ученик', 'Роль присваевается, если человек ходит хотя бы на одно занятие'),
                        (2, 'Преподаватель', 'Роль присваеватся вручную администратором'),
                        (3, 'Администратор', 'Роль присваевается вручную, полный доступ');
                
                CREATE TABLE IF NOT EXISTS User (
                  UserID INT(10) UNIQUE AUTO_INCREMENT,
                  FirstName VARCHAR(50),
                  LastName VARCHAR(50),
                  Birthday DATE,
                  Email VARCHAR(150) UNIQUE NOT NULL,
                  Password VARCHAR(150) NOT NULL,
                  LastTelegram INT(20),
                  Role INT(10) NOT NULL DEFAULT 0,
                  
                  PRIMARY KEY (UserID),
                  FOREIGN KEY (Role) REFERENCES Role (RoleID) ON DELETE SET DEFAULT,
                  
                  CONSTRAINT CHK_PASSWORD CHECK (Password REGEXP '[a-zA-Z0-9]' and LENGTH(Password) > 7),
                  CONSTRAINT CHK_EMAIL CHECK (Email REGEXP '[a-zA-Z]+([a-zA-Z0-9]+|[_.-]?)*[@][a-z]+[.][a-z]+')
                );
                
                INSERT INTO User
                VALUES (1, 'Руслан', 'Эшмуратов', '2001-11-20', 'golden_boy@gmail.com', 'b1c828636d696d16711d28e2765c9757ffbbe948436524ff6b43f4f78d2a770e', Null, 0),
                        (2, 'Степан', 'Филиппов', '2001-11-20', 'gggg@gmail.com', 'b1c828636d696d16711d28e2765c9757ffbbe948436524ff6b43f4f78d2a770e', Null, 0),
                        (3, 'Максим', 'Павлов', '2001-11-20', 'gzzvzxg@gmail.com', 'b1c828636d696d16711d28e2765c9757ffbbe948436524ff6b43f4f78d2a770e', Null, 1),
                        (4, 'Виктория', 'Прокофьева', '2001-11-20', 'gzzv231zxg@gmail.com', 'b1c828636d696d16711d28e2765c9757ffbbe948436524ff6b43f4f78d2a770e', Null, 1),
                        (5, 'Илья', 'Золотов', '2001-11-20', 'gzzv1szxg@ggg.com', 'b1c828636d696d16711d28e2765c9757ffbbe948436524ff6b43f4f78d2a770e', Null, 1),
                        (6, 'Полина', 'Михайлова', '2001-11-20', 'gzzv1sdzdzxg@gmail.com', 'b1c828636d696d16711d28e2765c9757ffbbe948436524ff6b43f4f78d2a770e', Null, 1),
                        (7, 'Никита', 'Волков', '2001-11-20', 'dasd@gmail.com', 'b1c828636d696d16711d28e2765c9757ffbbe948436524ff6b43f4f78d2a770e', Null, 2),
                        (8, 'Юрий', 'Кузнецов', '2001-11-20', 'vdf@gmail.com', 'b1c828636d696d16711d28e2765c9757ffbbe948436524ff6b43f4f78d2a770e', Null, 2),
                        (9, 'Екатерина', 'Петрова', '2001-11-20', 'asdew@gmail.com', 'b1c828636d696d16711d28e2765c9757ffbbe948436524ff6b43f4f78d2a770e', Null, 2),
                        (10, 'Иван', 'Волков', '2001-11-20', 'rwd21d@gmail.com', 'b1c828636d696d16711d28e2765c9757ffbbe948436524ff6b43f4f78d2a770e', Null, 3),
                        (11, 'Маргарита', 'Ежова', '2001-11-20', 'asdwe1@gmail.com', 'b1c828636d696d16711d28e2765c9757ffbbe948436524ff6b43f4f78d2a770e', Null, 3);
                
                
                CREATE TABLE IF NOT EXISTS Report (
                  ReportID INT(10) UNIQUE AUTO_INCREMENT,
                  From_User INT(10) NOT NULL,
                  Message TEXT NOT NULL,
                  is_active BOOL NOT NULL DEFAULT TRUE,
                  creating_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                  
                  PRIMARY KEY (ReportID),
                  FOREIGN KEY (From_User) REFERENCES User (UserID) ON DELETE CASCADE
                );
                
                CREATE TABLE IF NOT EXISTS Answer (
                  AnswerID INT(10) UNIQUE AUTO_INCREMENT,
                  Report INT(10) NOT NULL,
                  Admin INT(10),
                  Message TEXT,
                  answer_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                  
                  PRIMARY KEY (AnswerID),
                  FOREIGN KEY (Report) REFERENCES Report (ReportID) ON DELETE CASCADE,
                  FOREIGN KEY (Admin) REFERENCES User (UserID) ON DELETE SET NULL
                );
                
                INSERT INTO Report (ReportID, From_User, Message, is_active)
                VALUES (1, 1, 'Как записаться на секцию?', False),
                        (2, 5, 'У меня не работает бот', True),
                        (3, 7, 'Подскажите, могу ли я писать ученикам?', False),
                        (4, 3, 'Пишу по приколу', True);
                        
                INSERT INTO Answer (AnswerID, Report, Admin, Message)
                VALUES (1, 1, 10, 'Нажмите в главном меню кнопку Записаться на секцию'),
                        (2, 3, 10, 'Да, можете. Испольуйте кнопку Создать объявление');
                
                        
                CREATE TABLE IF NOT EXISTS Section (
                  SectionID INT(10) UNIQUE AUTO_INCREMENT,
                  Name VARCHAR(25) UNIQUE NOT NULL,
                  Tutor INT(10),
                  Timetable TEXT NOT NULL,
                
                  PRIMARY KEY (SectionID),
                  FOREIGN KEY (Tutor) REFERENCES User (UserID) ON DELETE SET NULL
                );
                
                INSERT INTO Section
                VALUES (1, 'Футбол', 7, 'ПН 14:50-16:30&ВТ -&СР -&ЧТ 15:00-16:30&ПТ 19:30-21:00'),
                        (2, 'Шахматы', 8, 'ПН 16:50-18:00&ВТ 16:50-18:00&СР -&ЧТ -&ПТ -'),
                        (3, 'Баскетбол', 7, 'ПН -&ВТ 14:50-16:30&СР 19:30-21:00&ЧТ -&ПТ -'),
                        (4, 'Волейбол', 7, 'ПН 16:50-18:00&ВТ 16:50-18:00&СР -&ЧТ -&ПТ 16:50-18:00'),
                        (5, 'Гитара', 9, 'ПН -&ВТ 14:00-15:30&СР 19:00-20:30&ЧТ 14:30-16:30&ПТ -'),
                        (6, 'Пианино', 9, 'ПН -&ВТ 16:50-18:00&СР -&ЧТ 17:00-19:30&ПТ 15:30-17:00');
                    
                
                CREATE TABLE IF NOT EXISTS Contract (
                  ContractID INT(10) UNIQUE AUTO_INCREMENT,
                  User INT(10) NOT NULL,
                  Section INT(10) NOT NULL,
                  Register_at DATE DEFAULT (CURRENT_DATE),
                  Until DATE DEFAULT (DATE_ADD(CURRENT_DATE, INTERVAL 90 DAY),
                  
                  PRIMARY KEY (ContractID),
                  FOREIGN KEY (User) REFERENCES User (UserID) ON DELETE CASCADE,
                  FOREIGN KEY (Section) REFERENCES Section (SectionID) ON DELETE CASCADE
                ); 
                
                INSERT INTO Contract
                VALUES (1, 3, 1, '2022-06-01', '2023-01-01'),
                        (2, 4, 4, '2022-06-15', '2023-01-01'),
                        (3, 3, 3, '2022-06-21', '2023-01-01'),
                        (4, 5, 2, '2022-06-22', '2023-01-01'),
                        (5, 6, 5, '2022-06-23', '2023-01-01'),
                        (6, 6, 6, '2022-07-01', '2023-01-01');
            
                
 

            """

            for i in sql.split(';')[:-1]:
                db.cursor().execute(i)
                print(i)
            db.commit()
        except Exception as e:
            print('Ошибка в создании таблиц!\n', e)
        db.close()

    def delete_tables(self):
        db = self.mysql_connect()

        sql = "show tables;"
        cur = db.cursor()
        cur.execute(sql)
        tbs = [i[0] for i in cur.fetchall()]
        db.cursor().execute('SET FOREIGN_KEY_CHECKS=0')
        for i in tbs:
            sql = f'DROP TABLE {i};'
            db.cursor().execute(sql)
        db.cursor().execute('SET FOREIGN_KEY_CHECKS=1')
        db.commit()
        db.close()

# __________ SIGNUP/LOGIN ________ #

    def create_new_user(self, email, password, telegram):
        db = self.mysql_connect()
        try:
            sql = "INSERT INTO `user` (`Email`, `Password`, `LastTelegram`) VALUES (%s, %s, %s);"

            cur = db.cursor()
            cur.execute(sql, (email, password, telegram))
            db.commit()
        except Exception as e:
            print('Ошибка при создании пользователя:\n', datetime.now(), e)
        db.close()

    def login(self, email, password, telegram_id):
        result = (False, 0)
        db = self.mysql_connect()
        try:
            sql = "SELECT * FROM `user` WHERE `Email` LIKE %s AND `Password` LIKE %s;"
            cur = db.cursor()
            cur.execute(sql, (email, password))
            user = cur.fetchone()
            if user:
                user_id = user[0]
                sql = "UPDATE user SET `LastTelegram` = %s WHERE `UserID` = %s"
                cur.execute(sql, (telegram_id, user_id))
                db.commit()
                result = (True, user)
        except Exception as e:
            print('Ошибка при авторизации пользователя:\n', datetime.now(), e)
        db.close()
        return result

    def is_user_login(self, telegram_id):
        result = False
        db = self.mysql_connect()
        try:
            sql = "SELECT * FROM `user` WHERE `LastTelegram` = %s;"
            cur = db.cursor()
            cur.execute(sql, (telegram_id,))
            user = cur.fetchone()
            if user:
                result = True
        except Exception as e:
            print('Ошибка нахождения пользователя по TelegramID', datetime.now(), e)
        db.close()
        return result

    def logout(self, telegram_id):
        db = self.mysql_connect()
        try:
            sql = """
            UPDATE `user`
            SET `LastTelegram` = Null
            WHERE `LastTelegram` = %s;
            """
            db.cursor().execute(sql, (telegram_id,))
            db.commit()
        except Exception as e:
            print('Ошибка в logout', e)

        db.close()

# ________ GET FUNCTIONS ________ #
    def get_tutors_with_emails(self):
        db = self.mysql_connect()
        res = 0
        try:
            sql = """
                SELECT `User`.`FirstName`, `User`.`LastName`, `User`.`Email`
                FROM `User`
                WHERE `User`.`Role` = 2;
                """
            cur = db.cursor()
            cur.execute(sql)
            res = cur.fetchall()
        except Exception as e:
            print('Ошибка в выдаче преподавателей с Email', datetime.now(), e)
        db.close()
        return res


    def get_all_lessons(self):
        db = self.mysql_connect()
        res = 0
        try:
            sql = """
            SELECT `Section`.`Name`, `Section`.`Timetable`, `User`.`FirstName`, `User`.`LastName`
            FROM `Section`
            INNER JOIN `User` ON `Section`.`Tutor` = `User`.`UserID`;
            """
            cur = db.cursor()
            cur.execute(sql)
            res = cur.fetchall()
        except Exception as e:
            print('Ошибка в выдаче расписания', datetime.now(), e)
        db.close()
        return res

    def get_my_lessons(self, telegram_id):
        db = self.mysql_connect()
        res = 0
        try:
            sql = """
            SELECT `Section`.`Name`, `Section`.`Timetable`
            FROM `Contract` 
            INNER JOIN `User` ON `Contract`.`User` = `User`.`UserID`
            INNER JOIN `Section` ON  `Contract`.`Section` = `Section`.`SectionID`
            WHERE `User`.`LastTelegram` = %s AND `Contract`.`Until` > CURRENT_DATE;
            """
            cur = db.cursor()
            cur.execute(sql, (telegram_id,))
            res = cur.fetchall()



        except Exception as e:
            print('Ошибка в показе пользователю своего расписания', datetime.now(), e)
        db.close()
        return res

    def get_my_lessons_tutor(self, telegram_id):
        db = self.mysql_connect()
        res = 0
        try:
            sql = """
            SELECT `Section`.`Name`, `Section`.`Timetable`
            FROM `Section`
            INNER JOIN `user` ON `Section`.`Tutor` = `User`.`UserID`
            WHERE `User`.`LastTelegram` = %s;
            """
            cur = db.cursor()
            cur.execute(sql, (telegram_id,))
            res = cur.fetchall()
        except Exception as e:
            print('Ошибка в показе преподавателю своего расписания', datetime.now(), e)
        db.close()
        return res

    def get_sections_not_users(self, telegram_id):
        db = self.mysql_connect()
        result = ''
        try:

            sql1 = """
                        SELECT `Section`.`SectionID`, `Section`.`Name`
                        FROM `Section`;
                        """
            sql2 = """
            SELECT `Section`.`SectionID`, `Section`.`Name` 
            FROM `Contract` 
            INNER JOIN `User` ON `Contract`.`User` = `User`.`UserID`
            INNER JOIN `Section` ON  `Contract`.`Section` = `Section`.`SectionID`
            WHERE `User`.`LastTelegram` = %s;
            
            """
            cur = db.cursor()
            cur.execute(sql1)
            result = cur.fetchall()
            print(result)
            cur.execute(sql2, (telegram_id,))
            result = set(result) - set(cur.fetchall())
            print(result)


        except Exception as e:
            print('Ошибка в просмотре секций пользователя', datetime.now(), e)
        db.close()
        return tuple(result)

    def get_user_by_telegram(self, telegram_id):
        db = self.mysql_connect()
        res = -1
        try:
            sql = """
            SELECT `User`.`UserID`
            FROM `user`
            WHERE `LastTelegram` = %s;
            """
            cur = db.cursor()
            cur.execute(sql, (telegram_id,))
            res = cur.fetchone()

        except Exception as e:
            print('Ошибка в получении пользователя по ID', datetime.now(), e)
        db.close()
        return res

    def get_telegram_by_user_id(self, user_id):
        db = self.mysql_connect()
        res = None
        try:
            sql = """
                   SELECT `User`.`LastTelegram`
                   FROM `user`
                   WHERE `UserID` = %s;
                   """
            cur = db.cursor()
            cur.execute(sql, (user_id,))
            res = cur.fetchone()

        except Exception as e:
            print('Ошибка в получении пользователя по Telegram', datetime.now(), e)
        db.close()
        return res

    def get_me(self, telegram_id):
        db = self.mysql_connect()
        res = 0
        try:
            sql = """
            SELECT `user`.`FirstName`, `user`.`LastName`, `user`.`Birthday`, `user`.`Email`, `role`.`Name`
            FROM `user` 
            INNER JOIN `role` ON `user`.`Role` = `role`.`RoleID`
            WHERE `user`.`LastTelegram` = %s;
            """
            cur = db.cursor()
            cur.execute(sql, (telegram_id,))
            res = cur.fetchone()
        except Exception as e:
            print('Ошибка в поиске по TelegramID', datetime.now(), e)
        db.close()
        return res

    def get_role(self, telegram_id):
        db = self.mysql_connect()
        res = -1
        try:
            sql = """
            SELECT `Role`
            FROM `user`
            WHERE `LastTelegram` = %s;
            """
            cur = db.cursor()
            cur.execute(sql, (telegram_id,))
            res = cur.fetchone()[0]

        except Exception as e:
            print('Ошибка в проверке роли!', datetime.now(), e)
        db.close()
        return res

    def get_rolename_by_telegram_id(self, telegram_id):
        db = self.mysql_connect()
        res = None
        try:
            sql = """
            SELECT `Role`.`Name`
            FROM `User`
            INNER JOIN `Role` ON `Role`.`RoleID` = `User`.`Role`
            WHERE `User`.`LastTelegram` = %s;
            """
            cur = db.cursor()
            cur.execute(sql, (telegram_id,))
            res = cur.fetchone()[0]
        except Exception as e:
            print('Ошибка в поиске роли!', datetime.now(), e)
        db.close()
        return res

    def get_telegrams_for_alert(self, section):
        db = self.mysql_connect()
        res = -1
        try:
            sql = """
            SELECT `User`.`LastTelegram`
            FROM `Contract`
            INNER JOIN `Section` on `Contract`.`Section` = `Section`.`SectionID`
            INNER JOIN `User` ON `Contract`.`User` = `User`.`UserID`
            WHERE `Section`.`Name` LIKE %s and `Contract`.`Until` > CURRENT_DATE and `User`.`LastTelegram` IS NOT NULL;
            """

            cur = db.cursor()
            cur.execute(sql, (section,))
            res = cur.fetchall()
        except Exception as e:
            print('Ошибка в просмотре пользователей по секции', datetime.now(), e)
        db.close()
        return res

    def get_user_by_email(self, email):
        db = self.mysql_connect()
        res = None
        try:
            sql = """
                   SELECT `User`.`UserID`, `User`.`FirstName`, `User`.`LastName`, `User`.`Email`, `Role`.`Name`, `User`.`LastTelegram`
                   FROM `User`
                   INNER JOIN `Role` ON `User`.`Role` = `Role`.`RoleID`
                   WHERE `User`.`Email` LIKE %s;
                   """
            cur = db.cursor()
            cur.execute(sql, (email,))
            res = cur.fetchone()
        except Exception as e:
            print('Ошибка в просмотре пароля', datetime.now(), e)
        db.close()
        return res

    def get_password(self, telegram_id):
        db = self.mysql_connect()
        res = -1
        try:
            sql = """
            SELECT `Password`
            FROM `user`
            WHERE `LastTelegram` = %s;
            """
            cur = db.cursor()
            cur.execute(sql, (telegram_id,))
            res = cur.fetchone()[0]
        except Exception as e:
            print('Ошибка в просмотре пароля', datetime.now(), e)
        db.close()
        return res


# __________ STUDENTS & TUTORS __________ #
    def show_all_tutors(self):
        db = self.mysql_connect()
        res = -1
        try:
            sql = """
            SELECT `Section`.`Name`, `User`.`UserID`, `User`.`FirstName`, `User`.`LastName`, `User`.`Email`
            FROM `User`
            LEFT JOIN `Section` ON `Section`.`Tutor` = `User`.`UserID`
            WHERE `User`.`Role` = 2
            ORDER BY `User`.`UserID`;
            """
            cur = db.cursor()
            cur.execute(sql)
            res = cur.fetchall()
        except Exception as e:
            print('Ошибка в просмотре преподавателей', datetime.now(), e)
        db.close()
        return res


    def add_tutor_to_section(self, tutor_id, section):
        db = self.mysql_connect()
        try:
            sql = """
            UPDATE `Section`
            SET `Tutor` = %s
            WHERE `Name` LIKE %s;
            """
            db.cursor().execute(sql, (tutor_id, section))
            db.commit()
        except Exception as e:
            print('Ошибка в добавлении преподавателя к секции', datetime.now(), e)
        db.close()




# __________ FOR SETTINGS __________ #

    def change_user_password(self, new_password, telegram_id):
        db = self.mysql_connect()
        try:
            sql = """
            UPDATE `user`
            SET `Password` = %s
            WHERE `LastTelegram` = %s;
            """
            cur = db.cursor()
            cur.execute(sql, (new_password, telegram_id))
            db.commit()
        except Exception as e:
            print('Ошибка в изменении пароля', datetime.now(), e)
        db.close()

    def change_user_email(self, new_email, telegram_id):
        db = self.mysql_connect()
        try:
            sql = """
            UPDATE `user`
            SET `Email` = %s
            WHERE `LastTelegram` = %s;
            """
            cur = db.cursor()
            cur.execute(sql, (new_email, telegram_id))
            db.commit()
        except Exception as e:
            print('Ошибка в изменении почты', datetime.now(), e)
        db.close()

    def change_user_firstname(self, firstname, telegram_id):
        db = self.mysql_connect()
        try:
            sql = """
            UPDATE `user`
            SET `FirstName` = %s
            WHERE `LastTelegram` = %s
            """
            db.cursor().execute(sql, (firstname, telegram_id))
            db.commit()
        except Exception as e:
            print('Ошибка в создании нового имени', datetime.now(), e)
        db.close()

    def change_user_lastname(self, lastname, telegram_id):
        db = self.mysql_connect()
        try:
            sql = """
            UPDATE `user`
            SET `LastName` = %s
            WHERE `LastTelegram` = %s
            """
            db.cursor().execute(sql, (lastname, telegram_id))
            db.commit()
        except Exception as e:
            print('Ошибка в создании новой фамилии', datetime.now(), e)
        db.close()

    def change_user_birthday(self, birthday, telegram_id):
        db = self.mysql_connect()
        try:
            sql = """
            UPDATE `user`
            SET `Birthday` = %s
            WHERE `LastTelegram` = %s
            """
            db.cursor().execute(sql, (birthday, telegram_id))
            db.commit()
        except Exception as e:
            print('Ошибка в создании новой даты рождения!', datetime.now(), e)
        db.close()

    def change_user_role_by_email(self, email, new_role):
        db = self.mysql_connect()
        try:
            sql = """
                  UPDATE `User`
                  SET `Role` = %s
                  WHERE `Email` = %s
                  """
            db.cursor().execute(sql, (new_role, email))
            db.commit()
        except Exception as e:
            print('Ошибка в обновлении роли по Email!', datetime.now(), e)
        db.close()

    def change_user_role_by_telegram(self, telegram_id, new_role):
        db = self.mysql_connect()
        try:
            sql = """
            UPDATE `user`
            SET `Role` = %s
            WHERE `LastTelegram` = %s
            """
            db.cursor().execute(sql, (new_role, telegram_id))
            db.commit()
        except Exception as e:
            print('Ошибка в обновлении роли!', datetime.now(), e)
        db.close()

# __________ CREATE CONTRACTS ________ #
    def make_new_contract(self, user_id, section_id):
        db = self.mysql_connect()
        try:
            sql = """
            INSERT INTO `Contract` (`User`, `Section`)
            VALUES (%s, %s);
            """
            db.cursor().execute(sql, (user_id, section_id))
            db.commit()
        except Exception as e:
            print('Ошибка в создании контракта', datetime.now(), e)
        db.close()

# __________ REPORTS ________ #

    #          CREATE TABLE IF NOT EXISTS Report (
    #                   ReportID INT(10) UNIQUE AUTO_INCREMENT,
    #                   From_User INT(10) NOT NULL,
    #                   Message TEXT NOT NULL,
    #                   is_active BOOL NOT NULL DEFAULT TRUE,
    #                   creating_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    #
    #                   PRIMARY KEY (ReportID),
    #                   FOREIGN KEY (From_User) REFERENCES User (UserID) ON DELETE CASCADE
    #                 );
    #
    #                 CREATE TABLE IF NOT EXISTS Answer (
    #                   AnswerID INT(10) UNIQUE AUTO_INCREMENT,
    #                   Report INT(10) NOT NULL,
    #                   Admin INT(10),
    #                   Message TEXT,
    #                   answer_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    #
    #                   PRIMARY KEY (AnswerID),
    #                   FOREIGN KEY (Report) REFERENCES Report (ReportID) ON DELETE CASCADE,
    #                   FOREIGN KEY (Admin) REFERENCES User (UserID) ON DELETE SET NULL

    def show_answers_by_user_id(self, user_id):
        db = self.mysql_connect()
        res = ''
        try:
            sql = """      
            SELECT `Report`.`ReportID`, `Report`.`Message`, `Report`.`creating_at`,`Answer`.`AnswerID`,  `Answer`.`Message`, `User`.`FirstName`, `User`.`LastName`
            FROM `Report`
            LEFT JOIN `Answer` ON `Answer`.`Report` = `Report`.`ReportID`
            LEFT JOIN `User` ON `Answer`.`Admin` = `User`.`UserID`
            WHERE `Report`.`From_User` = %s
            ORDER BY `Report`.`creating_at`;
                    """
            cur = db.cursor()
            cur.execute(sql, (user_id,))
            res = cur.fetchall()
        except Exception as e:
            print('Ошибка в просмотре ответов!', datetime.now(), e)
        db.close()
        return res

    def make_new_report(self, user_id, message):
        db = self.mysql_connect()
        try:
            sql = """
            INSERT INTO `Report` (`From_User`, `Message`)
            VALUES (%s, %s);
            """
            db.cursor().execute(sql, (user_id, message))
            db.commit()
        except Exception as e:
            print('Ошибка в создании репорта', datetime.now(), e)
        db.close()

    def check_reports(self):
        db = self.mysql_connect()
        res = ''
        try:
            sql = """
            SELECT `Report`.`ReportID`, `Report`.`From_User`, 
            `User`.`FirstName`, `User`.`LastName`, `User`.`Email`, 
            `Report`.`Message`, `Report`.`creating_at`
            FROM `Report`
            INNER JOIN `User` ON `User`.`UserID` = `Report`.`From_User`
            WHERE `Report`.`is_active`
            ORDER BY `Report`.`creating_at`;
            """
            cur = db.cursor()
            cur.execute(sql)
            res = cur.fetchall()

        except Exception as e:
            print('Ошибка в просмотре репортов!', datetime.now(), e)
        db.close()
        return res

    def make_answer_on_report(self, report_id, admin_id, message):
        db = self.mysql_connect()
        try:
            sql = """
            INSERT INTO `Answer` (`Report`, `Admin`, `Message`)
            VALUES (%s, %s, %s);
            """
            db.cursor().execute(sql, (report_id, admin_id, message))

            sql = """
            UPDATE `Report`
            SET `is_active` = False
            WHERE `ReportID` = %s;
            """
            db.cursor().execute(sql, (report_id,))

            db.commit()


        except Exception as e:
            print('Ошибка в создании ответа на репорт', datetime.now(), e)
        db.close()



