build:
	docker build -t cortlandt .

test: build
	docker run -it cortlandt /bin/bash -c "python3 -i -m unittest discover /app/tests/"

run: build
	docker run -it cortlandt /bin/bash -c "python3 -i ./app/run.py"



re: build run
