FROM python:alpine3.6

WORKDIR /opt/inobi/

COPY requirements.txt ./

RUN apk --update add \
      libffi-dev python3-dev \
      libffi python3 py-pip \
      tzdata

ENV TZ=Asia/Bishkek


RUN pip3 install --no-cache-dir -r requirements.txt

RUN rm -rf /var/cache/apk/*

COPY . .

EXPOSE 2222

CMD python ./run.py
