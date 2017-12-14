from views import app, db
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from instance.config import app_config

conf = app_config['development']
#app = create_app("development")

manage = Manager(app)
migrate = Migrate(app, db)

manage.add_command('db', MigrateCommand)

@manage.command
def create_db(default_data = True, sample_data = False):
    db.drop_all()
    db.create_all()
    #db.session.commit()

@manage.command
def drop_database():
     db.drop_all()

if __name__ == '__main__':
    manage.run()

