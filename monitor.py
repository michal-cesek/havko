import requests
import time
import hashlib
import os
from datetime import datetime
from bs4 import BeautifulSoup
from mailjet_rest import Client

URL = os.environ['URL_TO_CHECK']
# URL = "http://127.0.0.1:7648/"

WAIT = int(os.environ['WAIT'])
start = datetime.utcnow()

API_KEY = os.environ['MJ_APIKEY_PUBLIC']
API_SECRET = os.environ['MJ_APIKEY_PRIVATE']
RECEPIENT = os.environ['RECEPIENT']
mailjet = Client(auth=(API_KEY, API_SECRET), version='v3')
email = {
    'FromName': 'Havko script',
    'FromEmail': RECEPIENT,
    'Subject': 'Page {} has changed'.format(URL),
    'Text-Part': 'Hello, the page {} has changed.( scirpt started on {} )'.format(URL, start),
    'Recipients': [{'Email': RECEPIENT}]
}
headers = {
    'User-Agent': os.environ['USER_AGENT']
}


def get_hash():
    response = requests.get(URL, headers=headers)
    print('Sending request to {}'.format(URL))
    soup = BeautifulSoup(response.text.encode('utf-8'), "html.parser")
    # remove elemnt which changes with every request
    for div in soup.find_all("div", {'class': 'parallax-window'}):
        div.decompose()
    soup_str = str(soup).encode('utf-8')
    return hashlib.sha224(soup_str).hexdigest()


print('Starting script ...')
print('Recipeint of email notification: {}'.format(RECEPIENT))
initial_hash = get_hash()
print('Initial hash set.')

while True:

    print('Waiting {} seconds ... '.format(WAIT))
    time.sleep(WAIT)
    current_hash = get_hash()

    if current_hash == initial_hash:
        print('Hashes are same')
    else:
        print('Hashes are diffrent, sending email ...')
        initial_hash = current_hash
        mailjet.send.create(email)
        print('Email sent ({})'.format(datetime.utcnow()))
        break
