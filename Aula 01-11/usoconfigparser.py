import configparser


config = configparser.ConfigParser()

config['DEFAULT'] = {
    'database' : 'localhost',
    'user' : 'root',
    'password' : 'pass'
}

with open('config.ini', 'w') as configfile:
    config.write(configfile)

database = config['DEFAULT'].get('database')
user = config['DEFAULT'].get('user')
password = config['DEFAULT'].get('password')

print(database)
print(user)
print(password)