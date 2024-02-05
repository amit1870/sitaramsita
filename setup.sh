#!/bin/sh

# go to $HOME dir
cd $HOME

# create virtual env for package install
mkvirtualenv --python /usr/bin/python3.8 vrenv

# activate virtual env
workon vrenv

# go to $HOME dir
cd $HOME

# clone git code
git clone https://ghp_b2VYWGWEwKQxAIOIOHe4ivNMsyWtsx0ZGaUY@github.com/amit1870/sitaramsita.git

cd sitaramsita

# install requirements
pip install -r requires.txt

# run migration commands
python manage.py makemigrations accounts dukan

# run migrate command if no error in pevious command
python manage.py migrate

# run command to create superuser
python manage.py createsuperuser

# create static and media dir
mkdir -p static media

# collect static files
python manage.py collectstatic

# go to $HOME dir
cd $HOME

# reload app
touch $WSGI_FILE

# create a task
