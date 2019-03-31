FROM ubuntu:18.04
MAINTAINER Kojima <kojima.ryosuke.8e@kyoto-u.ac.jp>
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get install -y wget bzip2 curl git lsb-release gnupg sudo nginx sox build-essential unzip ffmpeg
RUN mkdir -p /usr/yukari
WORKDIR /usr/yukari

ENV CONDA_ROOT /root/miniconda
ENV PYTHONPATH /usr/yukari/
ENV PATH /root/miniconda/bin:$PATH
SHELL ["/bin/bash", "-c"]

RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
    bash ~/miniconda.sh -b -p $CONDA_ROOT && \
    ln -s ${CONDA_ROOT}/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
    echo ". ${CONDA_ROOT}/etc/profile.d/conda.sh" >> ~/.bashrc 

RUN pip install librosa numpy chainer pysptk fastdtw pyworld matplotlib chainerui
RUN git clone https://github.com/yamachu/WORLD4py && cd WORLD4py && python setup.py install

RUN git clone https://github.com/naegawa/become-yukarin.git

ENTRYPOINT cd /usr/yukari/become-yukarin/app && python app.py && tail -f /dev/null

