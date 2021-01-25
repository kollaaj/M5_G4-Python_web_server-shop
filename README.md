# Module 5 Python Flask web server

This is a front-end web server made with Python Flask that uses an API found on https://github.com/kollaaj/Module_5_python_API_server to manage product listings.

The technologies used are Python Flask, Jinja2, SCSS and Python Requests.

## Start web server on Windows PowerShell

``` 
$env:FLASK_ENV = "development"
$env:FLASK_APP = "app.py"
flask run
```

## Start web server on Linux
```
export FLASK_ENV=development
export FLASK_APP=app.py
flask run
```

To view the website after having started the server, navigate to http://localhost:5000.

Live version: https://mod5.kolbrun.io

