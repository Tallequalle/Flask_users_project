Файл "config.ini" включает конфигурационные записи, необходимые для работы. В файле "models.py" находится модель определения объекта пользователь. В папке templates находятся html шаблоны для ответов. Главный файл проекта "start_app.py" используется для запуска и управления проекта. Проект доступен при переходе на порт 8000.

Виртуальное окружение для проекта создается командой "virtualenv venv". Для запуска используйте команду "source venv/bin/activate". Для выхода из виртуального окружения - "deactivate".

Необходимые пакеты проекта хранятся в файле "requirements.txt". Импортируются командой "pip install -r requirements.txt".

Для создания пользователя, необходимого для работы с базой данных необходимо выполнить следующие команды:
	psql -U postgres
	CREATE DATABASE database_flask;
	\c database_flask;
	CREATE USER test_user with PASSWORD '1234554321';
	GRANT ALL PRIVILEGES ON TABLE users TO test_user;
	GRANT USAGE, SELECT ON SEQUENCE users_user_id_seq TO test_user;

Для создания необходимой таблицы используйте команду:
	"CREATE TABLE users (
	user_id serial PRIMARY KEY, 
	username varchar(50) unique not null, 
	password varchar(50) not null);"
	
Главная страница доступна по адресу url "http://localhost:8000/"
