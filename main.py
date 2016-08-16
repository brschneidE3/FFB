__author__ = 'brsch'

# import requests
# import yql
# from yql.storage import FileTokenStore
#
# # Fill in your details here to be posted to the login form.
# # payload = {
# #     'inUserName': 'donotletthisemailaddressbeused@yahoo.com',
# #     'inUserPass': 'NewHussey23'
# # }
# #
# # # Use 'with' to ensure the session context is closed after use.
# # with requests.Session() as s:
# #     p = s.post('https://login.yahoo.com/config/login?.src=spt&.intl=us&.done=http%3A%2F%2Ffootball.fantasysports.yahoo.com%2Ff1%2F427623%2Fplayers%3F.scrumb%3D0&specId=usernameRegWithName', data=payload)
# #     # print the html returned or something more intelligent to see if it's a successful login page.
# #     print p.text
# #     exit()
# #
# #     # An authorised request.
# #     r = s.get('http://football.fantasysports.yahoo.com/f1/427623/players')
# #     print r.text
#
# payload = {'inUserName': 'donotletthisemailaddressbeused@yahoo.com', 'inUserPass': 'NewHussey23'}
# url = 'http://football.fantasysports.yahoo.com/f1/427623/players'
# p = requests.post(url, data=payload)
# print p.text

import myql
from yahoo_oauth import OAuth1
oauth = OAuth1(None, None, from_file='credentials.json')
yql = myql.MYQL(format='xml', oauth=oauth)
'http://fantasysports.yahooapis.com/fantasy/v2/game/'
# response = yql.select('http://fantasysports.yahooapis.com/fantasy/v2/game/nfl')
# print response.__dict__