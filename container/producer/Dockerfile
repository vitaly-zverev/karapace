FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY producer.py .
RUN  mkdir -p ./container/producer
COPY . ./container/producer/

CMD [ "python", "./producer.py" ]