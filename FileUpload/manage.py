# -*- coding: utf-8 -*-
from app import create_app, db
from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand

app = create_app('config')
manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)
manager.add_command("runserver", Server(host='0.0.0.0', port=4545, use_debugger=True))

if __name__ == '__main__':
    manager.run()
