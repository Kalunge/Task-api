from flask import Flask
from flask_restx import Resource, Api, fields
from flask_sqlalchemy import SQLAlchemy
from Configs.DbConfig import DevelopmentConfig
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
db = SQLAlchemy(app)
api = Api(app, title='An Api to track a to do list')
ma = Marshmallow(app)
jwt = JWTManager(app)



from Models.taskModel import *
from Models.userModel import *

@app.before_first_request
def create_tables():
    db.create_all()


from Resources.taskResource import *
from Resources.userResource import *
from Resources.registerLogin import *





if __name__ == "__main__":
    app.run(debug=True)