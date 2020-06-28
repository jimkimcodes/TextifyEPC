# Textify - Django Channels

Clone the project to your local system

```git clone https://github.com/Deepzzz54321/TextifyEPC.git```

Create a virtual environment inside the cloned directory

```python -m venv myvenv```

Activate the virtual Environment

```myvenv\Scripts\activate```

Install Requirements

```pip install -r requirements.txt```

## Database Configuration

Launch the Postgres console by running ```psql```.

Create an authentication user and grant privileges to this user.
```
CREATE USER chatadmin;
ALTER USER chatadmin WITH PASSWORD 'chat12345';
```

Create 'chatdb' database.

```
CREATE DATABASE chatdb OWNER chatadmin;
```

## Django Configuration

Open the settings.py file of the Django project. Change ```DATABASES = ``` to
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'chatdb',
        'USER': 'chatadmin',
        'PASSWORD': 'chat12345',
        'HOST': 'localhost',
        'PORT': '',
    }
}
```
Migrate and create new superuser(admin) by providing eMail and password using CLI
```
python manage.py migrate
python manage.py createsuperuser
```
Make sure that you have opened up your redis server. 

That's it. Your local server is ready to run!
```
python manage.py runserver
```

Your Textify - Chat App is ready to go!
