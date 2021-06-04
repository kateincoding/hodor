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
number_print = 10
url = "http://158.69.76.135/level5.php"
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
     AppleWebKit/537.36 (KHTML, like Gecko)\
     Chrome/91.0.4501.0 Safari/537.36 Edg/91.0.866.0',
    'Referer': url
}
cookies_page = requests.session()
cookies_page.headers.update(header)

for i in range(0, number_print):
    # cookies_page = requests.session()
    # cookies_page.headers.update(header)
    r = cookies_page.get(url)

    soup = BeautifulSoup(r.text, "lxml")
    key_value = soup.find('form').find('input', {'name': 'key'})['value']
    
    captcha_url = "http://158.69.76.135/tim.php"
    captcha_image = cookies_page.get(captcha_url)
    file = open("captcha_image.png", "wb")
    file.write(cookies_page.get(captcha_url).content)
    # file.write(urllib.request.urlopen(captcha_url).read())
    # file.write(captcha_image.content)
    file.close()

    # convert captcha_image.png -gaussian-blur 0 -threshold 25% captcha_image_2.png

    im = Image.open("captcha_image.png")
    im = im.convert("P")
    his = im.histogram()
    im2 = Image.new("P", im.size, 255)

    values = {}

    for i in range(256):
        values[i] = his[i]
    for j,k in sorted(values.items(), key=itemgetter(1), reverse=True)[:10]:
        print (j, k)

    temp = {}

    for x in range(im.size[1]):
        for y in range(im.size[0]):
            pix = im.getpixel((y,x))
            temp[pix] = pix
            if pix < 139 and pix > 96:
                im2.putpixel((y,x),pix)

    im2.save("output.gif")
    im.close()
    
    captcha_text = tess.image_to_string("captcha_image.gif")[:4]
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
