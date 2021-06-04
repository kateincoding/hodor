#!/usr/bin/python3
from bs4 import BeautifulSoup
import requests
import sys
from PIL import Image
import urllib
from operator import itemgetter
import pytesseract as tess

success_votes = 0
error_cases = 0
user_id = int(input("Please write your ID: "))
number_print = 100
url = "http://158.69.76.135/level3.php"
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
     AppleWebKit/537.36 (KHTML, like Gecko)\
     Chrome/91.0.4501.0 Safari/537.36 Edg/91.0.866.0',
    'Referer': url
}
cookies_page = requests.session()
cookies_page.headers.update(header)

for i in range(0, number_print):
    r = cookies_page.get(url, headers=header)

    soup = BeautifulSoup(r.text, "lxml")
    key_value = soup.find('form').find('input', {'name': 'key'})['value']
    
    captcha_url = "http://158.69.76.135/captcha.php"
    captcha_image = cookies_page.get(captcha_url)
    file = open("captcha_image.png", "wb")
    file.write(cookies_page.get(captcha_url, headers=header).content)
    # file.write(urllib.request.urlopen(captcha_url).read())
    # file.write(captcha_image.content)
    file.close()

    captcha_text = tess.image_to_string("captcha_image.png")[:4]
    print(".{}.".format(captcha_text))
    votation = {'id': user_id, 'holdthedoor': 'Submit', 'key': key_value, 'captcha': captcha_text}
    vote = cookies_page.post(url, data=votation)

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
