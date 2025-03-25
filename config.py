import configparser
import uuid

if __name__ =="__main__":
    config = configparser.ConfigParser()
    config['WEBSITE'] = {
        'serverIP': '0.0.0.0',
        'serverPort': '5000',
        'secretKey': str(uuid.uuid4())
        }
    config['ADMIN'] = {
        'username': 'admin',
        'password': str(uuid.uuid4())
    }
    config['DATABASE'] = {
        'location': 'database',
        'name': 'database.db' 
    }

    with open('config.ini', 'w') as configfile:
        config.write(configfile)
