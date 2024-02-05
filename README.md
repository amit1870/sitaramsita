# [सीताराम](https://amitxvf.pythonanywhere.com/)
![सीताराम](accounts/static/accounts/img/sitaram.jpg)

## [Account Creation]

1. create a google account with similar to like dukan

2. create a pythonanywhere.com account with the email

3. create a account with fast2sms.com for message otp

## [PythonAnyWhere]

1. create web app manual configuration choosing python3.8

2. test created web app

3. go to console and perform `setup.sh` commands

4. do not forget to reload webapp


## [WSGI]

```
import os
import sys

HOME = os.environ['HOME']
CODE_PATH = f'{HOME}/sitaramsita'

if CODE_PATH not in sys.path:
    sys.path.insert(0, CODE_PATH)

os.environ["DJANGO_SETTINGS_MODULE"] = "sitaramsita.settings"
os.environ["SECRET_KEY"] = "WhDCWhDCaQSfX5YmxhDCaQSfX5YKubtTASfX5YmxZw2qlHKubtTA"
os.environ["FAST_SMS_AUTH_KEY"] = "SMS_AUTH_SECRET_KEY"
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

```

# सीताराम