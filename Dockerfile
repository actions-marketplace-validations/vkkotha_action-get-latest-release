# Container image that runs your code
FROM python:alpine

RUN pip install --no-cache-dir pygithub

VOLUME /app
WORKDIR /app
COPY entrypoint.py /app/entrypoint.py

RUN chmod +x /app/entrypoint.py
ENTRYPOINT ["./entrypoint.py"]