
# Google Tasks(FastApi)


## Clone Project
```console
Clone with HTTPS => https://gitlab.com/inexture-python/pythonlearning/google-tasks-fastapi.git

OR 

Clone with SSH => git@gitlab.com:inexture-python/pythonlearning/google-tasks-fastapi.git
```
Current updated code is in `dev` branch. To change branch `git checkout dev`.

## Install requirements.txt
```console
pip install -r requirements.txt
```

## Add Configurations to `.env` file in root directory.
```console
DB_URL = "postgresql://postgres:postgres@localhost:5432/google_tasks"

ALGORITHM = HS256
JWT_SECRET_KEY = 09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7
JWT_REFRESH_SECRET_KEY = 11854781eada5bf61369f3f69dd0e96020c26892a7321f9358df254d0ae8f5f1
JWT_FORGOT_PASSWORD_SECRET_KEY = 88cd196c74d095eee57877aaa4353326b088cc4430744e5a99c9ff17dd7e4270

RESET_PASSWORD_LINK = http://127.0.0.1:8000/api/v1/auth/reset_password

#Mail Configuration data
MAIL_USERNAME = "Your email Username"
MAIL_PASSWORD = "Your email password"
MAIL_FROM = "Mail From Name"
MAIL_PORT = 587
MAIL_SERVER = "mail server" (for eg->'smtp.gmail.com')
MAIL_FROM_NAME = Mail From Name (for eg->'Google Task notification')

#This is for Redis Server
CELERY_BROKER_URL = "redis://localhost:6379"
CELERY_RESULT_BACKEND = "redis://localhost:6379"

#This is for Rabbitmq Server
#CELERY_BROKER_URL = 'amqp://guest:guest@localhost:5672//'

REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_DB = "postgresql://postgres:postgres@localhost:5432/google_tasks"

```

## Project Structure
This is the folder/file structure we have.
```
/google_tasks
|
├── main.py
|
├── /tasks_api
│   ├── __init__.py          ---------------> Declared Application Directory         
│   ├── constants.py         ---------------> Declared All needed constants here
│   ├── utils.py             ---------------> Common function which is used repeadately declared here
│   ├── celery_config.py     ---------------> It contain all the configuration of the celery. 
|   |
│   └── /users
│   │   ├── __init__.py
│   │   ├── hashing.py          ---------------> It contain common classs hasher for all the cryptocontext.
│   │   ├── language.py         --------------->  It contain common function of jsonable_encoder for converting data.
│   │   ├── models.py           ---------------> It contain the script of metadata.
│   │   ├── oauth2.py           ---------------> It contain common function for authentication using token.
│   │   ├── schema_validations.py  ------------> It contain common function for validation like email pswd etc.
│   │   ├── schemas.py          ---------------> It contain schemas of the models.
│   │   ├── services.py         ---------------> Intermediate Layer( All other layer's communication must happen via this layer)
│   │   └── tokens.py           ---------------> Common function which is used repeadately for creation and verification of tokendeclared here
│   │   ├── views.py            ---------------> Api Endpoints
|   |
│   └── /task_list
│   │   ├── __init__.py
│   │   ├── models.py           ---------------> It contain the script of metadata.
│   │   ├── schemas.py          ---------------> It contain schemas of the models.
│   │   ├── services.py         ---------------> Intermediate Layer( All other layer's communication must happen via this layer)
│   │   └── views.py            ---------------> Api Endpoints
|   |
│   └── /task
│   │   ├── __init__.py
│   │   ├── models.py           ---------------> It contain the script of metadata.
│   │   ├── schemas.py          ---------------> It contain schemas of the models.
│   │   ├── services.py         ---------------> Intermediate Layer( All other layer's communication must happen via this layer)
│   │   ├── tasks.py            ---------------> It contain celery tasks function for mail notifications 
│   │   └── views.py            ---------------> Api Endpoints
|   |
│   └── /sub_task
│   │   ├── __init__.py
│   │   ├── models.py           ---------------> It contain the script of metadata.
│   │   ├── schemas.py          ---------------> It contain schemas of the models.
│   │   ├── services.py         ---------------> Intermediate Layer( All other layer's communication must happen via this layer)
│   │   ├── tasks.py            ---------------> It contain celery tasks function for mail notifications
│   │   └── views.py            ---------------> Api Endpoints
| 
├── templates
│   ├── email   
       ├── alert_msg.html   ---------------> It contain the html code for alert msg. 
│      ├── email.html       ---------------> It contain the html code for alert msg.
|  
├── .env-example  or .env          ---------------> Required configuartion(Development, Production etc.) 
├── .gitignore                     ---------------> Listing all files/folders to ignore in git commits   
├── database.py                    ---------------> Required configuartion(Development, Production etc.)
├── alembic.ini                    ---------------> It contain alembic configuartion for migrations(Development, Production etc)
├── /migrations                    ---------------> It contain all the files & folder related to migrations(Development, Production etc) 
├── README.md                      ---------------> Documentation on project code
├── requirements.txt               ---------------> Required Packages and Third party libraries
└── /testing                       ---------------> For testing the project code [ test-cases ]
```


