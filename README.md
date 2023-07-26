# viewed-list
Данная программа представляет собой электронный список просмотренного или прочитанного.
![screenshot 1](https://github.com/Yulya-S/viewed-list/blob/main/screenshots/screenshot_1.jpg)
![screenshot 2](https://github.com/Yulya-S/viewed-list/blob/main/screenshots/screenshot_2.jpg)
![screenshot 3](https://github.com/Yulya-S/viewed-list/blob/main/screenshots/screenshot_3.jpg)
![screenshot 4](https://github.com/Yulya-S/viewed-list/blob/main/screenshots/screenshot_4.jpg)
![screenshot 5](https://github.com/Yulya-S/viewed-list/blob/main/screenshots/screenshot_5.jpg)

### В программе реализованны следующие функции:
1. возможность регистрации нескольких пользователей, защищенных паролем.
2. настройки для каждого пользователя:
    - изменение приоритетного раздела
    - изменение цветовой гаммы программы из 9 возможных цветовых палитр
    - изменение варианта сортировки из 2 предложенных(по алфавиту, по дате добавления начиная со старых)
3. подсказки по использованию программы
4. добавление собственных разделов (Фильмы, Книги, Аниме, Манга и т.п)
5. удаление разделов возможно если ни у кого из пользователей он не является приоритетным и не имеет записей
6. возможнось сортировки записей(по названию, разделу, статусу) и разделов(по названию)
7. добавление и изменение созданых записей о тайтлах:
    - выбор статуса записи(не начатое, начатое, жду продолжение, не понравилось, закончено)
    - оценка по пятибальной шкале для завершённых записей
    - отметка номера большого блока и части начатой записи
    - возможность добавить заметку о записи
    - удаление записи если она находится в статусе не начата или не понравилась
### Структура программы:
- images - папка со всеми изображениями
- base - папка с базой данных (создается автоматически)
- code
    - coefficients.py - файл со всеми коэфициентами
    - items.py - файл со всеми объектами
    - data_base - файл со всеми функциями относящимися к базе данных
### В программе используются библиотеки:
- pygame
- sqlite3
- base64
- os

