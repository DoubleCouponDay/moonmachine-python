web: bin/start-nginx daphne -b 0.0.0.0 -p $PORT MoonMachine.MoonMachine.asgi:application
worker: python manage.py runworker
worker: touch /tmp/app-initialized/requiredfile.txt