import os
import click
from flask_migrate import Migrate,MigrateCommand
from app import create_app, db
from flask_script import Manager,Shell
from app.models import User, Role,Server

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager=Manager(app)
migrate = Migrate(app,db)

#u=User(email='1639643261@qq.com',username='john',phone='A2783D892CB3E7F5FCACD6DD0BC24695',password='FAD19AA23C7259D28F7A8EA6D36CF6C1')

@app.shell_context_processor

def make_shell_context():
    return dict(db=db, User=User, Role=Role, Permission=Permission,Server=Server)


manager.add_command('db',MigrateCommand)
@app.cli.command()
@click.argument('test_names', nargs=-1)
def test(test_names):
    """Run the unit tests."""
    import unittest
    if test_names:
        tests = unittest.TestLoader().loadTestsFromNames(test_names)
    else:
        tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

if __name__=='__main__':
  manager.run()



