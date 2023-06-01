start:
	python3 -m uvicorn main:app --reload

login:
	space login

link:
 	space link

build:
	space push


.PHONY: start
