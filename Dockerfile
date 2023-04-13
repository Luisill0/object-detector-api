FROM python:slim
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6 -y
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install --upgrade -r /app/requirements.txt
COPY ./api/models /app/api/models
COPY ./download_models.py /app/download_models.py
RUN python3 /app/download_models.py
COPY . /app
CMD ["uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "3100"]
EXPOSE 3100