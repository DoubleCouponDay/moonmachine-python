web: bin/start-nginx daphne -b 0.0.0.0 -p $PORT app.asgi:application
worker: python ./app/manage.py runworker
worker: touch ./tmp/app-initialized/requiredfile.txt