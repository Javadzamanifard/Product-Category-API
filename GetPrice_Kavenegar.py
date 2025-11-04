import requests
from environs import Env

env = Env()
env.read_env()

NORMAL_PRICE = 120000
API_KEY = env.str('API_KEY')
KAVENEGAR_API_KEY = env.str('KAVENEGAR_API_KEY')
PHONE_NUMBER = env.str('PHONE_NUMBER')
SENDER = env.str('PHONE_SENDER')
URL = f'http://api.navasan.tech/latest/?api_key={API_KEY}'

def inform_javad(price):
    URL = f'https://api.kavenegar.com/v1/{KAVENEGAR_API_KEY}/sms/send.json'
    payload = {
        'receptor':PHONE_NUMBER,
        'sender' :SENDER,
        'message' : f'الان وقتشه دلار رو بخری قیمتش :{price}'
    }
    response = requests.post(URL, data=payload)
    print(response.json())

response = requests.get(url=URL)
price = (int(response.json()['usd_sell']['value'])) / 10
print(f'Price is:{price}')
if price < NORMAL_PRICE:
    inform_javad(price)