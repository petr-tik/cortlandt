
build:
	docker build -t flat-scraper .

run:
	docker run -it flat-scraper /bin/bash -c "python3 -i scrape.py"



re: build run
