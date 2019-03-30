FROM ubuntu:18.04
MAINTAINER Kojima <kojima.ryosuke.8e@kyoto-u.ac.jp>
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get install -y wget bzip2 curl git lsb-release gnupg sudo nginx
RUN mkdir -p /usr/yukari
WORKDIR /usr/yukari

ADD app/default /etc/nginx/sites-available/default
ADD app/setup.sh /usr/hark/setup.sh


ENTRYPOINT tail -f /dev/null
