# Container image that runs your code
FROM python:alpine

ARG requirements=requirements.txt
COPY requirements*.txt ./

RUN pip install --no-cache-dir -r $requirements
RUN rm ./requirements*.txt

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]