![सीताराम](accounts/static/accounts/img/sitaram.jpg)

## Create a mobile only website within minutes

> 1. register yourself with pythonanywhere.com

> 2. choose a username when registering carefully that will be part of website domain

> 3. for example. if username is amitxvf, then domain will be amitxvf.pythonanywhere.com

> 4. create an account with fast2sms.com for otp message to send

> 5. a secret key will be provided that may be long string like jWhDCaRSfX5YmxZw2qlIKubtTBznVMOLrd39cyPF4pIeU6Bo91QmFtJ8hYjZX3swCTv6pVBdOIWEu7xZ

> 6. login to pythonanywhere.com with your account

> 7. change system image going into account -> system image -> change to python3.8 all field

> 8. create a web app using manual configuration

> 9. test your web app running successfully

> 10. open a bash console and peform [`setup.sh`](https://github.com/amit1870/sitaramsita/blob/sitaram/setup.sh) commands

> 11. change the content of `/var/www/{username}_pythonanywhere_com_wsgi.py` from below [WSGI]

> 12. change the value of `SECRET_KEY` and `SMS_AUTH_SECRET_KEY`

> 13. `SECRET_KEY` can be any string like TBznVMOLrd39cyPF4pIeU6Bo91QmFtJ8hYjZX3swCTv6pVBdOIW

> 14. `SMS_AUTH_SECRET_KEY` will be from `step 5`

> 15. do not forget to reload webapp

> 16. launch your [सीताराम](https://amitxvf.pythonanywhere.com/)


## [WSGI]

```
import os
import sys

HOME = os.environ['HOME']
CODE_PATH = f'{HOME}/sitaramsita'

if CODE_PATH not in sys.path:
    sys.path.insert(0, CODE_PATH)

os.environ["DJANGO_SETTINGS_MODULE"] = "sitaramsita.settings"
os.environ["SECRET_KEY"] = "SECRET_KEY"
os.environ["FAST_SMS_AUTH_KEY"] = "SMS_AUTH_SECRET_KEY"
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

```

# सीताराम