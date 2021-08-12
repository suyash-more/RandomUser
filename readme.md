# Random User API

Used this [API](https://randomuser.me/) for the user creation method / populating the database

Start the project

Create a virtual environment for your code
```shell
$ python -m venv venv
```

Activate the environment and install the dependencies
```shell
$ venv\Scripts\activate
$ pip install --upgrade pip
$ pip install -r requirements.txt
```

Make migrations to the database
```shell
$ py manage.py makemigrations
$ py manage.py migrate
```

Start your development server
```shell
$ py manage.py runserver
```

You can view your development server [here](http://127.0.0.1:8000/) 