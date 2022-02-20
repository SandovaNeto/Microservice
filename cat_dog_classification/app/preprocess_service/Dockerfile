FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

RUN pip install --upgrade pip

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6 -y

WORKDIR /usr/src/app

COPY ./requirements.txt $WORKDIR
RUN pip install -r requirements.txt

COPY ./app/ $WORKDIR

EXPOSE 7998

CMD ["python", "app_server.py"]

