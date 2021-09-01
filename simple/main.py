import re
import requests
from lib import utils, auth
from bs4 import BeautifulSoup as bS

s = requests.Session()
s.host = 'http://air.eu.ngrok.io'
#s.cron_key = 'fOD7znV7_s2Xn_iViz_07z9Hi6NJ01A5JVdHHNKwIpk'
s.cron_key = 'OHMqnu__Xiztjmy33VAapUPRZ9Bx5nu2Dvh5jWJM8bQ'
auth.drupal_login(s, 'gRun')
#auth.drupal_login(s)
url = '/my-auctions/new'
r = s.get(f'{s.host}{url}')
doc = bS(r.content, 'lxml')
form_html_id = "air-auction-page-node-form"
form_ids = utils.get_form_ids(doc, form_html_id)
inputs = doc.find_all('input')
values = {}
for i in inputs:
    if 'name' in i.attrs.keys() and 'value' in i.attrs.keys():
        values[i.attrs['name']] = i.attrs['value']
values['title'] = 'Test auction'
r = s.post(f'{s.host}{url}', values)
if r.status_code == 200:
    doc = bS(r.content, 'lxml')
    utils.print_page_result(r, s.username)

auth.drupal_logout(s)
