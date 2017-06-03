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

# CMD ["python3", "-i", "/scrape.py"]
