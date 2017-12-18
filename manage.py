import unittest
from recipe.auth.views import api
from recipe.categories.views import api_category
from recipe import app, db
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from recipe.config import app_config

conf = app_config['development']
#app = create_app("development")

manage = Manager(app)
migrate = Migrate(app, db)

manage.add_command('db', MigrateCommand)

@manage.command
def create_db(default_data = True, sample_data = False):
    """create the database"""
    db.drop_all()
    db.create_all()
    #db.session.commit()

@manage.command
def test():
    """Runs the tests without code coverage."""
    tests = unittest.TestLoader().discover('/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

@manage.command
def drop_database():
     db.drop_all()

if __name__ == '__main__':
    manage.run()

