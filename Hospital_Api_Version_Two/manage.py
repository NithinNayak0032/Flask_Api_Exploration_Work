import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from models import users,hospitals
from app import app,db



#Instance of database migration
migrate = Migrate();
#Intialization Of Database
db.init_app(app)
#Migration Of database used within app
migrate.init_app(app,db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()