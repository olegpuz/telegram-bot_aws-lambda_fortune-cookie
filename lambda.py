import random
import csv
import json
from botocore.vendored import requests

csv_file_path='FortuneCookie.csv'
telegram_token='{YOUR_TOKEN}'
telegram_api_url="https://api.telegram.org/bot{}/".format(telegram_token)
secret='{GENERATE_GUID}'

def getAllFortunes():
    with open(csv_file_path, newline='\n', encoding='utf-8') as csvfile:
        return list(csv.reader(csvfile, delimiter='~'))

all_fortunes = getAllFortunes()

def send_message(text, chat_id):
    print('Sending text {}'.format(text))
    url = telegram_api_url + "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(text, chat_id)
    requests.get(url)
    
def lambda_handler(event, context):
    print('Incoming event:')
    request_body = json.loads(event['body'])
    print(json.dumps(request_body))

    if event['rawPath']!=secret:
        auth_error_message='Wrong secret {}'.format(event['rawPath'])
        print(auth_error_message)
        return {
            'statusCode': 200,
            'body': auth_error_message
        }
    
    chat_id = request_body['message']['chat']['id']
    #command=request_body['message']['text'].split()[0]
    
    rnd_fortune = random.choice(all_fortunes)[0]

    send_message(rnd_fortune, chat_id)

    return {
        'statusCode': 200,
        'body': rnd_fortune
    }