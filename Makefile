build:
	docker build -t cortlandt .

test: build
	docker run -it cortlandt /bin/bash -c "python3 -m unittest discover /app/"

run:
	docker run -it cortlandt /bin/bash -c "python3 -i ./app/run.py"



re: build run
