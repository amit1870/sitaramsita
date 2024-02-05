# [सीताराम](https://amitxvf.pythonanywhere.com/)
![सीताराम](accounts/static/accounts/img/sitaram.jpg)

## [Account Creation]

### create a google account with similar to like dukan

### create a pythonanywhere.com account with the email

###  change system image in pythonanywere.com account setting

### create a account with fast2sms.com for message otp

###  get secret key with you that will be used in wsgi setup


## [PythonAnyWhere console]

### run setup.sh commands with no error


## [wsgi file change and reload]

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