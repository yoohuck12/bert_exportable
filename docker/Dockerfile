# Dockerfile for make base image for run_squad.py
# docker build -t ubuntu_with_tf ./
# docker tag ubuntu_with_tf:latest yoohuck12/ubuntu_with_tf:latest
# docker push yoohuck12/ubuntu_with_tf:latest

FROM index.docker.io/ubuntu:18.04

RUN apt update
RUN apt install -y python3-dev python3-pip python3-venv

RUN pip3 install --upgrade tensorflow
RUN python3 -c "import tensorflow as tf;print(tf.reduce_sum(tf.random.normal([1000, 1000])))"

RUN ln -s /usr/bin/python3 /usr/bin/python

RUN pip3 install --upgrade numpy
