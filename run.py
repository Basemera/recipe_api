# #run.py
# #from flask import Flask
# import os
# from app.app import api, db, app
# from app.views import AddUser
# from app.app import create_app
# from instance.config import app_config

# #config_name = 'development'
# #app = create_app(config_name)
# #app = Flask(__name__)
# #config_name = os.getenv('APP_SETTINGS') # config_name = "development"
# #app = create_app(config_name)

# api.add_resource(AddUser, '/user') # , endpoint = "add_user"
# if __name__ == '__main__':
#     app.run(debug=True)