web: bin/start-nginx daphne -b * -p $PORT MoonMachine.MoonMachine.asgi:application
worker: python manage.py runworker
worker: python manage.py runworker
worker: touch /tmp/app-initialized/requiredfile.txt