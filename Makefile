build:
	docker build -t cortlandt .

test: build
	docker run -it cortlandt /bin/bash -c "python3 -i -m unittest discover -v /app/tests/"

run: build
	docker run -it cortlandt /bin/bash -c "python3 -i ./app/run.py 2 1750"

sheets: build
	docker run -it cortlandt /bin/bash -c "python3 -i ./app/sheets.py"

directions: build
	docker run -it cortlandt /bin/bash -c "python3 -i ./app/directions.py"

doc: build
	docker run -it cortlandt /bin/bash

re: build run
