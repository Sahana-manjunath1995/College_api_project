## Flask-MYSQL college web application

   This project aims at creating website for retrieving information regarding students, teachers and library. I have used Flask for creating endpoints and a flask-sqlalchemy library to create table modules and run SQL queries, finally containerizing the application and its deployment in docker. API documentation is done by using swagger.


## System design for Flask-MYSQL college web application 
![image](https://user-images.githubusercontent.com/115713117/223188858-96928c72-42a2-4f0f-b444-74e18639c267.png)


## Data model - Schema design for database

   - Create schema design, before creating database in Mysql

 ![dbmodel](https://user-images.githubusercontent.com/115713117/208238709-cd6ed3bc-3d62-45e2-ae75-7cc3f07f98bf.PNG)


## Requirements

   - Docker
      1. mariadb:latest image
   - Flask
   - flask_sqlalchemy
   - flask_swagger_ui


## Installation of docker in Ubuntu-wsl

   1. Check if the system is up-to-date using the following command:
  
```bash
$ sudo apt-get update
```

   2. Install Docker using the following command:
   
```bash   
$ sudo apt install docker.io
```

   3. Install all the dependency packages using the following command:
   
```bash 
$ sudo snap install docker
```

   4. Before testing Docker, check the version installed using the following command:

```bash 
$ docker --version
```

## Containerizing the flask application

   1. Create Dockerfile in app folder
      - refer : ./app

   2. Create requirement.txt file in app folder for listing all the dependencies
      - refer : ./app

   3. Create docker-compose.yml file in application root directory.
      - refer : application root directory

   4. Command for building containers
```bash 
docker compose up -d --build
```

   5. Container is created by using Dockerfile

   6. Connection between containers is done using docker-compose.yml


## Login to mysql

  1. Connecting localhost to container in docker using TCP method
```bash 
$ mysql --host=localhost --protocol=TCP -uroot -proot
```
                  or
                  
  2. Start the container and run the following commands
```bash 
$ docker start contaner_name
```
```bash 
docker exec -it contaner_name bash
```
```bash 
$ mysql -uroot -proot
```

  3. After login create database named 'College' and insert data into table based on relationship given in data model


## Folder structure for the project

      .
      ├── app
      │   ├── Dockerfile
      │   ├── __init__.py
      │   ├── database
      │   │   ├── controllers.py
      │   │   └── models.py
      │   ├── requirements.txt
      │   ├── static
      │   │   ├── swagger.json
      │   │   └── swagger.yaml
      │   ├── templates
      │   │   └── 404.html
      │   └── views
      │       └── controllers.py
      ├── config.py
      ├── docker-compose.yml
      ├── readme.md
      └── run.py


## Module Requirements

   This module requires the following modules:

   - from flask import Flask, render_template
   - from flask_sqlalchemy import SQLAlchemy
   - from flask_swagger_ui import get_swaggerui_blueprint


## Installation
```bash 
$ pip install -U Flask
```
```bash
$ pip install -U Flask-SQLAlchemy
```


## Configuration

   - Create config file with the following configuration keys:

   1. SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@db:3306/College'
   2. SQLALCHEMY_TRACK_MODIFICATIONS = False


## API documentation using swagger

   1. Open console
```bash 
pip install flask_swagger_ui
```

   2. Open the app folder where Flask app is instantiated and add to the top
```bash 
from flask_swagger_ui import get_swaggerui_blueprint
```

   3. Add a folder to the application root directory and name it static.

   4. Create a new file in it and name it swagger.yml

   5. Add some Swagger specific blueprint code after you instantiate Flask
```bash 
app = Flask(__name__)

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
   SWAGGER_URL,
   API_URL,
   config={
      'app_name': "Seans-Python-Flask-REST-Boilerplate"
   }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
```

6. Add the minimum yml to the swagger.yml file
```bash 
Example:
openapi: 3.0.3
info:
 description: College-Information
 version: 1.0.11
 title: College API
 contact:
   email: sahana95man@gmail.com
servers:
- url: "http://127.0.0.1:5000"
tags:
- name: College
 description: College API for requesting information on students, teacher and library
```
7. Describe the paths, and specify the request method in swagger.yml
```bash 
Example:
 paths:
"/personal-info/":
  get:
    operationId: getSahana
    tags:
    - Student-information
    summary: Returns student's information
    responses:
      '200':
        description: OK
        content:
          application/json:
            schema:
              type: object
```

8. Run the application file (run.py)

   ![collegedb](https://user-images.githubusercontent.com/115713117/208236786-f13cfe0d-7d2d-4755-9399-1918ac5d7372.PNG)

9. Click on GET > try it out > execute

   ![request](https://user-images.githubusercontent.com/115713117/208237350-433d6f23-b899-4296-a633-5dd9a0ca3aec.PNG)

## Conclusion
I found flask-sqlalchemy as one of the easiest library because it is a flask extension that adds support for SQLAlchemy and provides tools and methods to interact with database and Flask applications. Flask is a lightweight web application framework that makes use of python to build simple websites and makes our work much easier. It would be a great choice for beginners to start with flask to learn more about web development. By containerizing the application you will gain more knowledge on how to use docker in your projects. Flask swagger UI helps you to document your AP and interact with the API

## Extra information

### How to copy the Database Dump to the Destination Server?
```bash 
$ docker cp student_data 952803436d01:/var/data/mysql
```


### How to restore the dump?
```bash 
 mysql -uroot -proot College < student_data
 ```


