from lib import utils, auth
from locust import HttpUser, task
from locust.env import Environment
from bs4 import BeautifulSoup as bS
from gevent import hub


class MyUser(HttpUser):
    host = 'http://air.localhost:8000'
    cron_key = 'qVOmeVcoyQa8jLOHBjQEb6CaNKDI9In0oyDk4ScmeuI'
    uid = 0
    username = 'Anonymous'

    def on_start(self):
        auth.drupal_login(self)

    def on_stop(self):
        auth.drupal_logout(self)

    @task
    def create_auction(self):
        url = '/my-auctions/new'
        page = self.client.get(url)
        doc = bS(page.content, 'lxml')
        form_ids = utils.get_form_ids(doc, 'air-node-form')
        r = self.client.post(url, {
            'form_id': form_ids['form_id'],
            'form_build_id': form_ids['form_build_id'],
            'form_token': form_ids['form_token'],
            'title': 'Test auction'
        })
        utils.print_page_result(r, self.username)


if __name__ == '__main__':
    MyUser(Environment()).run()
