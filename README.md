# Проект "Социальная сеть"

Этот проект представляет собой простую социальную сеть, где пользователи могут создавать посты, оставлять комментарии и обмениваться мнениями.

## Установка

1. Клонируйте репозиторий на свой локальный компьютер:

```bash
git clone https://github.com/velikiykeamil/social_network.git
```

2. Перейдите в каталог проекта:

```bash
cd social-network
```

3. Установите и поделючите виртуальное окружение:

```bash
virtualenv venv
```

```bash
source venv/bin/activate
```

4. Установите зависимости:

```bash
pip install -r requirements.txt
```

## Использование

1. Запустите приложение:

```bash
python manage.py
```

2. Перейдите по адресу [http://localhost:5000](http://localhost:5000) в вашем веб-браузере.

3. Зарегистрируйте новый аккаунт или войдите существующими учетными данными.

4. Создайте новый пост, просмотрите существующие посты, оставьте комментарий или удалите пост.

## Функции

- Регистрация новых пользователей.
- Аутентификация и авторизация пользователей.
- Создание, просмотр, редактирование и удаление постов.
- Оставление комментариев к постам.
- Обновление профиля пользователя с загрузкой изображения.

## Технологии

- Flask - микрофреймворк для веб-приложений на языке Python.
- SQLAlchemy - ORM (Object-Relational Mapping) для работы с базой данных.
- Flask-WTF - расширение для работы с формами в Flask.
- Flask-Login - управление сеансами пользователей в Flask.
- Flask-Migrate - инструмент для управления миграциями базы данных.
- Werkzeug - набор утилит для создания веб-приложений.
- Bootstrap - фреймворк для разработки веб-интерфейсов.

## Автор

[Keamil](https://github.com/Raphailinc)