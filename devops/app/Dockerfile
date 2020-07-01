FROM python:3.8

MAINTAINER Rishat Sharafiev <rishatsharafiev@ya.ru>

# create app path
RUN mkdir -p /app
WORKDIR /app

# Add a non-root user to prevent files being created with root permissions on host machine.
ARG USER=app
ARG UID=1000
ARG GID=1000
ARG HOME=/app
RUN groupadd $GID
RUN useradd -u $UID -g $GID -b $HOME $USER

# update pip
RUN pip install pip==20.1.1

# install poetry
RUN pip install --no-cache-dir poetry==1.0.9

# copy application code
ADD . /app
RUN chown -R ${UID}:${GID} /app

# install packages
RUN poetry config virtualenvs.create false
RUN poetry install

EXPOSE 8080
