import random
import string

from twilio.rest import Client
import os


def genret_order_id(length=10):
    key = ''
    for i in range(length):
        key += random.choice(string.ascii_lowercase + string.digits)
    return key


account_sid = 'AC9aa0fa32a744f5ca33458e15ae67fff6'
auth_token = '76020542d1c3cfbdd04b891515c4bfc7'
client = Client(account_sid, auth_token)


def send_sms(user_code, phone_number):
    message = client.messages.create(body=f'Hi ! Your Otp is- {user_code}',
                                     from_='+19706151513',
                                     to=f'+91{phone_number}')

    print(message.sid)


def send_link(user_link, phone_number):
    message = client.messages.create(body=f'Hi ! Your Otp is- {user_link}',
                                     from_='+19706151513',
                                     to=f'+91{phone_number}')

    print(message.sid)
