#!/usr/bin/python3
from bs4 import BeautifulSoup
import requests
import sys

# r = requests.post('http://158.69.76.135/level1.php', data=votation)

success_votes = 0
error_cases = 0
user_id = 3014
number_print = 4096
url = "http://158.69.76.135/level1.php"

for i in range(0, number_print):
    cookies_page = requests.session()
    r = cookies_page.get(url)
#    print(r.cookies)

    soup = BeautifulSoup(r.text, "lxml")
    key_value = soup.find('form').find('input', {'name' : 'key'})['value']

    votation = {'id': user_id, 'holdthedoor': 'Submit', 'key': key_value}
    vote = cookies_page.post(url, data=votation)
#    print(vote.cookies)

    if vote.status_code == 200:
        success_votes +=1
    else:
        error_cases += 1

print("-------------------")
print("print success: {}".format(success_votes))
print("error_cases: {}".format(error_cases), file=sys.stderr)
print("-------------------")
if error_cases == 0:
    print("Success operation: 100% of {} votes".format(success_votes))
