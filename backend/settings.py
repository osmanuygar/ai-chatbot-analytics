# Flask settings
SERVER_NAME = 'localhost:5004'
#SERVER_NAME = '172.28.9.75:5004'
SCORE_URL = 'http://localhost:8081/api/v1'
FLASK_DEBUG = True  # Do not use debug mode in production


# Flask-Restplus settings
SWAGGER_UI_DOC_EXPANSION = 'list'
RESTPLUS_VALIDATE = True
RESTPLUS_MASK_SWAGGER = False
ERROR_404_HELP = False
DEBUG = False

# MongoDB settings
MONGODB_DB = "iky-ai"
MONGODB_HOST = "10.0.0.82"
MONGODB_PORT = 27017
MONGODB_USERNAME = None
MONGODB_PASSWORD = None
MONGODB_URI = "mongodb://10.0.0.82:27017 / iky-ai"
