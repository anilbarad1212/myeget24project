from operator import ge
import random
import string

from twilio.rest import Client
import os


def genret_order_id(length=12):
    key = ''
    for i in range(length):
        key += random.choice(string.digits)
    return 'Eget24-' + key


account_sid = 'AC9aa0fa32a744f5ca33458e15ae67fff6'
auth_token = '76020542d1c3cfbdd04b891515c4bfc7'
client = Client(account_sid, auth_token)


def send_sms(user_code, phone_number):
    message = client.messages.create(body=f'Hi ! Your Otp is- {user_code}',
                                     from_='+19706151513',
                                     to=f'+91{phone_number}')

    print(message.sid)


def send_payment_info(user_link, phone_number):
    message = client.messages.create(body=f'Hi ! Your Otp is- {user_link}',
                                     from_='+19706151513',
                                     to=f'+91{phone_number}')

    print(message.sid)


def sent_order_confirmation_mesaage(phone_number, my_data, total_amount,
                                    order_id, txn_id, txn_date, txn_status,
                                    bank_txn_id):
    message = client.messages.create(
        body=
        f'Congratulations ! Your Order {my_data} Has Been Plced,Total Mount : {total_amount},order-id:{order_id},transaction-id : {txn_id} , transaction-date {txn_date},transaction-status {txn_status},Bank-transaction-id{bank_txn_id}',
        from_='+19706151513',
        to=f'+91{phone_number}')

    print(message.sid, 'THIS IS MESSAGE.SID')


def sent_dileverd_message(user, phone_number, product, quantity, total_price,
                          delivery_date):

    # message = client.messages.create(body=f'Hi ! Your Otp is- {user_link}',
    #                                  from_='+19706151513',
    #                                  to=f'+91{phone_number}')

    print(user, phone_number, product, quantity, total_price, delivery_date)
