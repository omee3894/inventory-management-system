#!/usr/bin/env bash
#!/usr/bin/env bash

python manage.py migrate
python manage.py collectstatic --noinput
pip install -r requirements.txt

python manage.py migrate

python manage.py collectstatic --noinput

# Create superuser automatically (only if not exists)
python manage.py shell << END
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
END