
#!/bin/bash
set -e

echo "Deployment started ..."

# Pull the latest version of the app
git pull origin master
echo "New changes copied to server !"

# Activate Virtual Env
source env/bin/activate
echo "Virtual env 'env' Activated !"

echo "Installing Dependencies..."
pip install -r requirements.txt --no-input

echo "Serving Static Files..."
python3 manage.py collectstatic --noinput

echo "Running Database migration"
python3 manage.py makemigrations
python3 manage.py migrate

# Deactivate Virtual Env
deactivate
echo "Virtual env 'env' Deactivated !"

# Reloading Application So New Changes could reflect on website
pushd sailoon
touch wsgi.py
popd

echo "Deployment Finished!"