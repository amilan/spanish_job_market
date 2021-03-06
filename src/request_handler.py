#!/usr/bin/env python

import re
import json
import logging
import datetime

import requests
from requests.exceptions import RequestException

from commons import BASE_URL, HEADERS


class RequestHandler(object):
    """Class to be used to manage the different requests to obtain data."""

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
        self.get_today_data = False
        self.get_custom_days = False
        self.n_days = 0

    def conf_query_all_offers(self):
        """Configure the parameters to get all the available data."""
        self.params['fq'] = "speStateId:1 OR speStateId:4"    

    def conf_query_all_spanish_offers(self):
        """Configure the parameters to get all the spanish offers."""
        self.params['fq'] = ["paisF: \"ESPAÑA\"",
                             "speStateId:1 OR speStateId:4"]

    def conf_query_todays_spanish_offers(self):
        """Configure the query to get the spanish offers added today."""
        self.get_today_data = True

    def conf_query_custom_days(self, number_of_days):
        """Configure the query to get data from custom days."""
        self.get_today_data = False
        self.get_custom_days = True
        self.n_days = number_of_days

    def get_todays_spanish_offers(self):
        """Get the spanish offers added today.
        
        It's done using an URL template instead of the self.params due to 
        incompatibilities when trying to make the request that forced me
        to implemented it in this way.
        """

        d_today = datetime.date.today()
        date_to_request = f'{d_today+ datetime.timedelta(days=-1)}T00:00:00Z+'\
                          f'{d_today + datetime.timedelta(days=0)}T00:00:00Z'
        
        rows = self.params['rows']
        start = self.params['start']
        URL = f"https://empleate.gob.es/empleate/open/solrService/select?q.op="\
              f"AND&rows={rows}&start={start}&&facet=true&facet.field=paisF"\
              f"&facet.field=provinciaF"\
              f"&facet.field=categoriaF&facet.field=subcategoriaF&facet.field"\
              f"=origen&facet.field=tipoContratoN&facet.field=noMeInteresa"\
              f"&facet.field=educacionF&facet.limit=7&facet.mincount=1&"\
              f"f.topics.facet.limit=50&json.nl=map&fq=fechaCreacionPortal"\
              f":[{date_to_request}]&fq=paisF:\"ESPAÑA\"&fq=speStateId:"\
              f"1%20OR%20speStateId:4&fl=*,%20score&q=*&wt=json&json.wrf="\
              f"jQuery110203397243895472001_1541105095567&_=1541105095572"

        return self.get_web(URL, use_params=False)

    def get_last_days_spanish_offers(self):
        """Get the spanish offers published in the last N days.
        
        It's done using an URL template instead of the self.params due to 
        incompatibilities when trying to make the request that forced me
        to implemented it in this way.
        """

        d_today = datetime.date.today()
        date_to_request = f'{d_today + datetime.timedelta(days=-self.n_days)}T00:00:00Z+'\
                          f'{d_today + datetime.timedelta(days=0)}T00:00:00Z'
        
        rows = self.params['rows']
        start = self.params['start']
        URL = f"https://empleate.gob.es/empleate/open/solrService/select?q.op="\
              f"AND&rows={rows}&start={start}&&facet=true&facet.field=paisF"\
              f"&facet.field=provinciaF"\
              f"&facet.field=categoriaF&facet.field=subcategoriaF&facet.field"\
              f"=origen&facet.field=tipoContratoN&facet.field=noMeInteresa"\
              f"&facet.field=educacionF&facet.limit=7&facet.mincount=1&"\
              f"f.topics.facet.limit=50&json.nl=map&fq=fechaCreacionPortal"\
              f":[{date_to_request}]&fq=paisF:\"ESPAÑA\"&fq=speStateId:"\
              f"1%20OR%20speStateId:4&fl=*,%20score&q=*&wt=json&json.wrf="\
              f"jQuery110203397243895472001_1541105095567&_=1541105095572"

        return self.get_web(URL, use_params=False)


    def get_web(self, url=BASE_URL, use_params=True):
        """Returns the downloaded web page where to extract the info."""
        try:
            if use_params:
                page = requests.get(url, headers=HEADERS, params=self.params)
            else:
                page = requests.get(url, headers=HEADERS)

        except RequestException as e:
            logging.error(f'Error downloading the web. Error: {e}')
            page = None
        return page

    def extract_json(self, page_text):
        """Extract the data from the request into a JSON object.
        
        As the data is coming in a form of JSONP, the first part needs to be
        extracted. Therefore, a regular expression is used to remove that 
        part and get only the json data.
        """
        p = re.compile('jQuery\w*\(')
        data = p.sub("", page_text)
        data = json.loads(data[:-1])
        return data

    def get_data(self, rows=10, start=0):
        """Get data rows starting from an specific start value."""
        self.params['rows'] = rows
        self.params['start'] = start

        if self.get_today_data:
            page = self.get_todays_spanish_offers()
        elif self.get_custom_days:
            page = self.get_last_days_spanish_offers()
        else:
            page = self.get_web()
        data = self.extract_json(page.text)
        return data

def main():
    # This code was used for testing.
    requestor = RequestHandler()
    # requestor.conf_query_all_offers()
    # requestor.conf_query_all_spanish_offers()
    # requestor.conf_query_todays_spanish_offers()
    # requestor.conf_query_last_two_weeks_spanish_offers()
    requestor.conf_query_custom_days(3)
    data = requestor.get_data()
    # print(page.url)
    # print(page.text)
    print(len(data['response']['docs']))

if __name__ == '__main__':
    main()

    # This code was used for testing.
    # page = get_web(BASE_URL)
    # data = extract_json(page.text)
    # print(len(data['response']['docs']))

    # page = requests.get(BASE_URL, headers=HEADERS, params=params)
    # print(page.url)
