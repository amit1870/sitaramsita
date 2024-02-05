import secrets
import requests

from datetime import date
from pathlib import Path

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


def process_form_data(form_data):
    qty_with_ids = {}

    for key, value in form_data.items():
        if key.startswith('ord_qty_'):
            product_id = int(key.split('ord_qty_')[1])
            try:
                qty_value = float(value)
            except:
                qty_value = 0

            qty_with_ids[product_id] = qty_value


    return qty_with_ids


def today_date():
    return date.today()


def handle_uploaded_file(f, rename='0'):
    success = True

    rename = f"{rename}"
    FILE_PATH = f"{settings.MEDIA_ROOT}/{rename}"

    delete_file(FILE_PATH)
    
    try:    
        with open(FILE_PATH, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
    except (Exception, FileNotFoundError):
        success = False

    return success

def delete_file(file_path):
    try:
        Path.unlink(Path(file_path), missing_ok=True)
    except Exception:
        pass



def read_text_file(file_path):
    data = []

    try:    
        with open(file_path) as f:
            data = f.readlines()
    except (Exception, FileNotFoundError):
        pass

    return data

def data_from_file(filename):
    FILE_PATH = f"{settings.MEDIA_ROOT}/{filename}"

    return read_text_file(FILE_PATH)