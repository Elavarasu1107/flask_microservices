ifeq ($(OS), Windows_NT)
include .env
init:
	@pip install -r requirements.txt

run_user:
	@flask --app app:user run -p ${USER_PORT} --debug

run_note:
	@flask --app app:note run -p ${NOTE_PORT} --debug

run_label:
	@flask --app app:label run -p ${LABEL_PORT} --debug

celery:
	@watchmedo auto-restart --pattern=tasks.py --recursive -- celery -A tasks.celery worker -l info --pool=solo

note_migrate:
	@flask --app app:note db migrate
	@flask --app app:note db upgrade

user_migrate:
	@flask --app app:user db migrate
	@flask --app app:user db upgrade

label_migrate:
	@flask --app app:label db migrate
	@flask --app app:label db upgrade

endif