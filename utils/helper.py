import secrets
import requests
from sitaramsita import settings

def verify_mobile(mobile):
    success = True

    if not mobile.isdigit():
        success = False

    elif mobile.isdigit() and len(mobile) != 10:
        success = False

    elif mobile.isdigit() and len(mobile) == 10:
        defaulters = [i * 10 for i in '0123456789']
        if mobile in defaulters:
            success = False

    return success


def generate_otp(otp_len=6):
    sequenc_ls = [1,2,3,4,5,6,7,8,9,0]

    otp_char1 = [secrets.choice(sequenc_ls) for i in range(otp_len)]
    otp_char2 = [secrets.choice(sequenc_ls) for i in range(otp_len)]

    while sum(otp_char1) == sum(otp_char2):
        otp_char2 = [secrets.choice(sequenc_ls) for i in range(otp_len)]

    otp = "".join([str(i) for i in otp_char2])
    return otp


def send_otp(numbers, otp):
    success = False

    url = settings.FAST_SMS['URL']
    headers = {
        'authorization' : settings.FAST_SMS['AUTH_KEY'],
        'Content-Type'  : 'application/json'
    }
    json_data = {
        'route' : 'otp',
        'variables_values' : otp,
        'numbers' : numbers        # number1,number2,number3
    }

    try:
        response = requests.post(url, headers=headers, json=json_data)
    except Exception as exp:
        response = []


    if response and response.status_code == 200:
        success = True

    return success
