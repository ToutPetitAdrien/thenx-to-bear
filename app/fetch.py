from os import getenv
import requests
from bs4 import BeautifulSoup
from loguru import logger

def create_logged_session(session: requests.Session):
    html_doc = session.get('https://thenx.com/sign_in')
    soup = BeautifulSoup(html_doc.text, 'html.parser')

    data = {
        'authenticity_token': soup.find('input').attrs["value"],
        'session[email]': getenv('THENX_EMAIL'),
        'session[password]': getenv('THENX_PASSWORD'),
        'commit': 'Login',
    }

    session.post("https://thenx.com/session", data=data)


def get_dom_page(url: str) -> str:
    with requests.Session() as s:
        create_logged_session(s)
        response = s.get(url)
        logger.info(response)
        logger.info(response.text)
        return response.text