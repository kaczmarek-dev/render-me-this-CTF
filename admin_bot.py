from bot.utils import get_session_cookie, visit_with_cookies_time_limit
from time import sleep
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from website.models import Report
from configparser import ConfigParser

if __name__ == "__main__":
    engine = create_engine('sqlite:///instance/database.db')
    Session = sessionmaker(bind=engine)
    session = Session()
    config = ConfigParser()
    config.read('config.ini')
    
    while(1):
        reports = session.query(Report).filter_by(verified=False)
        for report in reports:
            _session_cookie = get_session_cookie(f"{config['WEBSITE']['serverIP']}:{config['WEBSITE']['serverPort']}", {config['ADMIN']['username']}, {config['ADMIN']['password']})
            visit_with_cookies_time_limit(
                max_time_seconds=2,
                page_to_load=f"http://{config['WEBSITE']['serverIP']}:{config['WEBSITE']['serverPort']}/static/images/{report.filename}", 
                session_cookie=_session_cookie
            )
        reports.update({"verified": True})
        session.commit()  
        sleep(10)

    