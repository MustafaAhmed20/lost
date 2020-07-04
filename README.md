# Lost

The server side of "The Lost" project, which is an app to help find the lost people especially the children

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

you need to have Python 3.6.3 or later

Then install the requirements with:

```
pip install -r requirements.txt
```

you need to have a file ``` .env ``` inside ```project/ ``` directory with those variables:


```
SQLALCHEMY_DATABASE_URI = # your database URL
DATABASE_NAME_DEVELOPMENT = # the development database name
DATABASE_NAME_TESTING = # the testig database name

secret1 = # secret string for security
secret2 = # secret string for security

admin_pass = # admin password
admin_phone = # admin Phone number

IMEGE_TEST_NAME = # name of photo for testing
```

**warning:** you need to get sure those variables set correctly or you will get weird errors thrown on you!

i used mysql database , so the QLALCHEMY_DATABASE_URI = mysql://username:password@server/

``` admin_pass ``` and ``` admin_phone ``` used with default data in testing and development

## Running the tests
use this command to run all the tests in ```tests\```

```
python -m unittest
```

## warning

In those files ``` \project\run.py``` and ``` \project\tests\__init__.py``` there is database connection specific for mysql . you may consider change it for other type of databases!

## Running the app

```
python run.py
```

## Built With

* [Flask](https://flask.palletsprojects.com/en/1.1.x/) - The web framework used

## Authors

* **Mustafa Ahmed** - *Initial work* - [MustafaAhmed](https://github.com/MustafaAhmed20)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details