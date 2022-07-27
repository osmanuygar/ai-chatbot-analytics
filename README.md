# Chatbot Analytics
This API is a Rest API of chatbot performance analysis.  

<img width="800" alt="image" src="https://user-images.githubusercontent.com/45356325/181238738-62b575be-2384-4911-bb81-0c6f2d519f65.png">

## Installation

To download and unzip the application the following commands.

```sh
cd /u01/DAAP/
mkdir ai-chatbot-analytics
cd /u01/DAAP/daap-ai-chatbot-analytics
---- download zip package to here -----
unzip <file>
```

Create a virtual Python environment in a directory named venv, activate the virtualenv and install required dependencies using pip.

```sh
cd /u01/DAAP/daap-ai-chatbot-analytics/
virtualenv -p `which python3` venv
source venv/bin/activate
pip install -r requirements.txt
```

## Start the app

Dev - Prod Changes
```sh
/u01/DAAP/daap-ai-chatbot-analytics/frontend/settings.py

FLASK_SERVER_NAME = 'localhost:5004'
FLASK_SERVER_NAME = '172.28.9.75:5004'

MONGODB_DB = 
MONGODB_HOST = 
MONGODB_PORT = 
MONGODB_USERNAME = 
MONGODB_PASSWORD = 
```

Install packages
```sh
cd /u01/DAAP/daap-ai-chatbot-analytics/
python setup.py develop
```

Activate the virtual enviroment
Start the application with Gunicorn
```sh
source /u01/DAAP/venvChatbotAnalytics/bin/activate
cd /u01/DAAP/daap-ai-chatbot-analytics/frontend/

gunicorn \
--bind 0.0.0.0:5004 app:app \
--log-file /u01/DAAP/daap-ai-chatbot-analytics/daap-ai-chatbot-analytics.log \
--error-logfile /u01/DAAP/daap-ai-chatbot-analytics/error.log \
--access-logfile /u01/DAAP/daap-ai-chatbot-analytics/access.log  \
--log-level=info \
--timeout 7200 \
--workers 2 \
--threads 4 &
```

Install packages
```sh
cd /u01/DAAP/daap-ai-chatbot-analytics2/
python setup.py develop
```

Activate the virtual enviroment
Start the application with Gunicorn
```sh
source /u01/DAAP/venvChatbotAnalytics/bin/activate
cd /u01/DAAP/daap-ai-chatbot-analytics2/frontend/

gunicorn \
--bind 0.0.0.0:5005 app:app \
--log-file /u01/DAAP/daap-ai-chatbot-analytics2/daap-ai-chatbot-analytics.log \
--error-logfile /u01/DAAP/daap-ai-chatbot-analytics2/error.log \
--access-logfile /u01/DAAP/daap-ai-chatbot-analytics2/access.log  \
--log-level=info \
--timeout 7200 \
--workers 2 \
--threads 4 &
```

Kill the application 
```sh
ps -ef | grep "gunicorn"
kill -9 xxxx
```

## Usage

Swagger document helps you to use API, with examples and test screens.

http://localhost:5004/api/


## Development Tools

* [Python] - Programing language
* [SQLite] - SQL database engine
* [Scikit-learn] - Python ML library
* [Flask] - Python based web development microframework
* [Swagger] - API development framework
* [NLTK] - Language processing library
* [Zemberek] - Language processing tool
* [Gunicorn] - Python WSGI HTTP Server for UNIX


<br/>

######TECH 

   [Python]: <https://www.python.org/>
   [SQLite]: <https://www.sqlite.org/>
   [Scikit-learn]: <https://scikit-learn.org/>
   [Flask]: <http://flask.pocoo.org/>
   [Swagger]: <https://swagger.io/>
   [NLTK]: <https://www.nltk.org/>
   [Zemberek]: <http://zembereknlp.blogspot.com/>
   [Gunicorn]: <https://gunicorn.org/>
