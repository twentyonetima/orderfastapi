FROM python:3.13-slim

RUN apt-get update && apt-get install -y postgresql-client curl

RUN curl -sS https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh -o /wait-for-it.sh \
    && chmod +x /wait-for-it.sh

WORKDIR /app

COPY rq.txt .

RUN pip install --upgrade pip && pip install -r rq.txt

COPY . .

COPY start.sh ./start.sh
RUN chmod +x ./start.sh

CMD ["./start.sh"]