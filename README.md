# PBSpy — A Civ4 Pitboss webinterface based on Django

This software communicates with the PB Mod component of PBStats and provides
functions to show the game status, a game log and to administrate the game.

## Usage
1. Visit https://civ.zulan.net/pbspy or install this software on your own server.
2. Create an account on the new page and login.
3. Start/load a PitBoss-game which implements the PB Mod and click on "Register new PitBoss".
4. Enter the host name, port and password (defined in pbSettings.json), of the PB game and click on "Register".
5. As admin, you had now access on three pages:
   - 'Game overview': Available for everyone.
   - 'Edit game' page: To change connection details and the data shown in the overview.
   - 'Manage game': Administration site of the Pitboss server. Save/Load your games here.


## Installation of Django + Django packages with pip

Here, we assume python3 >= python3.8.
It is recommended to install the software with poetry.

### Dependencies

```
sudo apt install python3-poetry node-less
sudo apt install default-libmysqlclient-dev
poetry install
```

### Configuration
Copy `civdj/settings_local.example.py` to `civdj/settings_local.py` and adapt it to your environment. (See https://docs.djangoproject.com/en/dev/ref/settings/ for details.)

Without changes PBSpy will use Sqlite 3 as database backend. Look into the Django docs
for other setups.


### Prepare environment

This uses Debug mode. Release mode requires more steps.

```
poetry run python manage.py migrate
poetry run python manage.py migrate static_precompiler
poetry run python manage.py compilestatic
poetry run python manage.py collectstatic
poetry run python manage.py createsuperuser
```

### Local server start

```
poetry run python manage.py runserver 0.0.0.0:8000
```

### Running in apache with WSGI

Example:
```
WSGIScriptAlias /pbspy /home/civweb/pbspy/civdj/wsgi.py
WSGIDaemonProcess civ.zulan.net python-home=/home/civweb/pbspy/.venv python-path=/home/civweb/pbspy
WSGIProcessGroup civ.zulan.net
WSGIApplicationGroup %{GLOBAL}
```

### Update of Localization

```
poetry run python manage.py makemessages -l de
[Editing po file, e.g insert new translations ]
poetry run python manage.py compilemessages -l de
```


## Known issues

- Error: `ENOENT: no such file or directory, mkdir '[...]/static/COMPILED/pbspy/less/defaultstyle'`

  while running 'python3 manage.py compilestatic'
  
  Solution: Create above folder manually (simply use 'mkdir -p' instead of 'mkdir')

- Error during migrate:

  ```
  There is no South database module 'south.db.sqlite3' for your database. Please either choose a supported database, check for SOUTH_DATABASE_ADAPTER[S] settings, or remove South from INSTALLED_APPS.
  ```

  Could be solved by uninstalling south, i.e.
  `sudo pip uninstall South`

- Error `'Settings' object has no attribute 'H:i:s'":`

  ?
