from app import create_app
import os
from flask_script import Manager
from app import db

app = create_app(os.environ['CONFIG_TYPE'])

@app.route('/debug-sentry')
def trigger_error():
    division_by_zero = 1 / 0

manager = Manager(app)


@manager.command
def run():
    """Like a 'runserver' command but shorter, lol."""
    app.run(host="0.0.0.0")


@manager.command
def run_tests():
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command
def debug_fix():
    """
    I have trouble with hitting breakpoints in lask-RESTful class methods.
    This method help me.
    """
    app.config['DEBUG'] = False
    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.run(debug=False)


@manager.command
def db_init():
    db.create_all()


if __name__ == '__main__':
    manager.run()
