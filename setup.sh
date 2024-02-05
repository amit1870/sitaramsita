#!/bin/sh
USER=$1
AUTH_KEY=$2
echo "set up started for ${USER}.pythonanywhere.com ....\n"

# go to $HOME dir
cd $HOME

# create virtual env for package install
mkvirtualenv --python /usr/bin/python3.8 vrenv

if [ "$?" -ne "0" ]; then
    echo "some error occured during virtual env creation ...\n"
    echo "stopping ..."
    exit
fi

# activate virtual env
workon vrenv

# go to $HOME dir
cd $HOME

# clone git code
git clone https://ghp_b2VYWGWEwKQxAIOIOHe4ivNMsyWtsx0ZGaUY@github.com/amit1870/sitaramsita.git

cd sitaramsita

# install requirements
pip install -q -r requires.txt

# run migration commands
python manage.py makemigrations accounts dukan

if [ "$?" -ne "0" ]; then
    echo "some error occured during creating migrations ...\n"
    echo "stopping ..."
    exit
fi

# run migrate command if no error in pevious command
python manage.py migrate

if [ "$?" -ne "0" ]; then
    echo "some error occured during sql migrations ...\n"
    echo "stopping ..."
    exit
fi

# create static and media dir
mkdir -p static media

if [ "$?" -ne "0" ]; then
    echo "some error occured during dir creation ...\n"
    echo "stopping ..."
    exit
fi

# collect static files
python manage.py collectstatic

if [ "$?" -ne "0" ]; then
    echo "some error occured during setup ...\n"
    echo "stopping ..."
    exit
fi

# go to $HOME dir
cd $HOME

# empty wsgi file
WSGI_FILE="/var/www/${USER}_pythonanywhere_com_wsgi.py"
touch $WSGI_FILE
> $WSGI_FILE

if [ "$?" -ne "0" ]; then
    echo "some error occured during empting ${USER}_pythonanywhere_com_wsgi.py ...\n"
    echo "stopping ..."
    exit
fi

# add content to wsgi file
echo "import os" >> $WSGI_FILE
echo "import sys" >> $WSGI_FILE
echo "HOME = os.environ['HOME']" >> $WSGI_FILE
echo "CODE_PATH = f'{HOME}/sitaramsita'" >> $WSGI_FILE
echo "if CODE_PATH not in sys.path:" >> $WSGI_FILE
echo "    sys.path.insert(0, CODE_PATH)" >> $WSGI_FILE
echo "os.environ['DJANGO_SETTINGS_MODULE'] = 'sitaramsita.settings'" >> $WSGI_FILE
echo "os.environ['SECRET_KEY'] = 'WhDCWhDCaQSfX5YmxhDCaQSfX5YKubtTASfX5YmxZw2qlHKubtTA'" >> $WSGI_FILE
echo "os.environ['FAST_SMS_AUTH_KEY'] = '${AUTH_KEY}'" >> $WSGI_FILE
echo "from django.core.wsgi import get_wsgi_application" >> $WSGI_FILE
echo "application = get_wsgi_application()"
echo "" >> $WSGI_FILE

echo "wsgi file set up finished."

touch $WSGI_FILE

echo "reloading ${WSGI_FILE} ..."


echo "create superuser manually."

echo "console set up finished successfully for ${USER}.pythonanywhere.com ....\n"

echo "finished !!"


