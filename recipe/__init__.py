import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
    
app = Flask(__name__)
app.config.from_object("recipe.config.DevelopmentConfig")
db = SQLAlchemy(app)

if __name__ == "__main__":
    app.run()
