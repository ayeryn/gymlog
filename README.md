# README

## Flask

## ORM
### SQLALCHEMY
### flask-migrate

### flask-mail
#### Python email server emulator   
The module doesn't actually send out any mails. It will print the body of the email out to the console.
```console
$ python -m smtpd -n -c DebuggingServer localhost:8025
$ export MAIL_SERVER=localhost
$ export MAIL_PORT=8025
```

Using the GMAIL Server
```console
$ export MAIL_USERNAME = ...
$ export MAIL_PASSWORD = ...
```


### PyJWT
PyJWT is a Python library which allows you to encode and decode JSON Web Tokens (JWT). This project utilizes PyJWT for user authentication and password reset.

## Forms
```console
$ pip install flask-wtforms
```
### wtforms

## Setting up development environment

.profile
```console
$ va  # activate virtual env
$ setapp  # set FLASK_APP env
$ fenv  # display set FLASK_* env variables

.gymlog

```