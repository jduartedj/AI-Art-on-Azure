# For more information, please refer to https://aka.ms/vscode-docker-python
# FROM python:3.8-slim
FROM nvidia/cuda:11.4.2-runtime-ubuntu20.04

#set up environment
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get install -y unzip
RUN apt-get -y install python3
RUN apt-get -y install python3-pip
RUN apt-get -y install wget

EXPOSE 5002

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt

WORKDIR /app
COPY . /app

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

#DOES NOT WORK, need to find a way to pre-download the models so that this is done at image build
#RUN wget http://0.0.0.0:5002/create_image/pink%20football
RUN python3 ./download.py
RUN rm -f ./download.py

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["gunicorn", "--timeout", "3600", "--bind", "0.0.0.0:5002", "app:app"]


