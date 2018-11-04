#!/usr/bin/env python

import logging
import argparse
import math
import datetime
import re
import csv
import json
import time
import requests
from requests.exceptions import RequestException

from commons import DEFAULT_FILENAME
from request_handler import RequestHandler


def write_headers(filename, fields):
    """Write the headers of the CSV file."""
    with open(filename, 'w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fields,
                                restval='NA', extrasaction='ignore')
        writer.writeheader()


def write_rows(filename, fields, data):
    """Write the data as rows in the CSV file."""
    with open(filename, 'a') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fields,
                                restval='NA', extrasaction='ignore')
        for row in data:
            writer.writerow(row)


def visual_sleep(seconds):
    """Show some dots while sleeping."""
    logging.info("Waiting some seconds to avoid overload the server")
    for _ in range(seconds):
        time.sleep(1)
        logging.info(" . ")


def get_n_pages(data):
    """Return the number of pages to extract the offers."""
    n_offers = data['response']['numFound']
    n_pages = math.ceil(n_offers / 10.)
    logging.info(f'The total number of offers found is: {n_offers}')
    logging.info(f'The total number of pages will be: {n_pages}')
    return n_pages


def get_fields(docs):
    """Return the maximum number of fields to extract."""
    length_list = [len(doc) for doc in docs]
    max_value = max(length_list)
    max_index = length_list.index(max_value)
    fields = sorted(docs[max_index].keys())
    logging.info(f'The maximum number of fields found is: {max_value}, ' \
          f'in index: {max_index}')
    return fields


def show_total_time(n_page, wait_time):
    """Calculate the total amount of time that the process will last."""
    avg_time_to_get_page = n_page * 0.09  # Average time to download the web in ms
    total_seconds = (n_page * wait_time) + avg_time_to_get_page
    total_minutes = total_seconds / 60.0
    total_hours = total_minutes / 60.0
    logging.info(f"The process will last {total_minutes:.2g} minutes")
    logging.info(f"       ... That means {total_hours:.2g} hours")
    

def export_data_to_file(filename, wait_time, requestor, testing):
    """Extract the data from the source and save it to file."""
    logging.info(f'Starting to export data to file ...')
    
    # get the 10 first offers. This is the info in the 1st page.
    rows, start_at = (10, 0)
    data = requestor.get_data(rows, start_at)
    n_pages = get_n_pages(data)
    
    show_total_time(n_pages, wait_time)

    docs = data['response']['docs']
    fields = get_fields(docs)

    write_headers(filename, fields)
    write_rows(filename, fields, docs)
    visual_sleep(wait_time)
    
    # get the rest of the offers, shown in different pages.
    if testing:
        n_pages = 4

    for i in range(1, n_pages):        
        logging.info(f'Starting iteration: {i+1} of {n_pages}')
        start_at = i*10
        data = requestor.get_data(rows, start_at)
        docs = data['response']['docs']
        write_rows(filename, fields, docs)
        visual_sleep(wait_time)


def main():
    """Main function to extract job offers."""
    logging.basicConfig(format='%(asctime)s | %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p',
                        level=logging.INFO)

    parser = argparse.ArgumentParser(description='Extract job offers.')
    parser.add_argument('-f','--filename', type=str,
                        help=f'Filename where data will be saved. ' \
                             f'The date will be added at the end of it.\n' \
                             f'This argument is optional, the default value ' \
                             f'will be saved under the data directory with the '\
                             f'name: offers_XXXX-XX-XX.csv. Where XXXX-XX-XX '\
                             f'is the actual date.',
                        default=DEFAULT_FILENAME)
    parser.add_argument('-wt','--wait_time', type=int,
                        help=f'Time to wait between requests, used to prevent ' \
                             f'the overload of the server.\n' \
                             f'The default wait time is 5 seconds.',
                        default=5)
    parser.add_argument('-nd', '--number_of_days', type=int,
                        help=f"Set the number of days to collect data.",
                        default=None)
    parser.add_argument('-td', '--today', action="store_true",
                        help=f"Collect the data from today.")
    parser.add_argument('--testing', action="store_true",
                        help=f"Test with a limited number of pages.")
    args = parser.parse_args()

    # Get ready the different constants to be used.
    today_date = datetime.date.today()
    filename = f'../data/{args.filename}_{today_date}.csv'
    wait_time = args.wait_time

    requestor = RequestHandler()

    if args.today:
        logging.info(f"Only todays data: {today_date}")
        requestor.conf_query_todays_spanish_offers()
    
    elif args.number_of_days is not None:
        logging.info("Getting data from the last {args.number_of_days} days")
        requestor.conf_query_custom_days(args.number_of_days)
        filename = f'../data/{args.filename}_last_{args.number_of_days}_days.csv'
    
    else:
        logging.info("All the data")
        requestor.conf_query_all_spanish_offers()


    logging.info(f'Data will be saved in: {filename}')
    export_data_to_file(filename, wait_time,
                        requestor, args.testing)
    logging.info('Data extracted correctly.')


if __name__ == '__main__':
    main()