# Overview of project structure

Root folder main-project-directory that contains the project specific file under google tasks
directory and the files like requirements.txt, alembic.ini, migrations, .gitignore, .env, etc.

#### google_tasks Project

*1. \_\_init__.py*
* Configure Application Factory.
    * Create a FastApi app object, Configure app object using config file
    * Initialize plugins which is globally accessible
    * Imported routes and register Blueprints


*2. language.py(langauge layer file)*
* This layer can only communicate with the service layer.
    * It Processes the client request APIs data and serialize data(if required) and send response according to the requirement to the client.
    * For example, convert response data according to  success/fail response etc.This all kind
      of methods we can perform in this layer.

*3. constants.py*
- All App level constants are defined in here, right now we preferred to put all string constants in the single file so if we need to do multilingual app it can be useful to have all strings in single place.

### Module folders [folder/s]
* All the modules(app) must have their own package which works as an abstraction for itself.In this project has 4 modules(app)
    1. Users -- It contains User authentication related APIs etc.
    2. Task_list -- It contains task_list related APIs etc.
    3. Tasks -- It contain tasks related API etc.


# *Module level files*

* It's best practice to have internal dependency and calling hierarchy like below.
    * Module(app) can have some layers as per the requirements.

## 1. Views Layer:

### *view(routes).py*
* This file code should be just having the API end points and nothing else.
    * It's only responsibility is to have all the routes for that module.
    * This file can only interact with services.py.

## 2. Service Layer:
### *services.py*
* This file is kind of act as mediator between views and all other layers.

## 3. Language Layer:
### *languages.py*
* In this project , it's not required to create language.py at module level , but if required ww need to create it.

## 4. utils.py:
* Here we need to define extra utilities.
    * Here we define functions which might repeatedly used in python package.

## Files at root level
*1. config.py*
- This File is responsible for extracting variable value for .env file and assign to
  configuration variable according to requirements(like development, production etc.)

*2.requirements.txt*
* All required packages

*3. .env*
* It contains all SECRET and sensitive variables
* .env-example is the demo for creation the .env file

*4.main.py*
* Entry point of our project.

## Modules(Endpoints) Description: 
## Main 3 modules

- Task_list
- Tasks
- Sub_tasks


## Module #1 Task List

#### task_list
In this we have 5 endpoints

```http

POST   /api/v1/create/task_list (Create)
GET    /api/v1/get_all/task_list (Show All)
GET    /api/v1/get_one/{list_id}/task_list (Show One)
PUT    /api/v1/update/{list_id}/task_list (Update)
DELETE /api/v1/delete/{list_id}/task_list (Delete)

```

## Module #2 Tasks
#### tasks
In this we have 5 endpoints

```http

POST   /api/v1/create/{list_id}/task (Create)
GET    /api/v1/get_all/{list_id}/task (Show All)
GET    /api/v1/get_one/{task_id}/task (Show One)
PUT    /api/v1/update/{task_id}/task (Update)
DELETE /api/v1/delete/{list_id}/task (Delete)

```
## Module #3 Sub Tasks
#### sub_tasks
In this we have 5 endpoints

```http

POST   /api/v1/create/{task_id}/sub_task (Create)
GET    /api/v1/get_all/{task_id}/sub_task (Show All)
GET    /api/v1/get_one/{sub_task_id}/sub_task (Show One)
PUT    /api/v1/update/{sub_task_id}/sub_task (Update)
DELETE /api/v1/delete/{sub_task_id}/sub_task (Delete)

```
