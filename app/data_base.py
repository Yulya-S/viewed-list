import sqlite3
import base64
from os import mkdir
from os.path import exists

if not exists('./base'):
    mkdir('./base')

class Data_base():
    def __init__(self):
        self.db = sqlite3.connect('./base/base.db')
        self.cursor = self.db.cursor()
        self.create_tables
        self.cursor.execute("SELECT * FROM `sections`")
        if len(self.cursor.fetchall()) == 0:
            self.cursor.execute("""INSERT INTO `sections` (`title`, `bloc_name`, `chapter_name`, `display`)
                                VALUES (?,?,?,?)""", ('Фильм', '', '', 0))
            self.db.commit()

    @property
    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nickname VARCHAR(255),
                password VARCHAR(255),
                favorite_section_id INTEGER,
                color_box INTEGER,
                order_by INTEGER,
                FOREIGN KEY (`favorite_section_id`) REFERENCES `sections`(`id`)
                );
            """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS sections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title VARCHAR(255),
                bloc_name VARCHAR(255),
                chapter_name VARCHAR(255),
                display INT(2)
            );
            """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS titles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INT,
                section_id INT,
                title VARCHAR(255),
                status INT(4),
                bloc INT,
                chapter INT,
                note VARCHAR(255),
                stars INT,
                FOREIGN KEY (`user_id`) REFERENCES `users`(`id`),
                FOREIGN KEY (`section_id`) REFERENCES `types`(`id`)
            );
            """)


db = Data_base()


def delete_last_element(id: int, table_name: str):
    db.cursor.execute("SELECT seq FROM `sqlite_sequence` WHERE name = ?", (table_name,))
    count = db.cursor.fetchall()
    if len(count) != 0 and id == count[0][0]:
        db.cursor.execute("UPDATE `sqlite_sequence` SET seq = ? WHERE name = ?", (int(count[0][0]) - 1, table_name))
        db.db.commit()


def exceeding_number_of_records(table_name: str):
    if table_name == 'titles':
        db.cursor.execute("SELECT * FROM `titles`")
    elif table_name == 'sections':
        db.cursor.execute("SELECT * FROM `sections`")
    elif table_name == 'users':
        db.cursor.execute("SELECT * FROM `users`")
    return len(db.cursor.fetchall()) < 9223372036854775807


def encrypt_password(password: str):
    return base64.b64encode(password.encode("utf-8"))


def add_section(title: str, bloc_name: str, chapter_name: str, display: int):
    if section_not_exist(title):
        db.cursor.execute("INSERT INTO `sections` (`title`, `bloc_name`, `chapter_name`, `display`) VALUES (?,?,?,?)",
                          (title, bloc_name, chapter_name, display))
        db.db.commit()
        return (True,)
    return (False, 'Такой раздел уже существует!')


def section_not_exist(title: str):
    db.cursor.execute("SELECT * FROM `sections` WHERE title = ?", (title,))
    return len(db.cursor.fetchall()) == 0


def delete_section(id: int):
    section = select_section_by_id(id)
    if section and not section_not_exist(section[1]) and number_of_titles_related_to_section(id) == 0 and \
            not find_users_with_section(id):
        delete_last_element(id, 'sections')
        db.cursor.execute("DELETE FROM `sections` WHERE id = ?", (id,))
        db.db.commit()
        return True
    return False


def select_section_by_id(id: int):
    db.cursor.execute("SELECT * FROM `sections` WHERE id = ?", (id,))
    response = db.cursor.fetchall()
    if len(response) != 0:
        return response[0]


def select_section_by_title(title: str):
    db.cursor.execute("SELECT * FROM `sections` WHERE title = ?", (title,))
    response = db.cursor.fetchall()
    if len(response) != 0:
        return response[0]
    return False


def number_of_titles_related_to_section(id: int):
    db.cursor.execute("SELECT * FROM `titles` WHERE section_id = ?", (id,))
    response = db.cursor.fetchall()
    if len(response) != 0:
        return len(response[0])
    return 0


def append_user(nickname: str, password: str):
    password = encrypt_password(password)
    section = select_section_by_title(get_section_names()[0][0])
    if section and user_not_exist(nickname):
        db.cursor.execute("""INSERT INTO `users` (`nickname`, `password`, `favorite_section_id`, `color_box`, `order_by`)
                            VALUES (?,?,?,?,?)""", (nickname, password, section[0], 1, 1))
        db.db.commit()
        return (True,)
    return (False, 'Такой пользователь уже существует')


def user_not_exist(nickname: str):
    db.cursor.execute("SELECT * FROM `users` WHERE nickname = ?", (nickname,))
    return len(db.cursor.fetchall()) == 0


def delete_user(nickname: str, password: str):
    user_content = select_user(nickname, password)
    if user_content[0]:
        delete_all_user_titles(user_content[1][0])
        print(user_content[1][0])
        delete_last_element(user_content[1][0], 'users')
        db.cursor.execute("DELETE FROM `users` WHERE id = ?", (user_content[1][0],))
        db.db.commit()
        db.cursor.execute("SELECT COUNT(id) FROM `users`")
        result = db.cursor.fetchall()[0]
        if result and result[0] == 0:
            db.cursor.execute("UPDATE `sqlite_sequence` SET seq = 0 WHERE name = 'users'")
            db.db.commit()
        return (False, 'Пользователь успешно удален')
    return (False, 'Данные введены неверно')


def delete_all_user_titles(user_id: int):
    db.cursor.execute("DELETE FROM `titles` WHERE user_id = ?", (user_id,))
    db.db.commit()
    db.cursor.execute("SELECT COUNT(id) FROM `titles`")
    result = db.cursor.fetchall()[0]
    if result and result[0] == 0:
        db.cursor.execute("UPDATE `sqlite_sequence` SET seq = 0 WHERE name = 'titles'")
        db.db.commit()


def append_title(user_id: int, section_name: str, title: str, status='0', bloc=1, chapter=1, note='', stars=0):
    section = select_section_by_title(section_name)
    if section and title_not_exist(user_id, section[0], title):
        db.cursor.execute("""INSERT INTO `titles` (`user_id`, `section_id`, `title`, `status`, `bloc`, `chapter`,
                            `note`, `stars`) VALUES (?,?,?,?,?,?,?,?)""",
                          (user_id, section[0], title, status, bloc, chapter, note, stars))
        db.db.commit()
        return (True,)
    if not section:
        return (False, 'Такой раздел не существует')
    else:
        return (False, 'Такое название уже существует')


def title_not_exist(user_id: int, type_id: int, title: str):
    db.cursor.execute("SELECT * FROM `titles` WHERE user_id = ? AND section_id = ? AND title = ?",
                      (user_id, type_id, title,))
    return len(db.cursor.fetchall()) == 0


def delete_title(id: int):
    delete_last_element(id, 'titles')
    db.cursor.execute("DELETE FROM `titles` WHERE id = ?", (id,))
    db.db.commit()
    db.cursor.execute("SELECT COUNT(id) FROM `titles`")
    result = db.cursor.fetchall()[0]
    if result and result[0] == 0:
        db.cursor.execute("UPDATE `sqlite_sequence` SET seq = 0 WHERE name = 'titles'")
        db.db.commit()


def select_titles(user_id: int, section_name: str, piece_of_name: str, status, order_by: int):
    if status not in ['Не начато', 'Начато', 'Жду продолжения', 'Не понравилось', 'Завершено']:
        status = 5
    else:
        status = ['Не начато', 'Начато', 'Жду продолжения', 'Не понравилось', 'Завершено'].index(status)
    piece_of_name = '%' + piece_of_name + '%'
    if order_by == 0:
        order_by = "ORDER BY title"
    else:
        order_by = "ORDER BY id"
    section_id = select_section_by_title(section_name)[0]
    content = (user_id, section_id, piece_of_name)
    all_status = ''
    if status != 5:
        all_status = 'AND status = ? '
        content += (status,)
    db.cursor.execute("""SELECT * FROM `titles` WHERE user_id = ? AND section_id = ? AND title LIKE ? """ + \
                      all_status + order_by, content)
    return (True, db.cursor.fetchall())


def select_title_by_id(id: int):
    db.cursor.execute("SELECT * FROM `titles` WHERE id = ?", (id,))
    response = db.cursor.fetchall()
    if len(response) != 0:
        return response[0]


def find_users_with_section(id: int):
    db.cursor.execute("SELECT favorite_section_id FROM `users`")
    result = db.cursor.fetchall()
    if len(result) != 0:
        return id in [x[0] for x in result]
    return False


def select_user(nickname: str, password: str):
    if not user_not_exist(nickname):
        db.cursor.execute("SELECT * FROM `users` WHERE nickname = ? AND password = ?",
                          (nickname, encrypt_password(password)))
        response = db.cursor.fetchall()
        if len(response) != 0:
            return (True, response[0])
    return (False, 'Данные введены неверно')


def select_user_by_id(id: int):
    db.cursor.execute("SELECT * FROM `users` WHERE id = ?", (id,))
    response = db.cursor.fetchall()
    if len(response) != 0:
        return response[0]
    return False


def get_section_names():
    db.cursor.execute("SELECT title FROM `sections`")
    return db.cursor.fetchall()


def select_section_by_pice_of_name(text=''):
    text = '%' + str(text) + '%'
    db.cursor.execute("SELECT * FROM `sections` WHERE title LIKE ? ORDER BY id DESC", (text,))
    return db.cursor.fetchall()


def update_title(id: int, section_name: str, new_name: str, status: int, bloc: int, chapter: int,
                 note: str, stars: int):
    section_id = select_section_by_title(section_name)
    title = select_title_by_id(id)
    if section_id and title:
        if new_name == title[3] or title_not_exist(title[1], title[2], new_name):
            db.cursor.execute("""UPDATE `titles` SET title = ?, section_id = ?, status = ?, bloc = ?,
                                chapter = ?, note = ?, stars = ? WHERE id = ?""",
                              (new_name, section_id[0], status, bloc, chapter, note, stars, id))
            db.db.commit()
            return (True,)
        return (False, 'Такой тайтл уже существует')
    return (False, 'Такой раздел не существует')


def update_user(user_id, section_name, color_box, order_by):
    section_id = select_section_by_title(section_name)
    if section_id and select_user_by_id(user_id):
        db.cursor.execute("UPDATE `users` SET favorite_section_id = ?, color_box = ?, order_by = ? WHERE id = ?",
                          (section_id[0], color_box, order_by, user_id))
        db.db.commit()
        return (True,)
    return (False, 'Такой раздел не существует')
