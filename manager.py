from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from like_zhihu import app
from exts import db
from models import User, Question, Comment

manager = Manager(app)
# 使用Migrate绑定app和db
migrate = Migrate(app, db)
# 添加迁移脚本的命令到manager中
manager.add_command('db', MigrateCommand)

# 使用python manager.py db init初始化
# python manager.py db migrate
# python manager.py db upgrade
if __name__ == '__main__':
    manager.run()
