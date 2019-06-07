FROM python:3.7
RUN apt update
RUN apt install -y  ffmpeg
CMD rm -rf /usr/src/app
ENV workdir /usr/src/app
WORKDIR ${workdir}
CMD mkdir -p ${workdir}
ADD . ${workdir}
RUN pip install -r requirements.txt

