# MusicWebApp
A Music playlist app

[![Build Status](https://travis-ci.com/arpit1997/MusicWebApp.svg?token=3Uc9gKxpBA3p2jCgiRiz&branch=master)](https://travis-ci.com/arpit1997/MusicWebApp)
## How to run this code
1. pull this repository
2. set three environment variables to your machine:
  - This wil point to sender's email address in verification email.variable Name:email
  - This will point to sender's email's password.variable Name: password_a
  - This will point to encryption key.variable Name: encryption_key     Value:"1234567812345678"
3. make migrations (create database)

    `python3 manage.py makemigrations`
    
    `python3 manage.py migrate`
3. run the server

    `python3 manage.py runserver`
    
4. Go to Browser and type:

    `127.0.0.1:8000`

## License
This application is licensed under [Apache license](https://www.apache.org/licenses/LICENSE-2.0)
