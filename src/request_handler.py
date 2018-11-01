#!/usr/bin/env python

import re
import json
import logging
import datetime

import requests
from requests.exceptions import RequestException

from commons import BASE_URL, HEADERS


class RequestHandler(object):
    """Class to be used for the requests to obtain data."""

    def __init__(self, params=None):
        """Class constructor were we initialize the parameters to be used."""
        if params is not None:
            self.params = params
        else:
            self.params = {"q.op":"AND",
                           "rows":10,
                           "start":0,
                           "facet":"true",
                           "facet.field":[
                               "paisF",
                               "provinciaF",
                               "categoriaF",
                               "subcategoriaF",
                               "origen",
                               "tipoContratoN",
                               "noMeInteresa",
                               "educacionF"
                           ],
                           "facet.limit":7,
                           "facet.mincount":1,
                           "f.topics.facet.limit":50,
                           "json.nl":"map",
                           "fq":"speStateId:1 OR speStateId:4",
                           "fl":"*, score",
                           "q":"*",
                           "wt":"json",
                           "json.wrf":"jQuery110206334639521193013_1540412324942"
                           }

    def set_query_all_offers(self):
        """Get all the available data."""
        self.params['fq'] = "speStateId:1 OR speStateId:4"    

    def set_query_all_spanish_offers(self):
        """Get all the available data."""
        self.params['fq'] = ["paisF: \"ESPAÑA\"",
                             "speStateId:1 OR speStateId:4"]

    def set_query_todays_spanish_offers(self):
        """Get the data added today."""

        d_today = datetime.date.today()
        date_to_request = f'{d_today}T00:00:00Z+'\
                          f'{d_today + datetime.timedelta(days=1)}T00:00:00Z'
        
        # TODO: Find why this doesn't work.
        print(date_to_request)
        print(f"fechaCreacionPortal: [{date_to_request}]")
        self.params['fq'] = ["paisF:\"ESPAÑA\"",
                            #  f"fechaCreacionPortal:[{date_to_request}]",
                             "speStateId:1 OR speStateId:4",
                             "fechaCreacionPortal:[2018-11-01T00:00:00Z+2018-11-02T00:00:00Z]",
                             ]
        # self.params['fq'] = "paisF:\"ESPAÑA\"&fq=fechaCreacionPortal:[2018-11-01T00:00:00Z+2018-11-02T00:00:00Z]&fq=speStateId:1 OR speStateId:4".decode("iso-8859-1")

    def set_query_last_two_weeks_spanish_offers(self):
        d_today = datetime.date.today()
        date_to_request = f'{d_today}T00:00:00Z+'\
                          f'{d_today + datetime.timedelta(days=-14)}T00:00:00Z'
        
        # TODO: Find why this doesn't work.
        self.params['fq'] = ["paisF: \"ESPAÑA\"",
                             f"fechaCreacionPortal: {date_to_request}",
                             "speStateId:1 OR speStateId:4"]

    def get_web(self):
        """Method to download the web page where to extract the info."""
        try:
            page = requests.get(BASE_URL, headers=HEADERS, params=self.params)
        except RequestException as e:
            logging.error(f'Error downloading the web. Error: {e}')
            page = None
        return page

    def extract_json(self, page_text):
        """Extract the data from the request into a JSON object."""
        p = re.compile('jQuery\w*\(')
        # jQuery\w*,_:\w*\(
        data = p.sub("", page_text)
        data = json.loads(data[:-1])
        return data

    def get_data(self, rows=10, start=0):
        """Get data rows starting from an specific start value."""
        self.params['rows'] = rows
        self.params['start'] = start

        page = self.get_web()
        data = self.extract_json(page.text)
        return data

def main():
    requestor = RequestHandler()
    # requestor.set_query_all_offers()
    # requestor.set_query_all_spanish_offers()
    requestor.set_query_todays_spanish_offers()
    # requestor.set_query_last_two_weeks_spanish_offers()
    page = requestor.get_web()
    print(page.url)
    print(page.text)

if __name__ == '__main__':
    main()

    # page = get_web(BASE_URL)
    # data = extract_json(page.text)
    # print(len(data['response']['docs']))

    # page = requests.get(BASE_URL, headers=HEADERS, params=params)
    # print(page.url)
