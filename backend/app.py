import logging.config
import os

from flask import Flask, Blueprint
from backend.api.rest import api
from backend.api.chatlog.chatlogs import ns as chatlogs_namespaces
import json
from bson.objectid import ObjectId
import datetime
from flask_cors import CORS

# from app.db.model.dataset import db

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime.datetime):
            return str(o)
        return json.JSONEncoder.default(self, o)


app = Flask(__name__)
CORS(app)
logging_conf_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '../logging.conf'))
logging.config.fileConfig(logging_conf_path)
log = logging.getLogger(__name__)
app.config.from_object('settings')
#app.config['SERVER_NAME'] = settings.FLASK_SERVER_NAME
#app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
#app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VALIDATE
#app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
#app.config['ERROR_404_HELP'] = settings.RESTPLUS_ERROR_404_HELP
#app.config['DEBUG'] = settings.DEBUG

blueprint = Blueprint('api', __name__, url_prefix='/api')
api.init_app(blueprint)
api.add_namespace(chatlogs_namespaces)
app.register_blueprint(blueprint)
# db.init_app(app)
app.json_encoder = JSONEncoder
print('>>>>> Configured Application <<<<<')


def main():
    log.info('>>>>> Starting development server at http://{}/api/ <<<<<'.format(app.config['SERVER_NAME']))
    app.run(debug=app.config['FLASK_DEBUG'])


if __name__ != "__main__":
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

if __name__ == "__main__":
    main()


