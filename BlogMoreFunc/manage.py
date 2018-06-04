# -*- coding: utf-8 -*-
from app import create_app, db
from flask_script import Manager, Server, Shell
from flask_migrate import Migrate, MigrateCommand
from app.models import User, Role, Follow, Permission, Post, Comment


app = create_app('development')
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
	return dict(app=app, db=db, User=User, Role=Role, Follow=Follow, Permission=Permission, Post=Post, Comment=Comment)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)
manager.add_command("runserver", Server(host='0.0.0.0', port=5000, use_debugger=True))

if __name__ == '__main__':
    manager.run()