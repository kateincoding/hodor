#!/usr/bin/python3
from bs4 import BeautifulSoup
import requests
import sys
from PIL import Image
import urllib
from operator import itemgetter
import pytesseract as tess
from fp.fp import FreeProxy

success_votes = 0
error_cases = 0
user_id = int(input("Please write your ID: "))
number_print = 98
url = "http://158.69.76.135/level4.php"
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
     AppleWebKit/537.36 (KHTML, like Gecko)\
     Chrome/91.0.4501.0 Safari/537.36 Edg/91.0.866.0',
    'Referer': url
}


for i in range(0, number_print):
    flag = 0
    try:
        # Create the proxy
        proxy_content = FreeProxy(country_id=['US', 'CA', 'FR', 'MX', 'IR'], timeout=5, rand=True).get()
        print("IP + port = '{}'".format(proxy_content))
        list_proxy_content = proxy_content.split(':')
        proxy_content = str(list_proxy_content[0]) + ':' + str(list_proxy_content[1])
        proxy = {"http": proxy_content}
        flag = 1
        print("Sending = '{}'".format(proxy))
    except Exception as error:
        print("Error: ", error)

    if flag == 1:
        try:
            # Create the session
            # print("Receiving '{}'".format(proxy_content))
            print("Receiving '{}'".format(proxy))
            cookies_page = requests.session()
            cookies_page.headers.update(header)

            # Obtein the key
            r = cookies_page.get(url, headers=header, proxies=proxy, timeout=5)
            soup = BeautifulSoup(r.text, "lxml")
            key_value = soup.find('form').find('input', {'name': 'key'})['value']
            # Create the data and send it
            votation = {'id': user_id, 'holdthedoor': 'Submit', 'key': key_value}
            vote = cookies_page.post(url, headers=header, data=votation, proxies=proxy, timeout=5)

            if vote.status_code == 200:
                success_votes += 1
                print("Success: ", success_votes)
                print("Total success cases until now: {}".format(i))
        except Exception as error:
            print("Error: ", error)
            error_cases += 1
            i = i - 1

print("-------------------")
print("print success: {}".format(success_votes))
print("error_cases: {}".format(error_cases), file=sys.stderr)
print("-------------------")
if error_cases == 0:
    print("Success operation: 100% of {} votes".format(success_votes))
