FROM python:3.8.10

RUN apt-get install git -y
RUN pip install -r reqq.txt
COPY src src

CMD [ "uvicorn app.main:app" ]