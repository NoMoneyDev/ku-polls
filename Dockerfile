FROM python:3-alpine

WORKDIR /app/polls

COPY . .
COPY entrypoint.sh /entrypoint.sh

RUN pip install -r requirements.txt

ARG SECRET_KEY
ARG ALLOWED_HOSTS=127.0.0.1,localhost

ENV SECRET_KEY=${SECRET_KEY}
ENV DEBUG=True
ENV ALLOWED_HOSTS=${ALLOWED_HOSTS}
ENV TIME_ZONE=Asia/Bangkok

RUN chmod +x /entrypoint.sh

EXPOSE 8000

CMD [ "/entrypoint.sh" ]