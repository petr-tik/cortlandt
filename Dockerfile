FROM ubuntu:trusty

RUN apt-get update && apt-get install -y python3 python3-pip wget

RUN pip3 install --upgrade pip && \
    pip3 install selenium pygsheets

## Install phantom js and tidy up afterwards
## Uses a fixed version of phantomjs  development of new features will stop soon

COPY service_creds.json service_creds.json
COPY run.py ./run.py
RUN chmod +x run.py
#CMD ["/run.py"]
