DJANGO_SETTINGS_MODULE=telemann.settings python src/manage.py tailwind install
DJANGO_SETTINGS_MODULE=telemann.settings python src/manage.py tailwind build
DJANGO_SETTINGS_MODULE=telemann.settings python src/manage.py collectstatic --noinput
