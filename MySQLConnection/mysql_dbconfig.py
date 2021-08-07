# from configparser import ConfigParser
#
#
# def read_db_config(filename='config.ini', section='mysql'):
#     """
#     Read database config file and returns a dictionary object
#
#     filename: name of the config file
#     section: section of database config
#     """
#     # create parser and read ini config file
#     parser = ConfigParser()
#     parser.read(filename)
#
#     # get section
#     db = {}
#     if parser.has_section(section):
#         items = parser.items(section)
#         for item in items:
#             db[item[0]] = item[1]
#     else:
#         raise Exception('{0} not found in the {1} file'.format(section, filename))
#
#     return db
from app import app
from flaskext.mysql import MySQL

MySQL = MySQL()
app.config['DATABASE_USER'] = 'root'
app.config['DATABASE_PASS'] = 'D@jma!2#'
app.config['DATABASE_DB'] = 'reservation_system'
app.config['DATABASE_HOST'] = 'localhost'
MySQL.init_app(app)
