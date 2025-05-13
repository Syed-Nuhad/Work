python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Collect static files and migrate
python3.9 manage.py collectstatic --noinput
python3.9 manage.py migrate