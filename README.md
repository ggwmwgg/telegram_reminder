<table align="right">
 <tr><td><b><img src="https://github.com/ggwmwgg/ggwmwgg/blob/main/images/us_s.png" height="13" alt=""> English</b></td></tr>
 <tr><td><a href="README_ru.md"><img src="https://github.com/ggwmwgg/ggwmwgg/blob/main/images/ru.png" height="13" alt=""> Русский</a></td></tr>
</table>
## Notifications Telegram Bot (Aiogram)

### Description
```Manager``` sends link to Google Sheets ([Смотреть Пример](https://docs.google.com/spreadsheets/d/1vBHTh28dYkEt1_PDrR8PVa5tyzvFGb2ufEWTcnwzZy0/ "Пример")) data loaded to db, worker gets notification with inline keyboard attached (Done/Not completed). If an employee does not press any of the buttons within ```answer_time```, buttons are removed and the manager receives a corresponding notification. If, however, the employee pressed one of the buttons, the manager receives a notification on which one exactly, and the keyboard is also removed
Было создано несколько обработчиков и функций:
- ```/start``` - The start command that adds the user to the database.
- ```/m_add TG_ID``` - Command for adding a manager to the database.
- ```handlers/users/acl_test``` - Handler for the operation of the command above.
- ```handlers/users/echo``` - Processing of unknown commands.
- ```handlers/users/start``` - Processing of basic requests (registration, sending data by the manager, processing button presses in the notification).
- ```data/config.py``` - Configuration file that stores data for connecting to the database, Telegram API Token, as well as administrator IDs.
- ```utils/db_api/db_api.py``` - File with functions for working with the database, checking the latest notifications and sending them.
- ```utils/db_api/models.py``` - File with database models.
- ```utils/get_data.py``` - File with a function that takes a link and returns a list of dictionaries for further addition to the database.
- ```utils/notify_admins.py``` - File with a function that sends a notification to the administrator.
- The bot also has flood control.
- The function for removing the keyboard from notifications includes clearing from already completed tasks.

#### Technologies used:
- *Python*
- *Aiogram*
- *Asyncio*
- *Pandas*
- *Tortoise ORM*
- *PostgreSQL*
- *Docker*
- *Docker-compose*

#### Configuration:
- Set your data for connecting to PostgreSQL and Telegram API Token in ```.env.dist```, rename it to ```.env```.
- Set your Telegram ID in data/config.py on line ```7```.
- Set your data for the healthcheck in ```docker-compose.yml``` on line 23.
- Build the containers using ```docker-compose build```.
- Start the containers using ```docker-compose up```, you can add the ```-d``` flag to run in the background.
- To stop the containers, use ```docker-compose down```.

#### Usage:
- After setting yourself as an administrator, in the bot, after starting, write the command ```/m_add TG_ID``` where ```TG_ID``` is the ID manager ```Telegram ID```.
- To upload data, follow the instructions and structure indicated in the examples.

#### Contributing
Pull requests are welcome. For major changes please open an issue first.