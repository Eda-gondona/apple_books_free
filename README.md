# books_free
Этот проект представляет собой сервер RESTAPI с фронтендом и бд также это хороший код для понимания работы backend с frontend  и также для понимания RESTAPI .Его можно запустить и он будет работать 

# Features
1 - Аутентификация по электронной почте и паролю с использованием безопасных алгоритмов
2 - Эффективное управление рабочими процессами: перезапуск, ограничение по времени, максимальный срок службы
3 - Управление базами данных и миграции
4 - Схемы инициализации баз данных для PostgreSQL и SQLite
5 - Простой интерфейс для входа/регистрации/забытого пароля/сброса пароля

# Building Blocks
Python is a high-level and versatile scripting language that provides powerful features with an exceptionally clear syntax.

The language is well designed and has received increased fame and popularity over the recent years. Huge number of developers are picking Python in their work. In Sep 2017, a StackOverflow study writes about The Incredible Growth of Python: "Python has a solid claim to being the fastest-growing major programming language." In the TIOBE index Python stands at position 3 as of Sep 2018.

Having been coding Python professionally for close to two decades, I can say it has boosted my productivity and still is my primary language for many tasks, including developing the business logic in the back-end.

Flask is the Python web framework. Flask is considered as an unopinionated micro-framework that only provides the essentials of a web framework without enforcing other components (like database, orm, admin interface, sessions etc.) As a webdev veteran I appreciate this flexibility since I do want to pick the best of breed components myself. The core stays but other needs may vary from project to project, from Raspberry to the AWS cloud. The flexibility lets me be in control and simplify.

uwsgi is the master daemon that runs and supervises the Python worker processes. uwsgi has a list of power features that are essential to a robust back-end: timecapped requests, recycling of workers, background tasks, cron jobs, timers, logging, auto reloads on code change, run-as privileges. uwsgi is configured via the uwsgi.ini file.

PostgreSQL is the main database, "the most advanced open source database" that is getting stronger every year. PostgreSQL is a powerhouse of features with a rock-solid implementation. Personally I enjoy the JSON functionality the most, since it provides good amount of flexibility to the relational model that I still prefer in a master database over the schema-free solutions.

Someone wrote an article saying PostgreSQL is the worlds' best database.

Note that the code also supports SQLite database. SQLite maybe convenient in a lighter setup if the full power of PostgreSQL is not needed such as in a Raspberry.

Redis is a persistent in-memory database that is used as a storage for server-side session data and as a lightweight caching and queueing system. Fast and solid.

Peewee is a straightforward database ORM library. It is small and easy to learn, and has all the necessary features. I favor the simplicity of the ActiveRecord pattern with 1-1 mapping of classes and database, as opposed to more complex data mapper pattern that is followed by the big SQLAlchemy library. I know SQL and like to operate at the row level, and have explicit control. Peewee makes database access a breeze and allows you to execute raw SQL if you need the full power of the database. Peewee supports SQLite, MySQL and PostgreSQL.

For scheme migrations, Peewee-migrate is an easy choice that fits well with Peewee.
