FROM python:slim as base
RUN apt-get update
RUN apt-get install ffmpeg wget -y
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install --upgrade -r /app/requirements.txt
RUN wget https://github.com/AlexeyAB/darknet/releases/download/yolov4/yolov7.weights
RUN wget https://raw.githubusercontent.com/AlexeyAB/darknet/master/cfg/yolov7.cfg
COPY . .
RUN mv yolov7.weights /app/api/models/
RUN mv yolov7.cfg /app/api/models/yolov7.cfg
CMD ["uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "3100"]