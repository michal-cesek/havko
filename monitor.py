import requests
import time
import hashlib
import sys
import os
from datetime import datetime
from bs4 import BeautifulSoup
from mailjet_rest import Client

URL = os.environ['HAVKO_URL_TO_CHECK']
# URL = "http://127.0.0.1:7648/"
WAIT = int(os.environ['HAVKO_WAIT'])
API_KEY = os.environ['MJ_APIKEY_PUBLIC']
API_SECRET = os.environ['MJ_APIKEY_PRIVATE']
RECEPIENT = os.environ['HAVKO_RECEPIENT']
USER_AGENT = os.environ['HAVKO_USER_AGENT']

mailjet = Client(auth=(API_KEY, API_SECRET), version='v3')
email = {
    'FromName': 'Havko script',
    'FromEmail': RECEPIENT,
    'Subject': 'Page {} has changed'.format(URL),
    'Text-Part': 'Hello, the page {} has changed.( scirpt started on {} )'.format(URL, datetime.utcnow()),
    'Recipients': [{'Email': RECEPIENT}]
}
test_email = email
test_email['Subject'] = 'Just testing if script can send email.'

headers = {
    'User-Agent': USER_AGENT
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
print('Recipeint of email notification: {}. Sending test email ...'.format(RECEPIENT))
res = mailjet.send.create(test_email)
if res.status_code == 200:
    print('Test email sent successfully ({})'.format(datetime.utcnow()))
else:
    print('Email/email service is not set correctly')
    sys.exit()

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
        res = mailjet.send.create(email)
        if res.status_code == 200:
            print('Notification email sent successfully ({})'.format(datetime.utcnow()))
        else:
            print('Notification email was not sent successfully ({})'.format(datetime.utcnow()))

        break

