import configparser
import sys

if __name__ =="__main__":
    _new_prefix = sys.argv[1] if sys.argv[1].startswith('/') or sys.argv[1] == "" else f"/{sys.argv[1]}"
    config = configparser.ConfigParser()
    config.read('config.ini')

    config['WEBSITE']['prefix'] = _new_prefix


    with open('config.ini', 'w') as configfile:
        config.write(configfile)
