ifeq ($(OS), Windows_NT)
include .env
init:
	@pip install -r requirements.txt

run_user:
	@flask --app app:user run -p ${USER_PORT} --debug

run_note:
	@flask --app app:note run -p ${NOTE_PORT} --debug

run_label:
	@flask --app app:user run -p ${USER_PORT} --debug

endif