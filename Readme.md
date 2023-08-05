Project initialization
1. python -m venv venv
2. source venv/Scripts/activate
3. pip install -r requirements.txt


DB migration commands
1. flask db init
2. flask --app app:<app-instance> db migrate -m "<message>"
3. flask --app app:<app-instance> db upgrade

Celery command
1. celery -A tasks.celery -l info --pool=solo

App server commands
1. make run_user
2. make run_note