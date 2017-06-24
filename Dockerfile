FROM ubuntu:trusty

RUN apt-get update && apt-get install -y \
    python3 \ 
    python3-pip \
    wget

RUN pip3 install --upgrade pip && \
    pip3 install googlemaps pygsheets selenium 


RUN apt-get install -y phantomjs

RUN mkdir -p ./app/
COPY *.json ./app/
COPY *.py ./app/
COPY /tests/ ./app/tests/

ENV PYTHONPATH=$PYTHONPATH:/app/
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8


# CMD ["python3", "-i", "/scrape.py"]
