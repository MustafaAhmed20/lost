# lost
The server side of "The Lost" project, which is an app to help find the lost people especially the children

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

you need to have Python 3.6.3 or later

Then install the requirements with:

```
pip install -r requirements.txt
```
you need to have a file ``` .env ``` in side ```project/ ``` directory with those variables:

```
SQLALCHEMY_DATABASE_URI = #your database URL

secret1 = secret string for security
secret2 = secret string for security
```

## Running the tests

```
python run.py
```

## Built With

* [Flask](https://flask.palletsprojects.com/en/1.1.x/) - The web framework used

## Authors

* **Mustafa Ahmed** - *Initial work* - [MustafaAhmed](https://github.com/MustafaAhmed20)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details