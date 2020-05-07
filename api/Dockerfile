FROM ubuntu:18.04

RUN apt update -y && \
    apt install -y python3-pip python3

RUN mkdir -p /api

COPY requirements.txt /usr/src/app

WORKDIR /api

RUN pip3 install -r requirements.txt

ENTRYPOINT ["flask"]
CMD ["run", "--host=0.0.0.0", "--port=9000"]