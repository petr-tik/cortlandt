build:
	docker build -t cortlandt .

test: build
	docker run -it cortlandt /bin/bash -c "python3 -i -m unittest discover -v /app/tests/"

run: build
	docker run -it cortlandt /bin/bash -c "python3 -i ./app/run.py"

sheets: build
	docker run -it cortlandt /bin/bash -c "python3 -i ./app/sheets.py"

directions: build
	docker run -it cortlandt /bin/bash -c "python3 -i ./app/directions.py"

re: build run
