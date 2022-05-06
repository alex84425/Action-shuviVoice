# ##########################################################################
# Build uut operation proxy base image (temp solution for ssh)
# ##########################################################################
FROM node:14.18-slim AS uut-operation-proxy-base

RUN apt update && apt install -y vim curl

# for nodejs 14
RUN curl -sL https://deb.nodesource.com/setup_14.x | bash -
RUN apt -y install nodejs
RUN node -v

COPY ./ActionTemplate-Python3/UUTOperationProxy/. /UUTOperationProxy
WORKDIR /UUTOperationProxy
RUN npm ci
RUN npm install -g pkg
RUN pkg .

###########################################################################
# Create requirements from poetry
###########################################################################
FROM python:3.8-slim-buster as requirements-stage

WORKDIR /tmp
RUN pip install poetry
COPY ./pyproject.toml ./poetry.lock* /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes
RUN poetry export --dev -f requirements.txt --output requirements-dev.txt --without-hashes

###########################################################################
# Build dev base image
###########################################################################
FROM tiangolo/uvicorn-gunicorn:python3.8-slim AS dev-base

# set working directory
WORKDIR /app/

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV MAX_WORKERS=1
ENV LOG_LEVEL=debug
ENV PORT 8080
EXPOSE 8080

# install system dependencies
RUN apt-get update \
  && apt-get -y install --no-install-recommends \
  netcat \
  gcc \
  zip \
  curl \
  procps \
  vim \
  git \
  openssl \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* \
  && pip install --upgrade pip

COPY --from=requirements-stage /tmp/requirements.txt /opt/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /opt/requirements.txt

# Install submodule
COPY ./ActionTemplate-Python3/ /opt/action_template/
RUN pip install -e /opt/action_template/

COPY ./src /app

###########################################################################
# Build dev env image
###########################################################################
FROM dev-base AS dev-env
COPY --from=requirements-stage /tmp/requirements-dev.txt /opt/requirements-dev.txt
RUN pip install --no-cache-dir --upgrade -r /opt/requirements-dev.txt

###########################################################################
# Build lint image
###########################################################################
FROM dev-env AS dev-linter
COPY ./setup.cfg /app/
RUN pylama -o setup.cfg


###########################################################################
# Build utest coverage image
###########################################################################
FROM dev-env AS dev-coverage
RUN coverage run -m pytest -p no:warnings --cov=. --cov-report html --cov-report xml
RUN mkdir -p /var/src/htmlcov \
  && cp -r htmlcov  /var/src/htmlcov \
  && cp coverage.xml /var/src/coverage.xml

###########################################################################
# Build security check image
###########################################################################
FROM dev-env AS dev-security
RUN python -m bandit -r /app/app
RUN python -m safety check

###########################################################################
# Build production image - api
###########################################################################
FROM dev-base

VOLUME [ "/data" ]

# setup uut operaiont proxy binary
COPY --from=uut-operation-proxy-base /UUTOperationProxy/dist/uut-operation-proxy-linux /opt/uut-operation-proxy-linux

# use Gunicorn running Uvicorn workers in the container
# CMD /start.sh