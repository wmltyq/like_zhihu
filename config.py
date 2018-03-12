import os

DEBUG = True
SECRET_KEY = os.urandom(24)

HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'like_zhihu'
USERNAME = 'root'
# 这里的数据库密码改成自己的
PASSWORD = 'xxxx'
SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
# 关闭跟踪修改
SQLALCHEMY_TRACK_MODIFICATIONS = False
