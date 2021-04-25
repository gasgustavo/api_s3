FROM python:latest
MAINTAINER Gustavo Adriano
COPY . .
WORKDIR . 
RUN pip install -r requirements.txt 
CMD python apis3.py 8888 True 
EXPOSE 8888