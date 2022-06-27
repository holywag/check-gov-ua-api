#!/usr/bin/env python3

import json, requests, argparse
from selenium import webdriver
from check_gov_ua import CheckGovUaApi

parser = argparse.ArgumentParser()
parser.add_argument('company')
parser.add_argument('receipt_id', nargs='+')
args = parser.parse_args()

with webdriver.Safari() as driver:
    client = CheckGovUaApi(driver)
    for receipt_id in args.receipt_id:
        recaptcha_token = client.get_recaptcha_token()
        download_url = client.request_download_link(args.company, receipt_id, recaptcha_token)
        with open(f'{receipt_id}.pdf', 'wb') as file:
            file.write(requests.get(download_url).content)
            print(file.name)
