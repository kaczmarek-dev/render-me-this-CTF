from website import create_app
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')

app = create_app(config)

if __name__ == '__main__':
    app.run(debug=False, host=config['WEBSITE']['serverIP'])