FROM ubuntu:trusty

RUN apt-get update && apt-get install -y \
    python3 \ 
    python3-pip \
    wget

RUN pip3 install --upgrade pip && \
    pip3 install googlemaps pygsheets selenium 


RUN apt-get install -y phantomjs


COPY service_creds.json service_creds.json
COPY run.py ./run.py
COPY scrape.py ./scrape.py
COPY directions.py ./directions.py
